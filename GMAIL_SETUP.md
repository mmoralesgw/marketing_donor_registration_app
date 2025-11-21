# Gmail Setup Guide for Donor App

The app now uses Gmail SMTP to send emails. This is simpler and works great for no-reply accounts.

## Step 1: Prepare Your Gmail Account

You can use:
- A dedicated no-reply Gmail account (recommended)
- Your existing Gmail account
- A Google Workspace account

**Example:** `noreply.goodwill@gmail.com`

## Step 2: Enable 2-Factor Authentication

1. Go to [Google Account Security](https://myaccount.google.com/security)
2. Sign in with your Gmail account
3. Under "Signing in to Google", click **2-Step Verification**
4. Follow the prompts to enable 2FA (required for App Passwords)

## Step 3: Generate an App Password

1. Go to [App Passwords](https://myaccount.google.com/apppasswords)
2. Sign in if prompted
3. Under "Select app", choose **Mail**
4. Under "Select device", choose **Other (Custom name)**
5. Enter: `Donor App`
6. Click **Generate**
7. **Copy the 16-character password** (it looks like: `abcd efgh ijkl mnop`)
8. **Important:** Remove the spaces when copying

## Step 4: Update config.py

Edit `config.py` and add your credentials:

```python
EMAIL_CONFIG = {
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587,
    'sender_email': 'noreply.goodwill@gmail.com',  # Your Gmail address
    'sender_password': 'abcdefghijklmnop'  # App Password (no spaces)
}
```

## Step 5: Test It

Run the app and submit a test donation:

```bash
python app.py
```

Open `index.html` in your browser and test the form.

## For Azure Deployment

Instead of putting credentials in `config.py`, use environment variables:

In Azure Portal → App Service → Configuration → Application Settings:

```
SMTP_SERVER = smtp.gmail.com
SMTP_PORT = 587
SENDER_EMAIL = noreply.goodwill@gmail.com
SENDER_PASSWORD = abcdefghijklmnop
```

## Troubleshooting

### Error: "Username and Password not accepted"
- Make sure you're using an **App Password**, not your regular Gmail password
- Verify 2-Factor Authentication is enabled
- Check that the App Password has no spaces

### Error: "SMTP AUTH extension not supported"
- Verify smtp_server is `smtp.gmail.com`
- Check smtp_port is `587`

### Error: "Connection refused"
- Check your internet connection
- Verify port 587 is not blocked by firewall

### Emails going to spam
- Add SPF record to your domain (if using custom domain)
- Warm up the email account by sending gradually
- Ask recipients to whitelist your email

## Gmail Sending Limits

- **Free Gmail:** 500 emails per day
- **Google Workspace:** 2,000 emails per day

If you need more, consider:
- SendGrid
- Amazon SES
- Mailgun

## Security Best Practices

1. **Use a dedicated no-reply account**
   - Don't use your personal Gmail
   - Create: `noreply.goodwill@gmail.com`

2. **Keep App Password secure**
   - Never commit to Git
   - Use environment variables in production
   - Rotate periodically

3. **Monitor usage**
   - Check Gmail sent folder
   - Watch for suspicious activity
   - Enable alerts

## Alternative: Google Workspace

If you have Google Workspace (paid):
- Same setup process
- Higher sending limits (2,000/day)
- Better deliverability
- Custom domain support

## Need Help?

- [Gmail SMTP Settings](https://support.google.com/mail/answer/7126229)
- [App Passwords Guide](https://support.google.com/accounts/answer/185833)
- [2-Step Verification](https://support.google.com/accounts/answer/185839)

## Quick Reference

```
SMTP Server: smtp.gmail.com
Port: 587
Security: STARTTLS
Authentication: App Password (not regular password)
```
