# Deploy to Azure from GitHub - Step by Step

Your code is already on GitHub at:
`https://github.com/mmoralesgw/marketing_donor_registration_app`

Now let's deploy it to Azure App Service using GitHub as the source.

---

## Step 1: Create Azure App Service

### 1.1 Go to Azure Portal
- Open: https://portal.azure.com
- Sign in with your Azure account

### 1.2 Create Web App
1. Click **"Create a resource"** (top-left)
2. Search for **"Web App"**
3. Click **"Create"**

### 1.3 Fill in Basic Details

**Project Details:**
- **Subscription:** Select your subscription
- **Resource Group:** Create new → `goodwill-rg` (or use existing)

**Instance Details:**
- **Name:** `goodwill-donor-app` (or your choice)
  - This will be your URL: `goodwill-donor-app.azurewebsites.net`
- **Publish:** Code
- **Runtime stack:** Python 3.11
- **Operating System:** Linux
- **Region:** East US (or closest to you)

**Pricing Plan:**
- Click **"Create new"** or select existing
- **Sku and size:** B1 Basic (or higher)
  - Click "Change size" if needed
  - Recommended: B1 ($13/month) or S1 ($70/month)

### 1.4 Create
- Click **"Review + Create"**
- Review settings
- Click **"Create"**
- Wait 2-3 minutes for deployment

---

## Step 2: Configure GitHub Deployment

### 2.1 Go to Deployment Center
1. In your App Service, find **"Deployment Center"** in the left menu
2. Click on it

### 2.2 Select Source
1. **Source:** Select **"GitHub"**
2. Click **"Authorize"** if prompted
3. Sign in to GitHub and authorize Azure

### 2.3 Configure Repository
1. **Organization:** Select your GitHub username (`mmoralesgw`)
2. **Repository:** Select `marketing_donor_registration_app`
3. **Branch:** Select `main`

### 2.4 Build Configuration
- **Build Provider:** App Service Build Service (default)
- Leave other settings as default

### 2.5 Save
- Click **"Save"** at the top
- Azure will automatically start deploying from GitHub
- This takes 3-5 minutes

---

## Step 3: Configure Application Settings

### 3.1 Go to Configuration
1. In your App Service, click **"Configuration"** in the left menu
2. Click **"Application settings"** tab

### 3.2 Add Environment Variables

Click **"+ New application setting"** for each:

**Email Settings (Microsoft Graph API):**
```
Name: AZURE_TENANT_ID
Value: [your-tenant-id]

Name: AZURE_CLIENT_ID
Value: [your-client-id]

Name: AZURE_CLIENT_SECRET
Value: [your-client-secret]

Name: MS_SENDER_EMAIL
Value: gw-appdev@GoodwillMiami.org

Name: EMAIL_MODE
Value: microsoft
```

**Bloomerang CRM:**
```
Name: BLOOMERANG_ENABLED
Value: true

Name: BLOOMERANG_API_KEY
Value: [your-bloomerang-api-key]

Name: BLOOMERANG_API_URL
Value: https://api.bloomerang.co/v2

Name: BLOOMERANG_VERIFY_SSL
Value: true
```

**Organization Details:**
```
Name: ORG_NAME
Value: Goodwill South Florida

Name: ORG_ADDRESS
Value: 2121 NW 21st Street, Miami, FL 33142

Name: ORG_TAX_ID
Value: [your-tax-id]

Name: ORG_PHONE
Value: [your-phone]

Name: ORG_EMAIL
Value: gw-appdev@GoodwillMiami.org
```

### 3.3 Save Settings
- Click **"Save"** at the top
- Click **"Continue"** when prompted
- App will restart automatically

---

## Step 4: Configure Startup Command

### 4.1 Go to Configuration
1. Still in **"Configuration"**
2. Click **"General settings"** tab

### 4.2 Set Startup Command
- **Startup Command:** 
  ```
  gunicorn --bind=0.0.0.0 --timeout 600 app:app
  ```

### 4.3 Save
- Click **"Save"** at the top
- App will restart

---
##in the networking tab : 
GitHub Actions uses dynamic IP addresses that change frequently, so adding specific IPs isn't practical. Instead, here are your best options:

Option 1: Allow All GitHub Actions (Recommended)

In Azure Portal:

Go to your App Service → "Networking" → "Access restriction"
Click on the "Advanced tool site (SCM)" tab (this is important!)
Click "Add rule"
Configure:
Name: Allow GitHub Actions
Action: Allow
Priority: 100
Type: Service Tag
Service Tag: AzureCloud or GitHub
Click "Add rule"


## Step 5: Verify Deployment

### 5.1 Check Deployment Status
1. Go to **"Deployment Center"**
2. Check the **"Logs"** tab
3. Wait for deployment to complete (green checkmark)

### 5.2 Browse to Your App
1. Go to **"Overview"** in your App Service
2. Click the **URL** (e.g., `https://goodwill-donor-app.azurewebsites.net`)
3. Your donor form should load!

---

## Step 6: Test Everything

### 6.1 Submit Test Donation
1. Fill out the donor form
2. Submit a donation
3. Check for success message

### 6.2 Verify Integrations
- [ ] Email received with PDF receipt
- [ ] Constituent created in Bloomerang
- [ ] Transaction recorded in Bloomerang
- [ ] CSV download works

### 6.3 Test Settings Page
- [ ] Visit `/settings.html`
- [ ] Edit email template
- [ ] Save changes
- [ ] Submit another donation to test new template

---

## Step 7: Monitor and Troubleshoot

### 7.1 View Logs
1. Go to **"Log stream"** in your App Service
2. Watch for any errors
3. Check startup messages

### 7.2 Common Issues

**App won't start:**
- Check logs in Log stream
- Verify startup command is correct
- Ensure all environment variables are set

**Email not sending:**
- Verify Graph API credentials
- Check MS_SENDER_EMAIL is correct
- Ensure Mail.Send permission granted

**Bloomerang not syncing:**
- Verify BLOOMERANG_API_KEY is correct
- Check BLOOMERANG_VERIFY_SSL is true
- Review logs for specific errors

---

## Automatic Deployments

Now that GitHub is connected:

1. **Any push to `main` branch** will automatically deploy
2. **Check deployment status** in Deployment Center
3. **View deployment logs** to see progress

### To Deploy Updates:
```bash
git add .
git commit -m "Your update message"
git push
```

Azure will automatically deploy the changes!

---

## Step 8: Optional Enhancements

### 8.1 Custom Domain
1. Go to **"Custom domains"**
2. Add your domain (e.g., `donors.goodwillsouthflorida.org`)
3. Configure DNS records
4. Add SSL certificate

### 8.2 Enable Application Insights
1. Go to **"Application Insights"**
2. Click **"Turn on Application Insights"**
3. Create new or use existing
4. Monitor performance and errors

### 8.3 Set Up Alerts
1. Go to **"Alerts"**
2. Create alert rules for:
   - High response time
   - Error rate
   - CPU usage

### 8.4 Scale Up/Out
1. Go to **"Scale up (App Service plan)"**
2. Choose higher tier if needed
3. Or **"Scale out"** to add instances

---

## Security Best Practices

### After Deployment:

1. **Enable HTTPS Only:**
   - Configuration → General settings
   - HTTPS Only: On

2. **Rotate Exposed Credentials:**
   - Azure AD client secret (was in Git history)
   - Bloomerang API key (optional)

3. **Set Up Backup:**
   - Consider Azure Blob Storage for CSV
   - Backup email templates
   - Document recovery procedures

4. **Review Access:**
   - Limit who can access Azure Portal
   - Use role-based access control (RBAC)
   - Enable MFA for Azure accounts

---

## 📊 Monitoring Your App

### Key Metrics to Watch:
- Response time
- Error rate
- CPU/Memory usage
- Request count
- Bloomerang API calls

### Where to Check:
- **Overview:** Quick stats
- **Metrics:** Detailed charts
- **Log stream:** Real-time logs
- **Application Insights:** Advanced analytics

---

## 🎉 You're Done!

Your Marketing Donor Registration Form is now:
- ✅ Deployed to Azure
- ✅ Connected to GitHub for automatic deployments
- ✅ Configured with all integrations
- ✅ Ready for production use

**Your App URL:**
`https://goodwill-donor-app.azurewebsites.net`
(or whatever name you chose)

---

## 📞 Need Help?

- **Azure Support:** Azure Portal → Help + support
- **Documentation:** See other .md files in the repo
- **Logs:** App Service → Log stream
- **GitHub Issues:** Create issue in your repo

---

## Quick Reference

**App Service Name:** goodwill-donor-app
**Resource Group:** goodwill-rg
**GitHub Repo:** mmoralesgw/marketing_donor_registration_app
**Runtime:** Python 3.11
**Region:** East US

**Deployment:** Automatic from GitHub `main` branch

**Cost:** ~$13-70/month depending on plan

---

Congratulations on your deployment! 🎉
