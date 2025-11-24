# Bloomerang CRM - Quick Start

## 3-Step Setup

### 1. Get API Key
- Log in to Bloomerang
- Settings → Integrations → API
- Generate New API Key
- Copy the key

### 2. Update config.py
```python
BLOOMERANG_CONFIG = {
    'enabled': True,
    'api_key': 'paste-your-api-key-here',
    'api_url': 'https://api.bloomerang.co/v2'
}
```

### 3. Test It
```bash
python app.py
```

Look for:
```
🔄 Bloomerang CRM: ENABLED
   API URL: https://api.bloomerang.co/v2
   API Key: Configured
```

## What Happens Automatically

When a donor submits a donation:

1. ✅ **Donor is added to Bloomerang**
   - Searches by email first
   - Creates new if not found
   - Updates existing if found

2. ✅ **Transaction is recorded**
   - In-kind donation
   - Includes all details in notes
   - Links to donor record

3. ✅ **Everything else still works**
   - CSV file saved
   - Email sent
   - PDF receipt generated

## Disable Anytime

Just change one line:
```python
BLOOMERANG_CONFIG = {
    'enabled': False,  # Changed from True
    ...
}
```

## Check Sync Status

After submitting a donation, check the response:
- `bloomerangSynced: true` = Success!
- `bloomerangSynced: false` = Check logs

## Troubleshooting

**Not syncing?**
1. Check API key is correct
2. Verify `enabled: True`
3. Check console for errors

**Duplicates?**
- System searches by email
- Won't create duplicates
- Updates existing donor

## Full Documentation

See `BLOOMERANG_SETUP.md` for complete guide.
