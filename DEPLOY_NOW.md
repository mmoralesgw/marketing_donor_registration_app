# Deploy to Azure - Quick Commands

## ⚠️ BEFORE DEPLOYING

Update `config.py`:
```python
BLOOMERANG_CONFIG = {
    'verify_ssl': True  # Change from False to True!
}
```

## 🚀 Deploy Now

### Windows (PowerShell):
```powershell
.\deploy.ps1
```

### Linux/Mac:
```bash
chmod +x deploy.sh
./deploy.sh
```

## 📝 After Deployment

1. **Go to Azure Portal**
2. **Your App Service → Configuration → Application Settings**
3. **Add these variables:**

```
AZURE_TENANT_ID=your-tenant-id
AZURE_CLIENT_ID=your-client-id
AZURE_CLIENT_SECRET=your-client-secret
MS_SENDER_EMAIL=your-email@domain.org
EMAIL_MODE=microsoft

BLOOMERANG_ENABLED=true
BLOOMERANG_API_KEY=your-bloomerang-api-key
BLOOMERANG_VERIFY_SSL=true

ORG_NAME=Your Organization Name
ORG_ADDRESS=Your Address
ORG_EMAIL=your-email@domain.org
```

4. **Click "Save"**
5. **Visit your app:** `https://your-app-name.azurewebsites.net`

## ✅ That's It!

Your app is now live in Azure!
