"""
Simple test script to verify the donor app is working
Run this after deploying to test basic functionality
"""

import requests
import json

# Configuration
BASE_URL = "http://localhost:5000"  # Change to your Azure URL when deployed
# Example: BASE_URL = "https://goodwill-donor-app.azurewebsites.net"

def test_api_connection():
    """Test if the API is accessible"""
    print("Testing API connection...")
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            print("✓ API is accessible")
            return True
        else:
            print(f"✗ API returned status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Error connecting to API: {str(e)}")
        return False

def test_submit_donation():
    """Test submitting a donation"""
    print("\nTesting donation submission...")
    
    test_data = {
        "firstName": "John",
        "lastName": "Doe",
        "email": "test@example.com",
        "phone": "(555) 123-4567",
        "address": "123 Test Street, Miami, FL 33101",
        "donationType": "merchandise",
        "merchandiseItems": ["Clothing", "Books"],
        "donationDate": "2024-01-15",
        "location": "Main Office"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/submit-donation",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("✓ Donation submitted successfully")
                if result.get('emailSent'):
                    print("✓ Email sent successfully")
                else:
                    print("⚠ Email sending failed (check email configuration)")
                return True
            else:
                print(f"✗ Donation submission failed: {result.get('message')}")
                return False
        else:
            print(f"✗ API returned status code: {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"✗ Error submitting donation: {str(e)}")
        return False

def test_csv_download():
    """Test CSV download"""
    print("\nTesting CSV download...")
    try:
        response = requests.get(f"{BASE_URL}/api/download-csv")
        if response.status_code == 200:
            print("✓ CSV download successful")
            print(f"  CSV size: {len(response.content)} bytes")
            return True
        elif response.status_code == 404:
            print("⚠ No CSV data available yet (submit a donation first)")
            return True
        else:
            print(f"✗ CSV download failed with status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Error downloading CSV: {str(e)}")
        return False

def main():
    print("=" * 50)
    print("Donor App Test Suite")
    print("=" * 50)
    print(f"Testing: {BASE_URL}")
    print("=" * 50)
    
    results = []
    
    # Run tests
    results.append(("API Connection", test_api_connection()))
    results.append(("Donation Submission", test_submit_donation()))
    results.append(("CSV Download", test_csv_download()))
    
    # Summary
    print("\n" + "=" * 50)
    print("Test Summary")
    print("=" * 50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{test_name}: {status}")
    
    print("=" * 50)
    print(f"Results: {passed}/{total} tests passed")
    print("=" * 50)
    
    if passed == total:
        print("\n🎉 All tests passed! Your app is working correctly.")
    else:
        print("\n⚠ Some tests failed. Check the output above for details.")

if __name__ == "__main__":
    # Check if requests is installed
    try:
        import requests
    except ImportError:
        print("Error: 'requests' library not installed")
        print("Install it with: pip install requests")
        exit(1)
    
    main()
