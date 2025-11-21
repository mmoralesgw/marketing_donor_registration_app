# Microsoft Graph API - Quick Reference

## What You Need

From your Azure AD App Registration, you need 3 values:

1. **Tenant ID** (Directory ID)
2. **Client ID** (Application ID)  
3. **Client Secret** (Secret Value)

## Where to Find Them

### Azure Portal → Azure Active Directory → App registrations → Your App

- **Tenant ID**: Overview page → Directory (tenant) ID
- **Client ID**: Overview page → Application (client) ID
- **Client Secret**: Certificates & secrets → Client secrets → Value

## Update config.py

```python
GRAPH_CONFIG = {
    'tenant_id': 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx',
    'client_id': 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx',
    'client_secret': 'your~secret~value~here',
    'sender_email': 'gw-appdev@GoodwillMiami.org'
}
```

## Required Permission

- **Mail.Send** (Application permission)
- Requires admin consent

## Common Issues

| Error | Solution |
|-------|----------|
| "Insufficient privileges" | Grant admin consent for Mail.Send |
| "Invalid client secret" | Create new secret, update config |
| "Application not found" | Check tenant_id and client_id |
| "Tenant not found" | Verify tenant_id is correct |

## Test Your Setup

```bash
python app.py
```

Submit a test donation and check if email is received.

## For Azure Deployment

Use environment variables instead of config.py:

```
AZURE_TENANT_ID
AZURE_CLIENT_ID
AZURE_CLIENT_SECRET
SENDER_EMAIL
```

## Need Help?

See detailed guide: `GRAPH_API_SETUP.md`
