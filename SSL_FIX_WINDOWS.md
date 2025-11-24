# SSL Certificate Error Fix (Windows)

If you see this error:
```
[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate
```

## Quick Solutions

### Solution 1: Update Python Packages (Recommended)
```bash
pip install --upgrade certifi requests urllib3
```

### Solution 2: Install Python Certificates
If you're using Python from python.org:

1. Go to your Python installation folder:
   ```
   C:\Users\YourName\AppData\Local\Programs\Python\Python313\
   ```

2. Run the certificate installer:
   ```
   Install Certificates.command
   ```
   (Double-click this file)

### Solution 3: Run as Administrator
Right-click Command Prompt → "Run as Administrator", then:
```bash
python app.py
```

### Solution 4: Use Corporate Network Settings
If you're on a corporate network with a proxy:

Add to your `config.py`:
```python
import os
os.environ['REQUESTS_CA_BUNDLE'] = r'C:\path\to\your\corporate\cert.pem'
```

## Why This Happens

Windows doesn't always have the latest SSL certificates. The Bloomerang API uses modern SSL certificates that may not be in your Windows certificate store.

## Testing the Fix

Run this to test:
```bash
python fix_ssl_windows.py
```

You should see:
```
✅ SSL connection successful!
```

## Still Not Working?

### Option A: Temporary Workaround (NOT for Production!)

**For testing only**, you can disable SSL verification:

Edit `app.py` and change:
```python
verify=True
```
to:
```python
verify=False
```

⚠️ **WARNING:** This is insecure! Only use for local testing.

### Option B: Use Azure Deployment

Deploy to Azure where SSL certificates are properly configured:
```bash
.\deploy.ps1
```

Azure App Service has proper SSL certificates and won't have this issue.

## For IT Administrators

If this is a company-wide issue:

1. **Update Windows Certificates:**
   - Windows Update
   - Install latest root certificates

2. **Configure Corporate Proxy:**
   - Add corporate CA certificate
   - Configure proxy settings

3. **Python Installation:**
   - Use Python from Microsoft Store (has better certificate handling)
   - Or ensure python.org installation includes certificates

## Verification

After applying a fix, test with:
```bash
python -c "import requests; print(requests.get('https://api.bloomerang.co').status_code)"
```

Should print: `200` or `404` (not an SSL error)

## Need More Help?

- Check Python version: `python --version` (use 3.11 or higher)
- Check certifi: `python -c "import certifi; print(certifi.where())"`
- Check requests: `python -c "import requests; print(requests.__version__)"`

## For Production

Always use proper SSL verification (`verify=True`). Never disable SSL in production!

If SSL issues persist in production:
- Deploy to Azure (recommended)
- Use a proper SSL certificate bundle
- Contact your IT department
