# Azure App Service Deployment Guide

## Prerequisites
- Azure account with active subscription
- Azure CLI installed (optional, for command-line deployment)

## Deployment Methods

### Method 1: Deploy via Azure Portal (Recommended for beginners)

1. **Create Azure App Service**
   - Go to [Azure Portal](https://portal.azure.com)
   - Click "Create a resource" → "Web App"
   - Fill in the details:
     - **Subscription**: Your subscription
     - **Resource Group**: Create new or use existing
     - **Name**: `goodwill-donor-app` (or your preferred name)
     - **Publish**: Code
     - **Runtime stack**: Python 3.11
     - **Operating System**: Linux
     - **Region**: Choose closest to your location
     - **Pricing Plan**: Choose appropriate tier (B1 or higher recommended)
   - Click "Review + Create" → "Create"

2. **Configure Application Settings (Environment Variables)**
   - Go to your App Service
   - Navigate to "Configuration" → "Application settings"
   - Add the following settings:

   ```
   SMTP_SERVER = smtp.gmail.com
   SMTP_PORT = 587
   SENDER_EMAIL = noreply@yourdomain.com
   SENDER_PASSWORD = [your-gmail-app-password]
   ORG_NAME = Goodwill Miami
   ORG_ADDRESS = 2121 NW 21st Street, Miami, FL 33142
   ORG_TAX_ID = [your-tax-id]
   ORG_PHONE = [your-phone]
   ORG_EMAIL = info@goodwillmiami.org
   SCM_DO_BUILD_DURING_DEPLOYMENT = true
   ```

   **Note:** Get Gmail App Password from `GMAIL_SETUP.md`

   - Click "Save"

3. **Configure Startup Command**
   - In "Configuration" → "General settings"
   - Set **Startup Command**: `gunicorn --bind=0.0.0.0 --timeout 600 app:app`
   - Click "Save"

4. **Deploy Code**
   
   **Option A: Deploy from Local Git**
   - In your App Service, go to "Deployment Center"
   - Choose "Local Git" as source
   - Copy the Git URL
   - In your local project folder:
     ```bash
     git init
     git add .
     git commit -m "Initial commit"
     git remote add azure [paste-git-url-here]
     git push azure master
     ```

   **Option B: Deploy from GitHub**
   - Push your code to GitHub
   - In "Deployment Center", choose "GitHub"
   - Authorize and select your repository
   - Azure will automatically deploy

   **Option C: Deploy via ZIP**
   - Zip your project files (exclude .git, __pycache__, venv)
   - In "Deployment Center", choose "ZIP Deploy"
   - Upload your ZIP file

5. **Verify Deployment**
   - Go to your App Service URL: `https://goodwill-donor-app.azurewebsites.net`
   - The donor form should load
   - Test submitting a donation

### Method 2: Deploy via Azure CLI

```bash
# Login to Azure
az login

# Create resource group
az group create --name goodwill-rg --location eastus

# Create App Service plan
az appservice plan create --name goodwill-plan --resource-group goodwill-rg --sku B1 --is-linux

# Create web app
az webapp create --resource-group goodwill-rg --plan goodwill-plan --name goodwill-donor-app --runtime "PYTHON:3.11"

# Configure app settings
az webapp config appsettings set --resource-group goodwill-rg --name goodwill-donor-app --settings \
  SMTP_SERVER="smtp.office365.com" \
  SMTP_PORT="587" \
  SENDER_EMAIL="gw-appdev@GoodwillMiami.org" \
  SENDER_PASSWORD="your-password" \
  ORG_NAME="Goodwill Miami" \
  ORG_ADDRESS="2121 NW 21st Street, Miami, FL 33142" \
  ORG_TAX_ID="your-tax-id" \
  ORG_PHONE="your-phone" \
  ORG_EMAIL="gw-appdev@GoodwillMiami.org"

# Set startup command
az webapp config set --resource-group goodwill-rg --name goodwill-donor-app --startup-file "gunicorn --bind=0.0.0.0 --timeout 600 app:app"

# Deploy from local directory
az webapp up --resource-group goodwill-rg --name goodwill-donor-app --runtime "PYTHON:3.11"
```

## Important Notes

### Email Configuration
- Make sure the email account `gw-appdev@GoodwillMiami.org` has:
  - SMTP enabled
  - Correct password set in environment variables
  - No 2FA blocking (or use app-specific password)

### File Storage
- Azure App Service has ephemeral storage
- The `donors.csv` file will be lost on app restart
- **Recommended**: Implement Azure Blob Storage for persistent CSV storage

### To Add Azure Blob Storage (Optional but Recommended):

1. Create Azure Storage Account
2. Update `requirements.txt`:
   ```
   azure-storage-blob==12.19.0
   ```

3. Update app.py to use Blob Storage instead of local CSV

### Security Best Practices
- Never commit passwords to Git
- Use Azure Key Vault for sensitive data (production)
- Enable HTTPS only
- Set up custom domain with SSL certificate

### Monitoring
- Enable Application Insights for monitoring
- Check logs: `az webapp log tail --resource-group goodwill-rg --name goodwill-donor-app`
- Or view logs in Azure Portal → App Service → Log stream

### Scaling
- For production, consider:
  - Scaling up to higher tier (S1, P1V2)
  - Enable auto-scaling
  - Add Azure CDN for static files

## Troubleshooting

### App won't start
- Check logs in Azure Portal
- Verify Python version matches requirements
- Ensure all dependencies in requirements.txt

### Email not sending
- Verify environment variables are set correctly
- Check email credentials
- Test SMTP connection from Azure

### CSV not saving
- Check app has write permissions
- Consider implementing Azure Blob Storage

## Testing Your Deployment

1. Visit your app URL
2. Fill out the donation form
3. Submit and verify:
   - Success message appears
   - Email received
   - CSV download works

## Cost Estimation
- B1 Basic Plan: ~$13/month
- S1 Standard Plan: ~$70/month
- Storage: ~$0.02/GB/month

## Support
For issues, check:
- Azure Portal logs
- Application Insights
- Azure support documentation
