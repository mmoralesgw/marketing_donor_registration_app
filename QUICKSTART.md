# Quick Start Guide - Goodwill Miami Donor App

## Local Development (5 minutes)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Email (Gmail)
Edit `config.py` with your Gmail credentials:
```python
EMAIL_CONFIG = {
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587,
    'sender_email': 'noreply@yourdomain.com',
    'sender_password': 'your-app-password'  # 16-character App Password
}
```

**Need an App Password?** See `GMAIL_SETUP.md` for step-by-step instructions.

### 3. Start the Server
```bash
python app.py
```

### 4. Open the App
Open `index.html` in your browser or visit `http://localhost:5000`

### 5. Test It
- Fill out the form
- Submit a donation
- Check if email was received
- Click "Download All Donors (CSV)" to see the data

---

## Azure Deployment (15 minutes)

### Option 1: Automated Script (Easiest)

**Windows:**
```powershell
.\deploy.ps1
```

**Linux/Mac:**
```bash
chmod +x deploy.sh
./deploy.sh
```

Then configure environment variables in Azure Portal.

### Option 2: Azure Portal (Step-by-step)

1. **Create Web App**
   - Go to [Azure Portal](https://portal.azure.com)
   - Create Resource → Web App
   - Name: `goodwill-donor-app`
   - Runtime: Python 3.11
   - Region: East US (or closest)
   - Plan: B1 Basic or higher

2. **Configure Settings**
   - Go to Configuration → Application Settings
   - Add these variables:
     ```
     SMTP_SERVER = smtp.office365.com
     SMTP_PORT = 587
     SENDER_EMAIL = gw-appdev@GoodwillMiami.org
     SENDER_PASSWORD = [your-password]
     ORG_NAME = Goodwill Miami
     ORG_ADDRESS = 2121 NW 21st Street, Miami, FL 33142
     ORG_TAX_ID = [your-tax-id]
     ORG_PHONE = [your-phone]
     ORG_EMAIL = gw-appdev@GoodwillMiami.org
     ```

3. **Set Startup Command**
   - Configuration → General Settings
   - Startup Command: `gunicorn --bind=0.0.0.0 --timeout 600 app:app`

4. **Deploy Code**
   - Deployment Center → Choose source (GitHub, Local Git, or ZIP)
   - Follow prompts to deploy

5. **Test**
   - Visit: `https://goodwill-donor-app.azurewebsites.net`

---

## Testing Your Deployment

Run the test script:
```bash
# For local testing
python test_app.py

# For Azure testing (update BASE_URL in test_app.py first)
python test_app.py
```

---

## Troubleshooting

### Email Not Sending
- ✓ Verify Gmail credentials in config.py
- ✓ Ensure you're using an App Password (not regular password)
- ✓ Check that 2-Factor Authentication is enabled on Gmail
- ✓ See `GMAIL_SETUP.md` for detailed setup

### App Won't Start on Azure
- ✓ Check logs in Azure Portal → Log Stream
- ✓ Verify startup command is set correctly
- ✓ Ensure all environment variables are configured

### CSV Not Downloading
- ✓ Submit at least one donation first
- ✓ Check browser console for errors
- ✓ Verify API URL is correct

---

## File Structure

```
donor-app/
├── index.html              # Frontend web interface
├── app.py                  # Python Flask backend
├── config.py              # Local configuration
├── requirements.txt       # Python dependencies
├── startup.txt           # Azure startup command
├── deploy.ps1            # Windows deployment script
├── deploy.sh             # Linux/Mac deployment script
├── deploy-azure.md       # Detailed Azure guide
├── test_app.py           # Testing script
└── donors.csv            # Generated donor database
```

---

## Next Steps

1. **Customize Organization Info**
   - Update tax ID, phone, and address in config.py or Azure settings

2. **Set Up Custom Domain** (Optional)
   - Configure custom domain in Azure
   - Add SSL certificate

3. **Enable Monitoring**
   - Set up Application Insights
   - Configure alerts

4. **Backup Strategy**
   - Consider Azure Blob Storage for CSV persistence
   - Set up automated backups

---

## Support

For detailed documentation:
- Local setup: See `README.md`
- Azure deployment: See `deploy-azure.md`

For issues:
- Check Azure logs
- Review error messages
- Verify all configuration settings
