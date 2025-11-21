#!/bin/bash
# Quick deployment script for Azure App Service

# Configuration
RESOURCE_GROUP="goodwill-rg"
APP_NAME="goodwill-donor-app"
LOCATION="eastus"
PLAN_NAME="goodwill-plan"

echo "=========================================="
echo "Azure App Service Deployment Script"
echo "=========================================="

# Check if Azure CLI is installed
if ! command -v az &> /dev/null; then
    echo "Error: Azure CLI is not installed"
    echo "Install from: https://docs.microsoft.com/en-us/cli/azure/install-azure-cli"
    exit 1
fi

# Login to Azure
echo "Logging in to Azure..."
az login

# Create resource group
echo "Creating resource group..."
az group create --name $RESOURCE_GROUP --location $LOCATION

# Create App Service plan
echo "Creating App Service plan..."
az appservice plan create \
    --name $PLAN_NAME \
    --resource-group $RESOURCE_GROUP \
    --sku B1 \
    --is-linux

# Create web app
echo "Creating web app..."
az webapp create \
    --resource-group $RESOURCE_GROUP \
    --plan $PLAN_NAME \
    --name $APP_NAME \
    --runtime "PYTHON:3.11"

# Set startup command
echo "Configuring startup command..."
az webapp config set \
    --resource-group $RESOURCE_GROUP \
    --name $APP_NAME \
    --startup-file "gunicorn --bind=0.0.0.0 --timeout 600 app:app"

echo ""
echo "=========================================="
echo "IMPORTANT: Configure Application Settings"
echo "=========================================="
echo "Go to Azure Portal and add these settings:"
echo ""
echo "SMTP_SERVER = smtp.office365.com"
echo "SMTP_PORT = 587"
echo "SENDER_EMAIL = gw-appdev@GoodwillMiami.org"
echo "SENDER_PASSWORD = [your-password]"
echo "ORG_NAME = Goodwill Miami"
echo "ORG_ADDRESS = 2121 NW 21st Street, Miami, FL 33142"
echo "ORG_TAX_ID = [your-tax-id]"
echo "ORG_PHONE = [your-phone]"
echo "ORG_EMAIL = gw-appdev@GoodwillMiami.org"
echo ""
echo "Or run this command after updating the values:"
echo ""
echo "az webapp config appsettings set --resource-group $RESOURCE_GROUP --name $APP_NAME --settings \\"
echo "  SMTP_SERVER='smtp.office365.com' \\"
echo "  SMTP_PORT='587' \\"
echo "  SENDER_EMAIL='gw-appdev@GoodwillMiami.org' \\"
echo "  SENDER_PASSWORD='your-password' \\"
echo "  ORG_NAME='Goodwill Miami' \\"
echo "  ORG_ADDRESS='2121 NW 21st Street, Miami, FL 33142' \\"
echo "  ORG_TAX_ID='your-tax-id' \\"
echo "  ORG_PHONE='your-phone' \\"
echo "  ORG_EMAIL='gw-appdev@GoodwillMiami.org'"
echo ""
echo "=========================================="
echo "Deploying application..."
echo "=========================================="

# Deploy the app
az webapp up \
    --resource-group $RESOURCE_GROUP \
    --name $APP_NAME \
    --runtime "PYTHON:3.11"

echo ""
echo "=========================================="
echo "Deployment Complete!"
echo "=========================================="
echo "Your app is available at:"
echo "https://$APP_NAME.azurewebsites.net"
echo ""
echo "Next steps:"
echo "1. Configure application settings in Azure Portal"
echo "2. Test the application"
echo "3. Monitor logs for any issues"
echo "=========================================="
