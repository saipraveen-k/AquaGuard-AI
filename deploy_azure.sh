# Azure Web App Deployment Script for AquaGuard AI
# Microsoft-preferred deployment method

# Login to Azure
az login

# Set variables
RESOURCE_GROUP="AquaGuard-Web-RG"
APP_SERVICE_PLAN="AquaGuard-Plan"
WEB_APP_NAME="aquaguard-ai-webapp"
LOCATION="eastus2"

# Create Resource Group
echo "Creating resource group..."
az group create --name $RESOURCE_GROUP --location $LOCATION

# Create App Service Plan (Linux)
echo "Creating App Service Plan..."
az appservice plan create \
  --name $APP_SERVICE_PLAN \
  --resource-group $RESOURCE_GROUP \
  --sku B1 \
  --is-linux \
  --location $LOCATION

# Create Web App
echo "Creating Web App..."
az webapp create \
  --name $WEB_APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --plan $APP_SERVICE_PLAN \
  --runtime "PYTHON|3.9" \
  --startup-file "web_app.py"

# Configure Web App
echo "Configuring Web App settings..."
az webapp config appsettings set \
  --resource-group $RESOURCE_GROUP \
  --name $WEB_APP_NAME \
  --settings WEBSITE_RUN_FROM_PACKAGE=1 FLASK_APP=web_app.py

# Enable CORS
az webapp cors add \
  --resource-group $RESOURCE_GROUP \
  --name $WEB_APP_NAME \
  --allowed-origins "*"

# Get deployment credentials
echo "Getting deployment credentials..."
az webapp deployment user set --user-name aquaguard --password AquaGuard2026!

# Get Git URL
GIT_URL=$(az webapp deployment source config-local-git --resource-group $RESOURCE_GROUP --name $WEB_APP_NAME --query url --output tsv)

echo "Deployment setup complete!"
echo "Web App URL: https://$WEB_APP_NAME.azurewebsites.net"
echo "Git URL: $GIT_URL"
echo ""
echo "Next steps:"
echo "1. git add ."
echo "2. git commit -m 'Deploy AquaGuard AI to Azure'"
echo "3. git remote add azure $GIT_URL"
echo "4. git push azure master"
