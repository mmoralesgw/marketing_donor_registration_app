"""
Alternative version using Microsoft Graph API for email sending
Use this if SMTP authentication is blocked by your organization
"""

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import csv
import os
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
import io
import requests
import base64

# Import configuration
try:
    from config import ORGANIZATION_INFO, CSV_FILE, DEBUG, PORT
except ImportError:
    ORGANIZATION_INFO = {
        'name': 'Goodwill Miami',
        'address': '2121 NW 21st Street, Miami, FL 33142',
        'tax_id': 'XX-XXXXXXX',
        'phone': '(305) xxx-xxxx',
        'email': 'gw-appdev@GoodwillMiami.org'
    }
    CSV_FILE = 'donors.csv'
    DEBUG = True
    PORT = 5000

# Microsoft Graph API Configuration
GRAPH_CONFIG = {
    'tenant_id': os.getenv('AZURE_TENANT_ID', 'your-tenant-id'),
    'client_id': os.getenv('AZURE_CLIENT_ID', 'your-client-id'),
    'client_secret': os.getenv('AZURE_CLIENT_SECRET', 'your-client-secret'),
    'sender_email': os.getenv('SENDER_EMAIL', 'gw-appdev@GoodwillMiami.org')
}

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

def get_access_token():
    """Get access token for Microsoft Graph API"""
    url = f"https://login.microsoftonline.com/{GRAPH_CONFIG['tenant_id']}/oauth2/v2.0/token"
    
    data = {
        'client_id': GRAPH_CONFIG['client_id'],
        'client_secret': GRAPH_CONFIG['client_secret'],
        'scope': 'https://graph.microsoft.com/.default',
        'grant_type': 'client_credentials'
    }
    
    response = requests.post(url, data=data)
    if response.status_code == 200:
        return response.json()['access_token']
    else:
        raise Exception(f"Failed to get access token: {response.text}")

def send_email_graph(to_email, subject, body, pdf_bytes):
    """Send email using Microsoft Graph API"""
    try:
        token = get_access_token()
        
        # Encode PDF as base64
        pdf_base64 = base64.b64encode(pdf_bytes).decode('utf-8')
        
        # Create email message
        message = {
            "message": {
                "subject": subject,
                "body": {
                    "contentType": "Text",
                    "content": body
                },
                "toRecipients": [
                    {
                        "emailAddress": {
                            "address": to_email
                        }
                    }
                ],
                "attachments": [
                    {
                        "@odata.type": "#microsoft.graph.fileAttachment",
                        "name": f"donation_receipt_{datetime.now().strftime('%Y%m%d')}.pdf",
                        "contentType": "application/pdf",
                        "contentBytes": pdf_base64
                    }
                ]
            }
        }
        
        # Send email
        url = f"https://graph.microsoft.com/v1.0/users/{GRAPH_CONFIG['sender_email']}/sendMail"
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        
        response = requests.post(url, json=message, headers=headers)
        
        if response.status_code == 202:
            return True
        else:
            print(f"Email error: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"Email error: {str(e)}")
        return False

# ... (rest of the functions remain the same)

print("""
==========================================================
Microsoft Graph API Email Configuration Required
==========================================================
This version uses Microsoft Graph API instead of SMTP.

To configure:
1. Register an app in Azure AD
2. Grant Mail.Send permission
3. Set environment variables:
   - AZURE_TENANT_ID
   - AZURE_CLIENT_ID
   - AZURE_CLIENT_SECRET
   - SENDER_EMAIL

See: https://docs.microsoft.com/en-us/graph/auth-v2-service
==========================================================
""")
