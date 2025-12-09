# Bloomerang CRM Integration Guide

The Goodwill Donated Goods Form now automatically syncs donors to Bloomerang CRM.

## Features

- ✅ Automatic donor creation in Bloomerang
- ✅ Duplicate detection (searches by email)
- ✅ Transaction/donation recording
- ✅ In-kind donation tracking
- ✅ Merchandise details in notes
- ✅ Can be enabled/disabled easily

## Setup Steps

### 1. Get Your Bloomerang API Key

1. Log in to your Bloomerang account
2. Go to **Settings** → **Integrations** → **API**
3. Click **Generate New API Key**
4. Copy the API key (it looks like: `abc123def456...`)

### 2. Update config.py

Edit `config.py` and add your API key:

```python
BLOOMERANG_CONFIG = {
    'enabled': True,  # Set to False to disable
    'api_key': 'your-actual-api-key-here',
    'api_url': 'https://api.bloomerang.co/v2'
}
```

### 3. Test the Connection

Run the app and test:

```bash
python app.py
```

You should see:
```
🔄 Bloomerang CRM: ENABLED
   API URL: https://api.bloomerang.co/v2
   API Key: Configured
```

### 4. Submit a Test Donation

1. Open the donor form
2. Fill in test data
3. Submit
4. Check Bloomerang to verify the donor was created

## How It Works

### When a Donation is Submitted:

1. **Search for Existing Donor**
   - Searches Bloomerang by email address
   - If found, uses existing constituent ID

2. **Create New Donor (if needed)**
   - Creates new constituent with:
     - First Name
     - Last Name
     - Email Address
     - Phone Number
     - Home Address
     - Status: Active
     - Type: Individual

3. **Record Transaction**
   - Creates an in-kind donation record
   - Amount: $0 (in-kind)
   - Method: InKind
   - Date: Donation date
   - Notes: Includes donation type, location, and items

### Data Mapping

| Donor Form Field | Bloomerang Field |
|-----------------|------------------|
| First Name | FirstName |
| Last Name | LastName |
| Email | EmailAddress |
| Phone | PhoneNumber |
| Address | Address (Home) |
| Donation Type | Transaction Note |
| Merchandise Items | Transaction Note |
| Location | Transaction Note |
| Donation Date | Transaction Date |

## Disabling Bloomerang Integration

To disable without removing configuration:

```python
BLOOMERANG_CONFIG = {
    'enabled': False,  # Just change this to False
    'api_key': 'your-api-key',
    'api_url': 'https://api.bloomerang.co/v2'
}
```

## Testing the Integration

### Test API Connection

You can test the connection using the API endpoint:

```bash
curl -X POST http://localhost:5000/api/bloomerang/test
```

Or use a tool like Postman.

### Test with Sample Data

Submit a donation with test data:
- First Name: Test
- Last Name: Donor
- Email: test@example.com
- Phone: (555) 123-4567
- Address: 123 Test St

Check Bloomerang to verify:
1. Constituent was created
2. Transaction was recorded
3. Notes contain donation details

## For Azure Deployment

Set environment variables in Azure Portal:

```
BLOOMERANG_ENABLED = true
BLOOMERANG_API_KEY = your-api-key
BLOOMERANG_API_URL = https://api.bloomerang.co/v2
```

## Troubleshooting

### "Bloomerang integration is disabled"
**Solution:** Set `enabled: True` in config.py

### "Bloomerang API key not configured"
**Solution:** Add your API key to config.py

### "Failed to create constituent"
**Possible causes:**
- Invalid API key
- API rate limit exceeded
- Required fields missing
- Network connectivity issue

**Solution:**
- Verify API key is correct
- Check Bloomerang API status
- Review error message in console

### "Failed to create transaction"
**Possible causes:**
- Constituent ID not found
- Invalid transaction data
- API permissions issue

**Solution:**
- Check that constituent was created first
- Verify API key has transaction permissions
- Review error message

### Duplicate Detection

The system uses **smart matching** to find existing constituents using multiple identifiers:

**Matching Criteria (scored):**
- **Email match:** 100 points (strongest indicator)
- **Phone match:** 50 points (good indicator)
- **Name match:** 30 points (First + Last name)

**Match threshold:** 80 points or higher

**Examples:**
- ✅ Email matches → Uses existing constituent
- ✅ Phone + Name match → Uses existing constituent  
- ✅ Email matches (even if name different) → Uses existing constituent
- ❌ Only name matches → Creates new constituent (too weak)

This handles cases where:
- Constituents have no email address (uses phone + name)
- Email changed but phone/name same
- Typos in name but email/phone match

**Important:** The search checks the last 500 constituents (10 pages × 50 per page, Bloomerang's limit). If you have more than 500 constituents and the donor is older, a duplicate might be created. To adjust this:

Edit `app.py` and change the `max_pages` parameter:
```python
max_pages = 20  # Search up to 1000 constituents (20 pages × 50)
```

**Note:** More pages = slower search but better duplicate detection.

## API Rate Limits

Bloomerang API has rate limits:
- Check your plan's limits
- The app makes 2-3 API calls per donation:
  1. Search for existing constituent
  2. Create constituent (if new)
  3. Create transaction

## Best Practices

1. **Test First**
   - Use test data before going live
   - Verify data appears correctly in Bloomerang

2. **Monitor Logs**
   - Check console for sync status
   - Review error messages

3. **Backup Data**
   - CSV file is still created as backup
   - Don't rely solely on Bloomerang sync

4. **Handle Failures Gracefully**
   - If Bloomerang sync fails, donation is still:
     - Saved to CSV
     - Email sent to donor
     - PDF receipt generated

5. **Keep API Key Secure**
   - Never commit to Git
   - Use environment variables in production
   - Rotate periodically

## Response Messages

After submitting a donation, you'll see:

**Success:**
```json
{
  "success": true,
  "message": "Donation recorded successfully",
  "emailSent": true,
  "bloomerangSynced": true,
  "bloomerangMessage": "Successfully added to Bloomerang"
}
```

**Bloomerang Disabled:**
```json
{
  "success": true,
  "message": "Donation recorded successfully",
  "emailSent": true,
  "bloomerangSynced": false,
  "bloomerangMessage": "Bloomerang integration disabled"
}
```

**Bloomerang Error:**
```json
{
  "success": true,
  "message": "Donation recorded successfully",
  "emailSent": true,
  "bloomerangSynced": false,
  "bloomerangMessage": "Failed to create constituent: [error details]"
}
```

## Bloomerang API Documentation

For more details, see:
- [Bloomerang API Docs](https://bloomerang.co/product/integrations-api/)
- [API Reference](https://api.bloomerang.co/v2/help)

## Custom Fields

If you need to map additional fields:

1. Identify the Bloomerang field name
2. Update the `send_to_bloomerang()` function in `app.py`
3. Add the field to `constituent_data` or `transaction_data`

Example:
```python
constituent_data = {
    'Type': 'Individual',
    'FirstName': data['firstName'],
    'LastName': data['lastName'],
    # Add custom field:
    'CustomField1': data.get('customValue', '')
}
```

## Support

For Bloomerang-specific issues:
- Contact Bloomerang Support
- Check API status page
- Review API documentation

For integration issues:
- Check app console logs
- Test API connection endpoint
- Verify configuration
