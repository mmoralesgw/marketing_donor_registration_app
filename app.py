from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import csv
import json
import os
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import io
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import requests
import base64
import urllib3

# Suppress SSL warnings when verify_ssl is disabled (for local testing)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Import configuration
try:
    from config import ORGANIZATION_INFO, CSV_FILE
    # Try to import DEBUG and PORT from config, with fallbacks
    try:
        from config import DEBUG, PORT
    except ImportError:
        DEBUG = False
        PORT = int(os.getenv('PORT', 5000))
    # Try to import EMAIL_CONFIG and GRAPH_CONFIG from config.py (for local development)
    try:
        from config import EMAIL_CONFIG as LOCAL_EMAIL_CONFIG
    except ImportError:
        LOCAL_EMAIL_CONFIG = None
    try:
        from config import GRAPH_CONFIG as LOCAL_GRAPH_CONFIG
    except ImportError:
        LOCAL_GRAPH_CONFIG = None
    try:
        from config import EMAIL_MODE as LOCAL_EMAIL_MODE
    except ImportError:
        LOCAL_EMAIL_MODE = 'smtp'
    try:
        from config import BLOOMERANG_CONFIG as LOCAL_BLOOMERANG_CONFIG
    except ImportError:
        LOCAL_BLOOMERANG_CONFIG = None
except ImportError:
    # Default configuration if config.py doesn't exist
    ORGANIZATION_INFO = {
        'name': 'Your Organization Name',
        'address': '123 Main Street, City, State ZIP',
        'tax_id': 'XX-XXXXXXX',
        'phone': '(555) 123-4567',
        'email': 'info@yourorganization.org'
    }
    CSV_FILE = 'donors.csv'
    LOCAL_EMAIL_CONFIG = None
    LOCAL_GRAPH_CONFIG = None
    LOCAL_EMAIL_MODE = 'smtp'
    LOCAL_BLOOMERANG_CONFIG = None

# Set PORT and DEBUG with environment variable support
PORT = int(os.getenv('PORT', PORT if 'PORT' in locals() else 5000))
DEBUG = os.getenv('DEBUG', str(DEBUG if 'DEBUG' in locals() else False)).lower() == 'true'

# Email Mode Configuration
# Options: 'smtp' (Gmail/Google Workspace) or 'microsoft' (Graph API)
EMAIL_MODE = os.getenv('EMAIL_MODE', LOCAL_EMAIL_MODE).lower()

# SMTP Configuration (for Gmail/Google Workspace)
if LOCAL_EMAIL_CONFIG:
    EMAIL_CONFIG = {
        'smtp_server': os.getenv('SMTP_SERVER', LOCAL_EMAIL_CONFIG.get('smtp_server', 'smtp.gmail.com')),
        'smtp_port': int(os.getenv('SMTP_PORT', LOCAL_EMAIL_CONFIG.get('smtp_port', 587))),
        'sender_email': os.getenv('SENDER_EMAIL', LOCAL_EMAIL_CONFIG.get('sender_email', '')),
        'sender_password': os.getenv('SENDER_PASSWORD', LOCAL_EMAIL_CONFIG.get('sender_password', ''))
    }
else:
    EMAIL_CONFIG = {
        'smtp_server': os.getenv('SMTP_SERVER', 'smtp.gmail.com'),
        'smtp_port': int(os.getenv('SMTP_PORT', 587)),
        'sender_email': os.getenv('SENDER_EMAIL', ''),
        'sender_password': os.getenv('SENDER_PASSWORD', '')
    }

# Microsoft Graph API Configuration
if LOCAL_GRAPH_CONFIG:
    GRAPH_CONFIG = {
        'tenant_id': os.getenv('AZURE_TENANT_ID', LOCAL_GRAPH_CONFIG.get('tenant_id', '')),
        'client_id': os.getenv('AZURE_CLIENT_ID', LOCAL_GRAPH_CONFIG.get('client_id', '')),
        'client_secret': os.getenv('AZURE_CLIENT_SECRET', LOCAL_GRAPH_CONFIG.get('client_secret', '')),
        'sender_email': os.getenv('MS_SENDER_EMAIL', LOCAL_GRAPH_CONFIG.get('sender_email', ''))
    }
else:
    GRAPH_CONFIG = {
        'tenant_id': os.getenv('AZURE_TENANT_ID', ''),
        'client_id': os.getenv('AZURE_CLIENT_ID', ''),
        'client_secret': os.getenv('AZURE_CLIENT_SECRET', ''),
        'sender_email': os.getenv('MS_SENDER_EMAIL', '')
    }

# Bloomerang CRM Configuration
if LOCAL_BLOOMERANG_CONFIG:
    BLOOMERANG_CONFIG = {
        'enabled': LOCAL_BLOOMERANG_CONFIG.get('enabled', False),
        'api_key': os.getenv('BLOOMERANG_API_KEY', LOCAL_BLOOMERANG_CONFIG.get('api_key', '')),
        'api_url': os.getenv('BLOOMERANG_API_URL', LOCAL_BLOOMERANG_CONFIG.get('api_url', 'https://api.bloomerang.co/v2')),
        'verify_ssl': LOCAL_BLOOMERANG_CONFIG.get('verify_ssl', True)
    }
else:
    BLOOMERANG_CONFIG = {
        'enabled': os.getenv('BLOOMERANG_ENABLED', 'false').lower() == 'true',
        'api_key': os.getenv('BLOOMERANG_API_KEY', ''),
        'api_url': os.getenv('BLOOMERANG_API_URL', 'https://api.bloomerang.co/v2'),
        'verify_ssl': os.getenv('BLOOMERANG_VERIFY_SSL', 'true').lower() == 'true'
    }

# Override organization info with environment variables for Azure App Service
ORGANIZATION_INFO['name'] = os.getenv('ORG_NAME', ORGANIZATION_INFO.get('name', ''))
ORGANIZATION_INFO['address'] = os.getenv('ORG_ADDRESS', ORGANIZATION_INFO.get('address', ''))
ORGANIZATION_INFO['tax_id'] = os.getenv('ORG_TAX_ID', ORGANIZATION_INFO.get('tax_id', ''))
ORGANIZATION_INFO['phone'] = os.getenv('ORG_PHONE', ORGANIZATION_INFO.get('phone', ''))
ORGANIZATION_INFO['email'] = os.getenv('ORG_EMAIL', ORGANIZATION_INFO.get('email', ''))

app = Flask(__name__)
CORS(app)

def init_csv():
    """Initialize CSV file with headers if it doesn't exist"""
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                'Date Recorded', 'First Name', 'Last Name', 'Email', 
                'Phone', 'Address', 'Donation Type', 'Merchandise Items',
                'Donation Date', 'Location'
            ])

def save_to_csv(data):
    """Save donor data to CSV file"""
    with open(CSV_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        merchandise = ', '.join(data.get('merchandiseItems', [])) if data.get('merchandiseItems') else 'N/A'
        writer.writerow([
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            data['firstName'],
            data['lastName'],
            data['email'],
            data['phone'],
            data['address'],
            data['donationType'],
            merchandise,
            data['donationDate'],
            data['location']
        ])

def send_to_bloomerang(data):
    """Send donor data to Bloomerang CRM"""
    if not BLOOMERANG_CONFIG.get('enabled'):
        print("Bloomerang integration is disabled")
        return {'success': False, 'message': 'Bloomerang integration disabled'}
    
    if not BLOOMERANG_CONFIG.get('api_key'):
        print("Bloomerang API key not configured")
        return {'success': False, 'message': 'Bloomerang API key not configured'}
    
    try:
        # Prepare constituent data for Bloomerang
        # Prepare constituent data for Bloomerang
        # Note: Email and Phone need to be in specific format for Bloomerang API
        constituent_data = {
            'Type': 'Individual',
            'Status': 'Active',
            'FirstName': data['firstName'],
            'LastName': data['lastName'],
            'PrimaryEmail': {
                'Type': 'Home',
                'Value': data['email']
            },
            'PrimaryPhone': {
                'Type': 'Mobile',
                'Number': data['phone']
            }
        }
        
        # Add address only if provided
        if data.get('address') and data['address'].strip():
            constituent_data['PrimaryAddress'] = {
                'Street': data['address'],
                'Type': 'Home'
            }
        
        # Check if constituent already exists
        headers = {
            'X-API-Key': BLOOMERANG_CONFIG['api_key'],
            'Content-Type': 'application/json'
        }
        
        # Search for constituent by email
        # Note: Bloomerang API limits to 50 results per request, so we paginate
        search_url = f"{BLOOMERANG_CONFIG['api_url']}/constituents"
        
        constituent_id = None
        matching_constituent = None
        max_pages = 10  # Search up to 500 constituents (10 pages x 50)
        
        for page in range(max_pages):
            search_params = {
                'skip': page * 50,
                'take': 50,  # Maximum allowed by Bloomerang
                'orderBy': 'Id',
                'orderDirection': 'Desc'
            }
            
            search_response = requests.get(search_url, headers=headers, params=search_params, verify=BLOOMERANG_CONFIG.get('verify_ssl', True))
            
            if search_response.status_code == 200:
                results = search_response.json()['Results']
                
                # If no results, we've reached the end
                if not results or len(results) == 0:
                    break
                
                # Normalize donor data for comparison
                donor_email = data['email'].lower().strip() if data.get('email') else ''
                donor_phone = ''.join(filter(str.isdigit, data.get('phone', '')))  # Remove formatting
                donor_first = data['firstName'].lower().strip()
                donor_last = data['lastName'].lower().strip()
                
                # Filter results using multiple identifiers
                for constituent in results:
                    match_score = 0
                    match_details = []
                    
                    # Check email match (highest priority)
                    # Bloomerang stores email in PrimaryEmail object
                    constituent_email = ''
                    primary_email_obj = constituent.get('PrimaryEmail', {})
                    if isinstance(primary_email_obj, dict):
                        constituent_email = primary_email_obj.get('Value', '')
                    
                    # Also check EmailAddress field (some API versions)
                    if not constituent_email:
                        constituent_email = constituent.get('EmailAddress', '')
                    
                    if constituent_email and donor_email:
                        if constituent_email.lower().strip() == donor_email:
                            match_score += 100  # Email match is strongest
                            match_details.append('email')
                    
                    # Check phone match
                    # Bloomerang stores phone in PrimaryPhone.Number
                    constituent_phone = ''
                    primary_phone_obj = constituent.get('PrimaryPhone', {})
                    if isinstance(primary_phone_obj, dict):
                        constituent_phone = primary_phone_obj.get('Number', '')
                    
                    # Also check PhoneNumber field (some API versions)
                    if not constituent_phone:
                        constituent_phone = constituent.get('PhoneNumber', '')
                    
                    if constituent_phone and donor_phone:
                        # Normalize phone (remove formatting)
                        normalized_phone = ''.join(filter(str.isdigit, constituent_phone))
                        if normalized_phone == donor_phone and len(donor_phone) >= 10:
                            match_score += 50  # Phone match is good
                            match_details.append('phone')
                    
                    # Check name match
                    constituent_first = (constituent.get('FirstName', '') or '').lower().strip()
                    constituent_last = (constituent.get('LastName', '') or '').lower().strip()
                    
                    if constituent_first == donor_first and constituent_last == donor_last:
                        match_score += 30  # Name match
                        match_details.append('name')
                    
                    # Strong match: Email OR (Phone + Name)
                    if match_score >= 80:
                        matching_constituent = constituent
                        match_info = ' + '.join(match_details)
                        print(f"Match found (score: {match_score}, matched: {match_info}): {constituent.get('FullName', 'Unknown')}")
                        break
                
                # If we found a match, stop searching
                if matching_constituent:
                    break
            else:
                print(f"Search page {page} failed: {search_response.status_code}")
                break
        
        if matching_constituent:
            # Constituent exists, use existing ID
            constituent_id = matching_constituent.get('Id')
            print(f"Found existing constituent: {constituent_id} ({matching_constituent.get('FullName', 'Unknown')})")
            return {
                    'success': True,
                    'constituent_id': constituent_id,
                    'transaction_id': 0,
                    'message': f"Found existing constituent"
                }
        else:
            # Not found, create new constituent
            print(f"No matching constituent found for {data['email']}, creating new...")
            # Note: Bloomerang uses singular 'constituent' for POST
            create_url = f"{BLOOMERANG_CONFIG['api_url']}/constituent"
            create_response = requests.post(create_url, headers=headers, json=constituent_data, verify=BLOOMERANG_CONFIG.get('verify_ssl', True))
            
            if create_response.status_code in [200, 201]:
                result = create_response.json()
                constituent_id = result.get('Id')
                print(f"Created new constituent: {constituent_id}")
                return {
                    'success': True,
                    'constituent_id': constituent_id,
                    'transaction_id': 0,
                    'message': 'Successfully added to Bloomerang'
                }
            else:
                print(f"Failed to create constituent: {create_response.status_code} - {create_response.text}")
                return {'success': False, 'message': f'Failed to create constituent: {create_response.text}'}
        
        # Create transaction (donation record)
        # if constituent_id:
        #     transaction_data = {
        #         'ConstituentId': constituent_id,
        #         'Date': data['donationDate'],
        #         'Amount': 0,  # In-kind donation, no monetary value
        #         'Method': 'InKind',
        #         'Fund': 'General',
        #         'Note': f"Donation Type: {data['donationType']}\nLocation: {data['location']}"
        #     }
            
        #     # Add merchandise details if applicable
        #     if data['donationType'] == 'merchandise' and data.get('merchandiseItems'):
        #         transaction_data['Note'] += f"\nItems: {', '.join(data['merchandiseItems'])}"
            
        #     transaction_url = f"{BLOOMERANG_CONFIG['api_url']}/transactions"
        #     transaction_response = requests.post(transaction_url, headers=headers, json=transaction_data, verify=BLOOMERANG_CONFIG.get('verify_ssl', True))
            
        #     if transaction_response.status_code in [200, 201]:
        #         transaction_id = transaction_response.json().get('Id')
        #         print(f"Created transaction: {transaction_id}")
        #         return {
        #             'success': True,
        #             'constituent_id': constituent_id,
        #             'transaction_id': transaction_id,
        #             'message': 'Successfully added to Bloomerang'
        #         }
        #     else:
        #         print(f"Failed to create transaction: {transaction_response.status_code} - {transaction_response.text}")
        #         return {'success': False, 'message': f'Failed to create transaction: {transaction_response.text}'}
        
        # return {'success': False, 'message': 'Failed to get constituent ID'}
        
    except Exception as e:
        print(f"Bloomerang error: {str(e)}")
        return {'success': False, 'message': str(e)}

def generate_pdf_receipt(data):
    """Generate PDF receipt and return as bytes"""
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    
    # Header
    c.setFont("Helvetica-Bold", 20)
    c.drawString(1*inch, height - 0.8*inch, "This is your Tax Receipt")
    
    # Organization info
    c.setFont("Helvetica", 10)
    c.drawString(1*inch, height - 1.1*inch, "Goodwill Industries of South Florida, Inc.")
    c.drawString(1*inch, height - 1.3*inch, ORGANIZATION_INFO['address'])
    
    # Tax acknowledgment
    donation_date = datetime.strptime(data['donationDate'], '%Y-%m-%d').strftime('%m/%d/%Y')
    c.setFont("Helvetica", 11)
    y_position = height - 1.7*inch
    
    c.drawString(1*inch, y_position, f"Goodwill Industries of South Florida, Inc. acknowledges that a non-cash donation")
    y_position -= 0.2*inch
    c.drawString(1*inch, y_position, f"was received on {donation_date}.")
    y_position -= 0.3*inch
    
    # 501(c)(3) statement
    c.drawString(1*inch, y_position, "Goodwill Industries of South Florida, Inc is a 501(c)(3) non-profit organization.")
    y_position -= 0.2*inch
    c.drawString(1*inch, y_position, "Your donations are tax deductible to the fullest extent of the law.")
    y_position -= 0.2*inch
    c.drawString(1*inch, y_position, "No goods or services were provided in exchange for this donation.")
    y_position -= 0.4*inch
    
    # Itemized donations
    c.setFont("Helvetica-Bold", 11)
    c.drawString(1*inch, y_position, "For your records, below please find your itemized donation(s):")
    y_position -= 0.3*inch
    
    c.setFont("Helvetica", 11)
    if data['donationType'] == 'merchandise' and data.get('merchandiseItems'):
        for item in data['merchandiseItems']:
            c.drawString(1.2*inch, y_position, f"• {item}")
            y_position -= 0.2*inch
    else:
        c.drawString(1.2*inch, y_position, f"• {data['donationType'].capitalize()}")
        y_position -= 0.2*inch
    
    y_position -= 0.2*inch
    
    # IRS regulation notice
    c.setFont("Helvetica-Oblique", 10)
    c.drawString(1*inch, y_position, "IRS Regulations prohibit charitable organizations from establishing or affirming")
    y_position -= 0.2*inch
    c.drawString(1*inch, y_position, "the value of contributions.")
    y_position -= 0.5*inch
    
    # Donor Information section
    c.setFont("Helvetica-Bold", 12)
    c.drawString(1*inch, y_position, "Donor Information:")
    y_position -= 0.3*inch
    
    c.setFont("Helvetica", 10)
    donor_info = [
        f"Name: {data['firstName']} {data['lastName']}",
        f"Email: {data['email']}",
        f"Phone: {data['phone']}",
        f"Address: {data['address']}",
        f"Location: {data['location']}"
    ]
    
    for line in donor_info:
        c.drawString(1*inch, y_position, line)
        y_position -= 0.2*inch
    
    # Footer
    c.setFont("Helvetica-Oblique", 9)
    c.drawString(1*inch, 1.2*inch, "Thank you for your generous donation!")
    c.drawString(1*inch, 1.0*inch, "Please consult with a tax professional regarding deductibility.")
    
    # Receipt date at bottom
    c.setFont("Helvetica", 8)
    c.drawString(1*inch, 0.7*inch, f"Receipt Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}")
    
    c.save()
    buffer.seek(0)
    return buffer

def get_email_body(data):
    """Generate email body text using template"""
    template = load_email_template()
    
    # Replace variables in template
    body = template.replace('{firstName}', data['firstName'])
    body = body.replace('{lastName}', data['lastName'])
    body = body.replace('{donationType}', data['donationType'].capitalize())
    body = body.replace('{donationDate}', datetime.strptime(data['donationDate'], '%Y-%m-%d').strftime('%B %d, %Y'))
    body = body.replace('{location}', data['location'])
    
    return body

def get_access_token():
    """Get access token for Microsoft Graph API"""
    if not GRAPH_CONFIG.get('tenant_id') or not GRAPH_CONFIG.get('client_id') or not GRAPH_CONFIG.get('client_secret'):
        raise Exception(
            "Microsoft Graph API credentials not configured. "
            "Please update config.py with your Azure AD app credentials."
        )
    
    token_url = f"https://login.microsoftonline.com/{GRAPH_CONFIG['tenant_id']}/oauth2/v2.0/token"
    
    payload = {
        'grant_type': 'client_credentials',
        'client_id': GRAPH_CONFIG['client_id'],
        'client_secret': GRAPH_CONFIG['client_secret'],
        'scope': 'https://graph.microsoft.com/.default'
    }
    
    response = requests.post(token_url, data=payload)
    
    if response.status_code != 200:
        raise Exception(f"Failed to get access token: {response.status_code} - {response.text}")
    
    access_token = response.json().get('access_token')
    
    if not access_token:
        raise Exception("No access token received from Microsoft Graph API")
    
    return access_token

def send_email_smtp(data, pdf_buffer):
    """Send email using SMTP (Gmail/Google Workspace)"""
    if not EMAIL_CONFIG.get('sender_email') or not EMAIL_CONFIG.get('sender_password'):
        raise Exception("SMTP credentials not configured in config.py")
    
    # Create message
    msg = MIMEMultipart()
    msg['From'] = EMAIL_CONFIG['sender_email']
    msg['To'] = data['email']
    msg['Subject'] = 'Thank You for Your Donation - Receipt Enclosed'
    
    # Email body
    body = get_email_body(data)
    msg.attach(MIMEText(body, 'plain'))
    
    # Attach PDF
    pdf_buffer.seek(0)
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(pdf_buffer.read())
    encoders.encode_base64(part)
    part.add_header(
        'Content-Disposition',
        f'attachment; filename=donation_receipt_{datetime.now().strftime("%Y%m%d")}.pdf'
    )
    msg.attach(part)
    
    # Send email via SMTP
    server = smtplib.SMTP(EMAIL_CONFIG['smtp_server'], EMAIL_CONFIG['smtp_port'])
    server.starttls()
    server.login(EMAIL_CONFIG['sender_email'], EMAIL_CONFIG['sender_password'])
    server.send_message(msg)
    server.quit()
    
    print(f"Email sent successfully via SMTP to {data['email']}")

def send_email_microsoft(data, pdf_buffer):
    """Send email using Microsoft Graph API"""
    # Get access token
    token = get_access_token()
    
    # Read PDF and encode as base64
    pdf_buffer.seek(0)
    pdf_bytes = pdf_buffer.read()
    pdf_base64 = base64.b64encode(pdf_bytes).decode('utf-8')
    
    # Email body
    body = get_email_body(data)
    
    # Create email message for Graph API
    message = {
        "message": {
            "subject": "Thank You for Your Donation - Receipt Enclosed",
            "body": {
                "contentType": "Text",
                "content": body
            },
            "toRecipients": [
                {
                    "emailAddress": {
                        "address": data['email']
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
    
    # Send email via Graph API
    url = f"https://graph.microsoft.com/v1.0/users/{GRAPH_CONFIG['sender_email']}/sendMail"
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    response = requests.post(url, json=message, headers=headers)
    
    if response.status_code != 202:
        raise Exception(f"Graph API error: {response.status_code} - {response.text}")
    
    print(f"Email sent successfully via Microsoft Graph API to {data['email']}")

def send_email_with_receipt(data, pdf_buffer):
    """Send email with PDF receipt attached - uses configured email mode"""
    try:
        if EMAIL_MODE == 'microsoft':
            send_email_microsoft(data, pdf_buffer)
        else:  # Default to SMTP
            send_email_smtp(data, pdf_buffer)
        
        return True
            
    except Exception as e:
        print(f"Email error ({EMAIL_MODE} mode): {str(e)}")
        return False

@app.route('/api/submit-donation', methods=['POST'])
def submit_donation():
    """Handle donation submission"""
    try:
        data = request.json
        
        # Save to CSV
        save_to_csv(data)
        
        # Generate PDF
        pdf_buffer = generate_pdf_receipt(data)
        
        # Send email
        email_sent = send_email_with_receipt(data, pdf_buffer)
        
        # Send to Bloomerang CRM
        bloomerang_result = send_to_bloomerang(data)
        
        return jsonify({
            'success': True,
            'message': 'Donation recorded successfully',
            'emailSent': email_sent,
            'bloomerangSynced': bloomerang_result.get('success', False),
            'bloomerangMessage': bloomerang_result.get('message', '')
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@app.route('/api/download-csv', methods=['GET'])
def download_csv():
    """Download the donors CSV file"""
    if os.path.exists(CSV_FILE):
        return send_file(CSV_FILE, as_attachment=True, download_name='donors.csv')
    return jsonify({'error': 'No data available'}), 404

@app.route('/api/test-email', methods=['POST'])
def test_email():
    """Test email configuration - uses configured email mode"""
    try:
        data = request.json
        
        if EMAIL_MODE == 'microsoft':
            # Test Microsoft Graph API
            test_email_address = data.get('email', GRAPH_CONFIG['sender_email'])
            token = get_access_token()
            
            message = {
                "message": {
                    "subject": "Test Email - Donor App",
                    "body": {
                        "contentType": "Text",
                        "content": "This is a test email from your donor app using Microsoft Graph API."
                    },
                    "toRecipients": [
                        {
                            "emailAddress": {
                                "address": test_email_address
                            }
                        }
                    ]
                }
            }
            
            url = f"https://graph.microsoft.com/v1.0/users/{GRAPH_CONFIG['sender_email']}/sendMail"
            headers = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }
            
            response = requests.post(url, json=message, headers=headers)
            
            if response.status_code == 202:
                return jsonify({'success': True, 'message': 'Test email sent successfully via Microsoft Graph API'})
            else:
                return jsonify({'success': False, 'message': f'Graph API error: {response.status_code} - {response.text}'}), 500
        
        else:  # SMTP mode
            test_email_address = data.get('email', EMAIL_CONFIG['sender_email'])
            
            msg = MIMEMultipart()
            msg['From'] = EMAIL_CONFIG['sender_email']
            msg['To'] = test_email_address
            msg['Subject'] = 'Test Email - Donor App'
            msg.attach(MIMEText('This is a test email from your donor app using SMTP.', 'plain'))
            
            server = smtplib.SMTP(EMAIL_CONFIG['smtp_server'], EMAIL_CONFIG['smtp_port'])
            server.starttls()
            server.login(EMAIL_CONFIG['sender_email'], EMAIL_CONFIG['sender_password'])
            server.send_message(msg)
            server.quit()
            
            return jsonify({'success': True, 'message': 'Test email sent successfully via SMTP'})
            
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/')
def index():
    """Serve the main HTML page"""
    return send_file('index.html')

@app.route('/settings')
def settings_page():
    """Serve the settings page"""
    return send_file('settings.html')

@app.route('/static/<path:filename>')
def serve_static(filename):
    """Serve static files (images, etc.)"""
    from flask import send_from_directory
    return send_from_directory('static', filename)

# Email template storage file (will be redefined below with persistent path)

def get_default_email_template():
    """Get the default email template"""
    return """Dear {firstName} {lastName},

On behalf of the 6,000 people we serve, we would like to thank you for your donation. Your continued support makes a significant impact to people with disabilities and other barriers in Miami-Dade, Broward and Monroe Counties.

With each donation, 28 million pounds of reusable items are kept out of landfills and are used to fill our store shelves. When these items are purchased at our 35 Goodwill stores, the money is used to help fund our training, employment and job placement programs.

Because of loyal supporters like you, we can make a lasting impact on the environment, in our community and in the lives of people with disabilities and other barriers.

Donation Details:
- Type: {donationType}
- Date: {donationDate}
- Location: {location}

Please find your donation receipt attached to this email for your records.

Thank You!

Your friends at Goodwill South Florida"""

def load_email_template():
    """Load email template from file or return default"""
    if os.path.exists(EMAIL_TEMPLATE_FILE):
        try:
            with open(EMAIL_TEMPLATE_FILE, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"Error loading template: {e}")
    return get_default_email_template()

def save_email_template(template):
    """Save email template to file"""
    try:
        with open(EMAIL_TEMPLATE_FILE, 'w', encoding='utf-8') as f:
            f.write(template)
        return True
    except Exception as e:
        print(f"Error saving template: {e}")
        return False

@app.route('/api/email-template', methods=['GET'])
def get_email_template():
    """Get current email template"""
    try:
        template = load_email_template()
        return jsonify({'success': True, 'template': template})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/email-template', methods=['POST'])
def update_email_template():
    """Update email template"""
    try:
        data = request.json
        template = data.get('template', '')
        
        if not template:
            return jsonify({'success': False, 'message': 'Template cannot be empty'}), 400
        
        if save_email_template(template):
            return jsonify({'success': True, 'message': 'Template saved successfully'})
        else:
            return jsonify({'success': False, 'message': 'Failed to save template'}), 500
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/email-template/reset', methods=['POST'])
def reset_email_template():
    """Reset email template to default"""
    try:
        default_template = get_default_email_template()
        if save_email_template(default_template):
            return jsonify({'success': True, 'template': default_template})
        else:
            return jsonify({'success': False, 'message': 'Failed to reset template'}), 500
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

# Location Management
# Use /home directory on Azure (persists across deployments) or local directory
PERSISTENT_DIR = '/home' if os.path.exists('/home/site/wwwroot') else '.'
LOCATIONS_FILE = os.path.join(PERSISTENT_DIR, 'donation_locations.json')
FORM_TITLE_FILE = os.path.join(PERSISTENT_DIR, 'form_title.txt')
EMAIL_TEMPLATE_FILE = os.path.join(PERSISTENT_DIR, 'email_template.txt')

def load_locations():
    """Load locations from file"""
    try:
        if os.path.exists(LOCATIONS_FILE):
            with open(LOCATIONS_FILE, 'r') as f:
                return json.load(f)
        else:
            # Default locations
            return [
                "Gulliver Prep | Marian C. Krutulis PK-8 Campus",
                "Gulliver Prep | Upper School Campus"
            ]
    except Exception as e:
        print(f"Error loading locations: {e}")
        return [
            "Gulliver Prep | Marian C. Krutulis PK-8 Campus",
            "Gulliver Prep | Upper School Campus"
        ]

def save_locations(locations):
    """Save locations to file"""
    try:
        with open(LOCATIONS_FILE, 'w') as f:
            json.dump(locations, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving locations: {e}")
        return False

@app.route('/api/locations', methods=['GET'])
def get_locations():
    """Get all donation locations"""
    try:
        locations = load_locations()
        return jsonify({'success': True, 'locations': locations})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/locations', methods=['POST'])
def add_location():
    """Add a new donation location"""
    try:
        data = request.json
        location = data.get('location', '').strip()
        
        if not location:
            return jsonify({'success': False, 'message': 'Location name cannot be empty'}), 400
        
        locations = load_locations()
        
        if location in locations:
            return jsonify({'success': False, 'message': 'Location already exists'}), 400
        
        locations.append(location)
        
        if save_locations(locations):
            return jsonify({'success': True, 'message': 'Location added successfully'})
        else:
            return jsonify({'success': False, 'message': 'Failed to save location'}), 500
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/locations', methods=['DELETE'])
def delete_location():
    """Delete a donation location"""
    try:
        data = request.json
        location = data.get('location', '').strip()
        
        if not location:
            return jsonify({'success': False, 'message': 'Location name cannot be empty'}), 400
        
        locations = load_locations()
        
        if location not in locations:
            return jsonify({'success': False, 'message': 'Location not found'}), 404
        
        if len(locations) <= 1:
            return jsonify({'success': False, 'message': 'Cannot delete the last location'}), 400
        
        locations.remove(location)
        
        if save_locations(locations):
            return jsonify({'success': True, 'message': 'Location deleted successfully'})
        else:
            return jsonify({'success': False, 'message': 'Failed to save locations'}), 500
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

# Form Title Management
def load_form_title():
    """Load form title from file"""
    try:
        if os.path.exists(FORM_TITLE_FILE):
            with open(FORM_TITLE_FILE, 'r', encoding='utf-8') as f:
                return f.read().strip()
        else:
            return "Marketing Donor Registration Form"
    except Exception as e:
        print(f"Error loading form title: {e}")
        return "Marketing Donor Registration Form"

def save_form_title(title):
    """Save form title to file"""
    try:
        with open(FORM_TITLE_FILE, 'w', encoding='utf-8') as f:
            f.write(title)
        return True
    except Exception as e:
        print(f"Error saving form title: {e}")
        return False

@app.route('/api/form-title', methods=['GET'])
def get_form_title():
    """Get form title"""
    try:
        title = load_form_title()
        return jsonify({'success': True, 'title': title})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/form-title', methods=['POST'])
def update_form_title():
    """Update form title"""
    try:
        data = request.json
        title = data.get('title', '').strip()
        
        if not title:
            return jsonify({'success': False, 'message': 'Title cannot be empty'}), 400
        
        if save_form_title(title):
            return jsonify({'success': True, 'message': 'Form title saved successfully'})
        else:
            return jsonify({'success': False, 'message': 'Failed to save form title'}), 500
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/bloomerang/test', methods=['POST'])
def test_bloomerang():
    """Test Bloomerang CRM connection"""
    try:
        if not BLOOMERANG_CONFIG.get('enabled'):
            return jsonify({'success': False, 'message': 'Bloomerang integration is disabled'}), 400
        
        if not BLOOMERANG_CONFIG.get('api_key'):
            return jsonify({'success': False, 'message': 'Bloomerang API key not configured'}), 400
        
        # Test API connection
        headers = {
            'X-API-Key': BLOOMERANG_CONFIG['api_key'],
            'Content-Type': 'application/json'
        }
        
        test_url = f"{BLOOMERANG_CONFIG['api_url']}/constituents?take=1"
        response = requests.get(test_url, headers=headers)
        
        if response.status_code == 200:
            return jsonify({
                'success': True,
                'message': 'Successfully connected to Bloomerang CRM',
                'api_url': BLOOMERANG_CONFIG['api_url']
            })
        else:
            return jsonify({
                'success': False,
                'message': f'Failed to connect: {response.status_code} - {response.text}'
            }), 500
            
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

# Initialize CSV on startup
init_csv()

if __name__ == '__main__':
    print("=" * 50)
    print("Starting Marketing Donor Management Server...")
    print(f"Server running on http://localhost:{PORT}")
    print("=" * 50)
    print(f"\n📧 Email Mode: {EMAIL_MODE.upper()}")
    if EMAIL_MODE == 'microsoft':
        print(f"   Sender: {GRAPH_CONFIG.get('sender_email', 'Not configured')}")
        print("   Method: Microsoft Graph API")
    else:
        print(f"   Sender: {EMAIL_CONFIG.get('sender_email', 'Not configured')}")
        print("   Method: SMTP")
    print("\n🔄 Bloomerang CRM: " + ("ENABLED" if BLOOMERANG_CONFIG.get('enabled') else "DISABLED"))
    if BLOOMERANG_CONFIG.get('enabled'):
        print(f"   API URL: {BLOOMERANG_CONFIG.get('api_url', 'Not configured')}")
        print(f"   API Key: {'Configured' if BLOOMERANG_CONFIG.get('api_key') else 'Not configured'}")
        if not BLOOMERANG_CONFIG.get('verify_ssl', True):
            print("   ⚠️  SSL Verification: DISABLED (for local testing only!)")
    print("=" * 50)
    app.run(debug=DEBUG, host='0.0.0.0', port=PORT)
