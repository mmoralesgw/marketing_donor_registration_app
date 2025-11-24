"""
Fix SSL Certificate Issues on Windows
Run this if you get SSL certificate verification errors
"""

import ssl
import certifi

def fix_ssl_certificates():
    """Update SSL certificates for Windows"""
    print("Checking SSL certificates...")
    
    # Get certifi certificate path
    cert_path = certifi.where()
    print(f"Certificate bundle location: {cert_path}")
    
    # Test SSL connection
    try:
        import urllib.request
        context = ssl.create_default_context(cafile=cert_path)
        
        # Test connection to Bloomerang API
        print("\nTesting connection to Bloomerang API...")
        req = urllib.request.Request('https://api.bloomerang.co')
        response = urllib.request.urlopen(req, context=context)
        print("✅ SSL connection successful!")
        print(f"Status: {response.status}")
        
    except Exception as e:
        print(f"❌ SSL connection failed: {e}")
        print("\nTry these solutions:")
        print("1. Update certifi: pip install --upgrade certifi")
        print("2. Update requests: pip install --upgrade requests")
        print("3. Update Python to latest version")
        print("4. Run as administrator")

if __name__ == "__main__":
    fix_ssl_certificates()
