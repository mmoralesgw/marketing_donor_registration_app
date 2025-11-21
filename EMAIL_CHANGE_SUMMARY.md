# Email System Changed to Gmail SMTP ✅

## What Changed

The app now uses **Gmail SMTP** instead of Microsoft Graph API for sending emails.

### Why This Change?
- ✅ Simpler setup (no Azure AD registration needed)
- ✅ Works with any Gmail account
- ✅ Perfect for no-reply accounts
- ✅ Easier to configure and test
- ✅ No admin consent required

---

## Quick Setup (5 Minutes)

### 1. Get a Gmail Account
Use a dedicated no-reply account:
- Example: `noreply.goodwill@gmail.com`
- Or use existing Gmail account

### 2. Enable 2-Factor Authentication
- Go to: https://myaccount.google.com/security
- Enable 2-Step Verification

### 3. Generate App Password
- Go to: https://myaccount.google.com/apppasswords
- Select: Mail → Other (Custom name) → "Donor App"
- Copy the 16-character password (remove spaces)

### 4. Update config.py

```python
EMAIL_CONFIG = {
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587,
    'sender_email': 'noreply.goodwill@gmail.com',  # Your Gmail
    'sender_password': 'abcdefghijklmnop'  # App Password (no spaces)
}
```

### 5. Test It

```bash
python app.py
```

Open `index.html` and submit a test donation!

---

## For Azure Deployment

Set these environment variables in Azure Portal:

```
SMTP_SERVER = smtp.gmail.com
SMTP_PORT = 587
SENDER_EMAIL = noreply.goodwill@gmail.com
SENDER_PASSWORD = your-app-password
```

---

## What Was Removed

- ❌ Microsoft Graph API integration
- ❌ Azure AD app registration requirement
- ❌ OAuth2 token management
- ❌ Admin consent requirement
- ❌ Complex permission setup

## What Was Added

- ✅ Simple SMTP email sending
- ✅ Gmail App Password authentication
- ✅ Easier configuration
- ✅ Faster setup

---

## Files Updated

- `app.py` - Changed to SMTP email sending
- `config.py` - Updated with Gmail settings
- `config.example.py` - Gmail template
- `GMAIL_SETUP.md` - New setup guide
- `README.md` - Updated documentation
- `QUICKSTART.md` - Updated quick start
- `deploy-azure.md` - Updated Azure guide

---

## Gmail Limits

- **Free Gmail:** 500 emails/day
- **Google Workspace:** 2,000 emails/day

This should be plenty for most donation tracking needs!

---

## Troubleshooting

### "Username and Password not accepted"
→ Use App Password, not regular password

### "2FA not enabled"
→ Enable at: https://myaccount.google.com/security

### "Connection refused"
→ Check firewall, verify port 587

---

## Documentation

- **Setup Guide:** `GMAIL_SETUP.md`
- **Quick Start:** `QUICKSTART.md`
- **Main Docs:** `README.md`

---

## Ready to Deploy! 🚀

The app is now simpler and ready for both local testing and Azure deployment.

**Next Steps:**
1. Set up Gmail App Password
2. Update config.py
3. Test locally
4. Deploy to Azure

---

**Status:** ✅ READY
**Email System:** Gmail SMTP
**Setup Time:** ~5 minutes
