# Donor Management System

A complete web application for managing donor information, generating PDF receipts, and sending email confirmations.

## Features

- ✅ Collect donor information (name, email, phone, address)
- ✅ Record donation type (Cash or Merchandise)
- ✅ Track merchandise categories (Clothing, Books, Shoes, Toys, etc.)
- ✅ Save all donations to CSV file
- ✅ Generate PDF receipts automatically
- ✅ Send receipts via email to donors
- ✅ Download complete donor database as CSV

## Setup Instructions

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Email Settings (Gmail SMTP)

This app uses Gmail SMTP for sending emails.

**Quick Setup:**
1. Enable 2-Factor Authentication on your Gmail account
2. Generate an App Password at: https://myaccount.google.com/apppasswords
3. Update `config.py` with your credentials

**Detailed instructions:** See `GMAIL_SETUP.md`

```python
EMAIL_CONFIG = {
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587,
    'sender_email': 'noreply@yourdomain.com',
    'sender_password': 'your-app-password'
}
```

### 3. Update Organization Information

Edit `config.py` to customize your organization details for PDF receipts:

```python
ORGANIZATION_INFO = {
    'name': 'Your Organization Name',
    'address': '123 Main Street, City, State ZIP',
    'tax_id': 'XX-XXXXXXX',
    'phone': '(555) 123-4567',
    'email': 'info@yourorganization.org'
}
```

### 4. Start the Server

```bash
python app.py
```

The server will start on `http://localhost:5000`

### 5. Open the Web App

Open `index.html` in your web browser. The form will automatically connect to the Python backend.

## Usage

1. **Submit a Donation**:
   - Fill in donor information
   - Select donation type (Cash or Merchandise)
   - If merchandise, select item categories
   - Enter donation date and location
   - Click "Submit Donation"

2. **Automatic Actions**:
   - Data saved to `donors.csv`
   - PDF receipt generated
   - Email sent to donor with receipt attached

3. **Download All Data**:
   - Click "Download All Donors (CSV)" button
   - Opens the complete donor database

## File Structure

```
donor-app/
├── index.html          # Frontend web interface
├── app.py             # Python Flask backend
├── config.py          # Configuration file
├── requirements.txt   # Python dependencies
├── donors.csv         # Donor database (auto-generated)
└── README.md          # This file
```

## API Endpoints

- `POST /api/submit-donation` - Submit new donation
- `GET /api/download-csv` - Download donors CSV
- `POST /api/test-email` - Test email configuration

## Troubleshooting

### Email Not Sending
- Verify Gmail credentials in `config.py`
- Ensure you're using an App Password (not regular password)
- Check that 2-Factor Authentication is enabled
- Verify smtp_server and smtp_port are correct
- See `GMAIL_SETUP.md` for detailed troubleshooting

### Server Connection Error
- Make sure Python backend is running (`python app.py`)
- Check that port 5000 is not in use
- Verify the API_URL in `index.html` matches your server address

### CSV Not Saving
- Check file permissions in the application directory
- Ensure the Python process has write access

## Security Notes

- Never commit `config.py` with real credentials to version control
- Use environment variables for production deployments
- Keep your App Password secure
- Consider using HTTPS in production

## Azure Deployment

This app is ready for Azure App Service deployment. See `deploy-azure.md` for detailed instructions.

### Quick Deploy to Azure:

**Windows:**
```powershell
.\deploy.ps1
```

**Linux/Mac:**
```bash
chmod +x deploy.sh
./deploy.sh
```

Or deploy manually through Azure Portal - see `deploy-azure.md` for step-by-step guide.

### Environment Variables for Azure

Set these in Azure Portal → App Service → Configuration → Application Settings:

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

## License

Free to use for non-profit organizations.
