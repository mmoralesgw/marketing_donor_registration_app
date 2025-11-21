# ============================================
# EMAIL MODE CONFIGURATION
# ============================================
# Choose email sending method: 'smtp' or 'microsoft'
EMAIL_MODE = 'smtp'  # Change to 'microsoft' to use Graph API

# ============================================
# SMTP CONFIGURATION (Gmail/Google Workspace)
# ============================================
# Used when EMAIL_MODE = 'smtp'
EMAIL_CONFIG = {
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587,
    'sender_email': 'your-email@yourdomain.org',
    'sender_password': 'your-app-password-here'  # Gmail App Password (16 characters)
}

# To get Gmail App Password:
# 1. Enable 2FA: https://myaccount.google.com/security
# 2. Generate App Password: https://myaccount.google.com/apppasswords
# 3. Select: Mail -> Other (Custom name) -> "Donor App"
# 4. Copy the 16-character password (remove spaces)

# ============================================
# MICROSOFT GRAPH API CONFIGURATION
# ============================================
# Used when EMAIL_MODE = 'microsoft'
GRAPH_CONFIG = {
    'tenant_id': 'your-tenant-id-here',
    'client_id': 'your-client-id-here',
    'client_secret': 'your-client-secret-here',
    'sender_email': 'your-email@yourdomain.org'
}

# Organization Details (for PDF receipt)
ORGANIZATION_INFO = {
    'name': 'Your Organization Name',
    'address': '123 Main Street, City, State ZIP',
    'tax_id': 'XX-XXXXXXX',  # Update with actual Tax ID
    'phone': '(555) 123-4567',  # Update with actual phone
    'email': 'info@yourorganization.org'
}

# CSV File Settings
CSV_FILE = 'donors.csv'

# Flask Settings
DEBUG = True
PORT = 5000
