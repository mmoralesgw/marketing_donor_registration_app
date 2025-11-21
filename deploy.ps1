# PowerShell deployment script for Azure App Service

# Configuration
$RESOURCE_GROUP = "goodwill-rg"
$APP_NAME = "goodwill-donor-app"
$LOCATION = "eastus"
$PLAN_NAME = "goodwill-plan"

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Azure App Service Deployment Script" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan

# Check if Azure CLI is installed
if (!(Get-Command az -ErrorAction SilentlyContinue)) {
    Write-Host "Error: Azure CLI is not installed" -ForegroundColor Red
    Write-Host "Install from: https://docs.microsoft.com/en-us/cli/azure/install-azure-cli"
    exit 1
}

# Login to Azure
Write-Host "Logging in to Azure..." -ForegroundColor Yellow
az login

# Create resource group
Write-Host "Creating resource group..." -ForegroundColor Yellow
az group create --name $RESOURCE_GROUP --location $LOCATION

# Create App Service plan
Write-Host "Creating App Service plan..." -ForegroundColor Yellow
az appservice plan create `
    --name $PLAN_NAME `
    --resource-group $RESOURCE_GROUP `
    --sku B1 `
    --is-linux

# Create web app
Write-Host "Creating web app..." -ForegroundColor Yellow
az webapp create `
    --resource-group $RESOURCE_GROUP `
    --plan $PLAN_NAME `
    --name $APP_NAME `
    --runtime "PYTHON:3.11"

# Set startup command
Write-Host "Configuring startup command..." -ForegroundColor Yellow
az webapp config set `
    --resource-group $RESOURCE_GROUP `
    --name $APP_NAME `
    --startup-file "gunicorn --bind=0.0.0.0 --timeout 600 app:app"

Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "IMPORTANT: Configure Application Settings" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Go to Azure Portal and add these settings:" -ForegroundColor Yellow
Write-Host ""
Write-Host "SMTP_SERVER = smtp.office365.com"
Write-Host "SMTP_PORT = 587"
Write-Host "SENDER_EMAIL = gw-appdev@GoodwillMiami.org"
Write-Host "SENDER_PASSWORD = [your-password]"
Write-Host "ORG_NAME = Goodwill Miami"
Write-Host "ORG_ADDRESS = 2121 NW 21st Street, Miami, FL 33142"
Write-Host "ORG_TAX_ID = [your-tax-id]"
Write-Host "ORG_PHONE = [your-phone]"
Write-Host "ORG_EMAIL = gw-appdev@GoodwillMiami.org"
Write-Host ""
Write-Host "Or run this command after updating the values:" -ForegroundColor Yellow
Write-Host ""
Write-Host "az webapp config appsettings set --resource-group $RESOURCE_GROUP --name $APP_NAME --settings SMTP_SERVER='smtp.office365.com' SMTP_PORT='587' SENDER_EMAIL='gw-appdev@GoodwillMiami.org' SENDER_PASSWORD='your-password' ORG_NAME='Goodwill Miami' ORG_ADDRESS='2121 NW 21st Street, Miami, FL 33142' ORG_TAX_ID='your-tax-id' ORG_PHONE='your-phone' ORG_EMAIL='gw-appdev@GoodwillMiami.org'"
Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Deploying application..." -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan

# Deploy the app
az webapp up `
    --resource-group $RESOURCE_GROUP `
    --name $APP_NAME `
    --runtime "PYTHON:3.11"

Write-Host ""
Write-Host "==========================================" -ForegroundColor Green
Write-Host "Deployment Complete!" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Green
Write-Host "Your app is available at:" -ForegroundColor Yellow
Write-Host "https://$APP_NAME.azurewebsites.net" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Configure application settings in Azure Portal"
Write-Host "2. Test the application"
Write-Host "3. Monitor logs for any issues"
Write-Host "==========================================" -ForegroundColor Green
