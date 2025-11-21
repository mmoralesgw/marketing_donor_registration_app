# Email Mode Configuration Guide

The donor app now supports **two email sending methods** that you can easily switch between in `config.py`.

## Quick Switch

Edit `config.py` and change the `EMAIL_MODE`:

```python
EMAIL_MODE = 'smtp'       # Use Gmail/Google Workspace
# or
EMAIL_MODE = 'microsoft'  # Use Microsoft Graph API
```

---

## Option 1: SMTP Mode (Gmail/Google Workspace)

**Best for:** Gmail accounts, Google Workspace accounts

### Configuration

```python
EMAIL_MODE = 'smtp'

EMAIL_CONFIG = {
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587,
    'sender_email': 'marketing@Goodwillsouthflorida.org',
    'sender_password': 'your-app-password'
}
```

### Setup Steps

1. **Enable 2-Factor Authentication**
   - Go to: https://myaccount.google.com/security
   - Enable 2-Step Verification

2. **Generate App Password**
   - Go to: https://myaccount.google.com/apppasswords
   - Select: Mail → Other (Custom name) → "Donor App"
   - Copy the 16-character password (remove spaces)

3. **Update config.py**
   - Paste the app password in `sender_password`

4. **Test**
   ```bash
   python app.py
   ```

### Pros
- ✅ Simple setup (5 minutes)
- ✅ No Azure AD registration needed
- ✅ Works with any Gmail account
- ✅ 500 emails/day (free Gmail) or 2,000/day (Google Workspace)

### Cons
- ❌ Requires App Password management
- ❌ Lower sending limits than Graph API

---

## Option 2: Microsoft Mode (Graph API)

**Best for:** Microsoft 365/Office 365 accounts

### Configuration

```python
EMAIL_MODE = 'microsoft'

GRAPH_CONFIG = {
    'tenant_id': 'your-tenant-id',
    'client_id': 'your-client-id',
    'client_secret': 'your-client-secret',
    'sender_email': 'gw-appdev@GoodwillMiami.org'
}
```

### Setup Steps

1. **Register Azure AD App**
   - Go to: https://portal.azure.com
   - Azure Active Directory → App registrations
   - Create new registration
   - Copy: Tenant ID, Client ID

2. **Create Client Secret**
   - Certificates & secrets → New client secret
   - Copy the secret value

3. **Grant Permissions**
   - API permissions → Add permission
   - Microsoft Graph → Application permissions
   - Add: Mail.Send
   - Grant admin consent

4. **Update config.py**
   - Add your Tenant ID, Client ID, Client Secret
   - Set sender_email to an email that exists in your Azure AD

5. **Test**
   ```bash
   python app.py
   ```

### Pros
- ✅ More secure (OAuth2)
- ✅ Higher sending limits
- ✅ No password management
- ✅ Better for enterprise

### Cons
- ❌ Requires Azure AD setup (15 minutes)
- ❌ Requires admin consent
- ❌ Email must exist in Azure AD tenant

---

## Switching Between Modes

Just change one line in `config.py`:

```python
# Use Gmail
EMAIL_MODE = 'smtp'

# Use Microsoft
EMAIL_MODE = 'microsoft'
```

Both configurations can stay in the file - only the active mode will be used.

---

## For Azure Deployment

Set the environment variable:

```
EMAIL_MODE = smtp
```
or
```
EMAIL_MODE = microsoft
```

Then set the appropriate credentials:

**For SMTP:**
```
SMTP_SERVER = smtp.gmail.com
SMTP_PORT = 587
SENDER_EMAIL = marketing@Goodwillsouthflorida.org
SENDER_PASSWORD = your-app-password
```

**For Microsoft:**
```
AZURE_TENANT_ID = your-tenant-id
AZURE_CLIENT_ID = your-client-id
AZURE_CLIENT_SECRET = your-client-secret
MS_SENDER_EMAIL = gw-appdev@GoodwillMiami.org
```

---

## Verification

When you start the app, you'll see which mode is active:

```
==================================================
Starting Donor Management Server...
Server running on http://localhost:5000
==================================================

📧 Email Mode: SMTP
   Sender: marketing@Goodwillsouthflorida.org
   Method: SMTP
==================================================
```

or

```
📧 Email Mode: MICROSOFT
   Sender: gw-appdev@GoodwillMiami.org
   Method: Microsoft Graph API
```

---

## Troubleshooting

### SMTP Mode Issues
- **"Username and Password not accepted"**
  → Use App Password, not regular password
  
- **"2FA not enabled"**
  → Enable at: https://myaccount.google.com/security

### Microsoft Mode Issues
- **"Insufficient privileges"**
  → Grant Mail.Send permission with admin consent
  
- **"User not found"**
  → Email must exist in your Azure AD tenant

---

## Recommendation

- **Use SMTP** if you have a Gmail/Google Workspace account
- **Use Microsoft** if you have Microsoft 365 and want enterprise features

Both work great - choose what's easier for your setup!
