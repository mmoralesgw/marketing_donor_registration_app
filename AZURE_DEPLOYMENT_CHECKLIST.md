# Azure Deployment Checklist ✅

## Pre-Deployment Review

### ✅ Code Ready
- [x] Flask app configured with environment variable support
- [x] Microsoft Graph API integration for email
- [x] CORS enabled for cross-origin requests
- [x] Static file serving configured
- [x] CSV file handling implemented
- [x] PDF generation working
- [x] Error handling in place

### ✅ Azure Configuration Files
- [x] `requirements.txt` - All dependencies listed
- [x] `startup.txt` - Gunicorn startup command
- [x] `.deployment` - Build configuration
- [x] `web.config` - Windows compatibility (optional)
- [x] `.gitignore` - Excludes sensitive files

### ✅ Environment Variables Support
- [x] PORT - Auto-configured from Azure
- [x] AZURE_TENANT_ID - Graph API tenant
- [x] AZURE_CLIENT_ID - Graph API client
- [x] AZURE_CLIENT_SECRET - Graph API secret
- [x] SENDER_EMAIL - Email sender address
- [x] ORG_NAME - Organization name
- [x] ORG_ADDRESS - Organization address
- [x] ORG_TAX_ID - Tax ID
- [x] ORG_PHONE - Phone number
- [x] ORG_EMAIL - Organization email

## Deployment Steps

### 1. Azure AD App Registration (Required First!)
- [ ] Go to Azure Portal → Azure Active Directory → App registrations
- [ ] Create new registration: "Goodwill Donor App"
- [ ] Copy Tenant ID
- [ ] Copy Client ID
- [ ] Create Client Secret and copy value
- [ ] Grant API Permission: Mail.Send (Application)
- [ ] Grant admin consent

**Documentation:** See `GRAPH_API_SETUP.md`

### 2. Create Azure App Service
- [ ] Go to Azure Portal → Create Resource → Web App
- [ ] Name: `goodwill-donor-app` (or your choice)
- [ ] Runtime: Python 3.11
- [ ] Operating System: Linux (recommended)
- [ ] Region: Choose closest to users
- [ ] Pricing: B1 Basic or higher

### 3. Configure Application Settings
Go to App Service → Configuration → Application Settings

**Required Settings:**
```
AZURE_TENANT_ID = [from step 1]
AZURE_CLIENT_ID = [from step 1]
AZURE_CLIENT_SECRET = [from step 1]
SENDER_EMAIL = gw-appdev@GoodwillMiami.org
```

**Organization Settings:**
```
ORG_NAME = Goodwill Miami
ORG_ADDRESS = 2121 NW 21st Street, Miami, FL 33142
ORG_TAX_ID = [your-tax-id]
ORG_PHONE = [your-phone]
ORG_EMAIL = gw-appdev@GoodwillMiami.org
```

**Optional Settings:**
```
DEBUG = false
SCM_DO_BUILD_DURING_DEPLOYMENT = true
```

- [ ] Click "Save" after adding all settings

### 4. Configure Startup Command
- [ ] Go to Configuration → General Settings
- [ ] Startup Command: `gunicorn --bind=0.0.0.0 --timeout 600 app:app`
- [ ] Click "Save"

### 5. Deploy Code

**Option A: Local Git**
```bash
git init
git add .
git commit -m "Initial deployment"
git remote add azure [your-git-url]
git push azure master
```

**Option B: GitHub**
- [ ] Push code to GitHub
- [ ] In Azure: Deployment Center → GitHub
- [ ] Authorize and select repository
- [ ] Azure will auto-deploy

**Option C: Azure CLI**
```bash
az webapp up --resource-group goodwill-rg --name goodwill-donor-app --runtime "PYTHON:3.11"
```

**Option D: VS Code**
- [ ] Install Azure App Service extension
- [ ] Right-click on App Service → Deploy to Web App

### 6. Verify Deployment
- [ ] Go to your app URL: `https://goodwill-donor-app.azurewebsites.net`
- [ ] Check if the form loads
- [ ] Submit a test donation
- [ ] Verify email is received
- [ ] Test CSV download

### 7. Monitor and Troubleshoot
- [ ] Check Log Stream: App Service → Log stream
- [ ] View Application Insights (if enabled)
- [ ] Check for errors in logs

## Post-Deployment

### Security
- [ ] Enable HTTPS only: Configuration → General Settings
- [ ] Consider adding custom domain
- [ ] Set up SSL certificate
- [ ] Review CORS settings if needed

### Performance
- [ ] Consider scaling up if needed
- [ ] Enable Application Insights for monitoring
- [ ] Set up alerts for errors

### Backup
- [ ] Consider Azure Blob Storage for CSV persistence
- [ ] Set up automated backups
- [ ] Document recovery procedures

## Testing Checklist

After deployment, test:
- [ ] Form loads correctly
- [ ] All form fields work
- [ ] Donation submission succeeds
- [ ] Email is sent and received
- [ ] PDF receipt is attached
- [ ] CSV download works
- [ ] Data persists correctly

## Common Issues & Solutions

### Issue: App won't start
**Solution:** Check logs, verify Python version, check startup command

### Issue: Email not sending
**Solution:** Verify Graph API credentials, check permissions, ensure admin consent

### Issue: 500 Internal Server Error
**Solution:** Check Application Settings, verify all required env vars are set

### Issue: CSV not saving
**Solution:** Check app has write permissions, consider Azure Blob Storage

### Issue: Slow performance
**Solution:** Scale up to higher tier, optimize code, enable caching

## Rollback Plan

If deployment fails:
1. Check logs for errors
2. Revert to previous deployment slot (if configured)
3. Or redeploy last known good version
4. Contact support if needed

## Support Resources

- Azure Portal: https://portal.azure.com
- Azure Documentation: https://docs.microsoft.com/azure
- Graph API Docs: https://docs.microsoft.com/graph
- Project Documentation: See README.md, GRAPH_API_SETUP.md

## Deployment Scripts

Quick deployment scripts available:
- Windows: `deploy.ps1`
- Linux/Mac: `deploy.sh`

## Cost Estimate

- B1 Basic: ~$13/month
- S1 Standard: ~$70/month
- Storage: ~$0.02/GB/month
- Bandwidth: First 5GB free

## Notes

- CSV files are stored in ephemeral storage (lost on restart)
- Consider Azure Blob Storage for production
- Rotate client secrets before expiration
- Monitor usage and costs regularly
