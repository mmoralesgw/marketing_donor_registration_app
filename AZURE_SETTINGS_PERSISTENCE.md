# Azure Settings Persistence Guide

## Problem
When you deploy to Azure via GitHub, the deployment overwrites all files, causing your settings (locations, form title, email template) to reset.

## Solution Implemented
The app now stores settings in Azure's `/home` directory, which **persists across deployments**.

## How It Works

### Local Development
- Settings are stored in the current directory (`.`)
- Files: `donation_locations.json`, `form_title.txt`, `email_template.txt`

### Azure Production
- Settings are stored in `/home` directory
- This directory is **NOT overwritten** during deployments
- Your settings will persist even after pushing new code

## Files That Persist
✅ `donation_locations.json` - Your custom locations
✅ `form_title.txt` - Your custom form title  
✅ `email_template.txt` - Your custom email template
✅ `donors.csv` - Donor records

## Files That Update
🔄 `app.py` - Application code
🔄 `index.html` - Main form
🔄 `settings.html` - Settings page
🔄 All other code files

## Testing

### After Deployment:
1. Go to your Azure app
2. Change settings (add locations, change title, etc.)
3. Push new code to GitHub
4. Wait for deployment to complete
5. Check your app - **settings should still be there!**

## Verification

To verify settings are in the persistent directory on Azure:

1. Go to Azure Portal → Your App Service
2. Click "Advanced Tools" → "Go"
3. Click "Debug console" → "CMD"
4. Navigate to `/home`
5. You should see your settings files there

## Backup (Optional)

To backup your settings from Azure:

1. Go to Kudu console (Advanced Tools)
2. Navigate to `/home`
3. Download: `donation_locations.json`, `form_title.txt`, `email_template.txt`
4. Keep these as backups

## Important Notes

⚠️ The `/home` directory has limited space (1GB on Basic tier)
⚠️ If you delete the App Service, the `/home` directory is also deleted
⚠️ For production, consider using Azure Storage or Azure App Configuration for even more reliability

## Alternative: Azure App Configuration

For enterprise-level persistence, consider using Azure App Configuration:
- Settings stored in Azure cloud
- Version history
- Can be shared across multiple apps
- More reliable than file storage

Would you like help setting up Azure App Configuration instead?
