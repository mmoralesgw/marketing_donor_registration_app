# Microsoft Graph API Setup Guide

The app now uses Microsoft Graph API to send emails, which is more secure and reliable than SMTP for Office 365 accounts.

## Step 1: Register an App in Azure AD

1. Go to [Azure Portal](https://portal.azure.com)
2. Navigate to **Azure Active Directory** → **App registrations**
3. Click **New registration**
4. Fill in the details:
   - **Name**: `Goodwill Donor App`
   - **Supported account types**: Accounts in this organizational directory only
   - **Redirect URI**: Leave blank
5. Click **Register**

## Step 2: Note Your Application Details

After registration, you'll see:
- **Application (client) ID** - Copy this
- **Directory (tenant) ID** - Copy this

## Step 3: Create a Client Secret

1. In your app registration, go to **Certificates & secrets**
2. Click **New client secret**
3. Add a description: `Donor App Secret`
4. Choose expiration: 24 months (or as per your policy)
5. Click **Add**
6. **IMPORTANT**: Copy the **Value** immediately (you won't see it again!)

## Step 4: Grant API Permissions

1. In your app registration, go to **API permissions**
2. Click **Add a permission**
3. Select **Microsoft Graph**
4. Choose **Application permissions** (not Delegated)
5. Search and add these permissions:
   - `Mail.Send`
6. Click **Add permissions**
7. Click **Grant admin consent for [Your Organization]** (requires admin)
8. Confirm the consent

## Step 5: Update config.py

Edit `config.py` and add your values:

```python
GRAPH_CONFIG = {
    'tenant_id': 'your-tenant-id-here',           # From Step 2
    'client_id': 'your-client-id-here',           # From Step 2
    'client_secret': 'your-client-secret-here',   # From Step 3
    'sender_email': 'gw-appdev@GoodwillMiami.org'
}
```

## Step 6: Test the Configuration

Run the app and test:

```bash
python app.py
```

Then submit a test donation or use the test endpoint.

## For Azure App Service Deployment

Instead of putting credentials in `config.py`, use environment variables:

In Azure Portal → App Service → Configuration → Application Settings:

```
AZURE_TENANT_ID = your-tenant-id
AZURE_CLIENT_ID = your-client-id
AZURE_CLIENT_SECRET = your-client-secret
SENDER_EMAIL = gw-appdev@GoodwillMiami.org
```

## Troubleshooting

### Error: "Insufficient privileges to complete the operation"
- Make sure you granted **Application permissions** (not Delegated)
- Ensure admin consent was granted
- Wait a few minutes for permissions to propagate

### Error: "AADSTS700016: Application not found"
- Check that tenant_id and client_id are correct
- Ensure the app registration exists in your Azure AD

### Error: "Invalid client secret"
- The client secret may have expired
- Create a new secret and update config.py

### Error: "The user or administrator has not consented"
- Admin consent is required for Mail.Send permission
- Ask your Azure AD admin to grant consent

## Security Best Practices

1. **Never commit secrets to Git**
   - Use environment variables in production
   - Keep config.py in .gitignore

2. **Rotate secrets regularly**
   - Set expiration on client secrets
   - Update before expiration

3. **Use least privilege**
   - Only grant Mail.Send permission
   - Don't grant unnecessary permissions

4. **Monitor usage**
   - Check Azure AD sign-in logs
   - Monitor for unusual activity

## Permissions Explained

- **Mail.Send**: Allows the app to send mail as any user without a signed-in user
  - This is an Application permission (app acts on its own)
  - Requires admin consent
  - More secure than storing passwords

## Additional Resources

- [Microsoft Graph API Documentation](https://docs.microsoft.com/en-us/graph/api/user-sendmail)
- [App Registration Guide](https://docs.microsoft.com/en-us/azure/active-directory/develop/quickstart-register-app)
- [Application Permissions](https://docs.microsoft.com/en-us/graph/permissions-reference)
