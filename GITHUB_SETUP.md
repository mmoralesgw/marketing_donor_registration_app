# GitHub Setup Instructions

## Before Uploading to GitHub

### ✅ Security Checklist

Make sure these files are **NOT** uploaded (they're in `.gitignore`):
- ✅ `config.py` - Contains your credentials
- ✅ `donors.csv` - Contains donor data
- ✅ `email_template.txt` - Custom email template
- ✅ `*.pdf` - Generated receipts
- ✅ `__pycache__/` - Python cache

### Files That WILL Be Uploaded:
- ✅ `config.example.py` - Template without credentials
- ✅ All `.md` documentation files
- ✅ `app.py`, `index.html`, `settings.html`
- ✅ `requirements.txt`
- ✅ `.gitignore`

## Step-by-Step Upload

### 1. Initialize Git (if not already done)

```bash
git init
```

### 2. Check What Will Be Committed

```bash
git status
```

**Verify that `config.py` is NOT listed!**

### 3. Add Files

```bash
git add .
```

### 4. Commit

```bash
git commit -m "Initial commit: Goodwill Donated Goods Form"
```

### 5. Create GitHub Repository

1. Go to https://github.com
2. Click "New repository"
3. Name: `donor-management-system` (or your choice)
4. Description: "Goodwill Donated Goods Form for Goodwill South Florida"
5. Choose: **Private** (recommended) or Public
6. Don't initialize with README (you already have one)
7. Click "Create repository"

### 6. Connect to GitHub

```bash
git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPO-NAME.git
git branch -M main
git push -u origin main
```

## After Uploading

### For Team Members Cloning the Repo

1. **Clone the repository:**
   ```bash
   git clone https://github.com/YOUR-USERNAME/YOUR-REPO-NAME.git
   cd YOUR-REPO-NAME
   ```

2. **Create config.py from template:**
   ```bash
   copy config.example.py config.py
   ```
   (On Linux/Mac: `cp config.example.py config.py`)

3. **Update config.py with actual credentials**
   - Add email credentials
   - Add Azure AD credentials (if using Microsoft mode)
   - Update organization details

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the app:**
   ```bash
   python app.py
   ```

## Important Notes

### Never Commit Credentials

If you accidentally commit `config.py` with credentials:

1. **Remove from Git history:**
   ```bash
   git rm --cached config.py
   git commit -m "Remove config.py from tracking"
   git push
   ```

2. **Rotate all credentials immediately:**
   - Generate new Azure client secret
   - Generate new Gmail app password
   - Update config.py locally

### Repository Settings

**Recommended GitHub Settings:**

1. **Make it Private** (if it contains organization-specific code)
2. **Add collaborators** (Settings → Collaborators)
3. **Enable branch protection** (Settings → Branches)
4. **Add repository description**

### .gitignore Verification

Before each commit, verify sensitive files are ignored:

```bash
git status
```

Should NOT show:
- config.py
- donors.csv
- *.pdf
- email_template.txt

## Updating the Repository

### Regular Updates

```bash
git add .
git commit -m "Description of changes"
git push
```

### Pulling Updates

```bash
git pull origin main
```

## Documentation Files

These documentation files are included in the repo:

- `README.md` - Main documentation
- `QUICKSTART.md` - Quick setup guide
- `GMAIL_SETUP.md` - Gmail configuration
- `GRAPH_API_SETUP.md` - Microsoft Graph API setup
- `EMAIL_MODE_GUIDE.md` - Email mode switching
- `SETTINGS_GUIDE.md` - Settings page guide
- `deploy-azure.md` - Azure deployment
- `AZURE_DEPLOYMENT_CHECKLIST.md` - Deployment checklist

## Collaboration

### For Team Members

1. **Clone the repo**
2. **Create your own config.py** (never commit it!)
3. **Create a branch for features:**
   ```bash
   git checkout -b feature/your-feature-name
   ```
4. **Make changes and commit**
5. **Push and create Pull Request**

### Code Review

Before merging:
- ✅ Check no credentials are committed
- ✅ Test the changes locally
- ✅ Update documentation if needed

## Backup Strategy

### What to Backup Separately

These files are NOT in Git (by design):
- `config.py` - Store securely (password manager, Azure Key Vault)
- `donors.csv` - Backup to secure location
- `email_template.txt` - Backup custom templates

### Recommended Backup

1. **Azure Key Vault** - For credentials
2. **Azure Blob Storage** - For donor data
3. **Encrypted backup** - For local copies

## Security Best Practices

1. ✅ Never commit credentials
2. ✅ Use `.gitignore` properly
3. ✅ Make repo private if needed
4. ✅ Rotate credentials regularly
5. ✅ Use environment variables in production
6. ✅ Enable 2FA on GitHub
7. ✅ Review commits before pushing

## Troubleshooting

### "config.py not found" Error

**Solution:** Copy from template
```bash
copy config.example.py config.py
```

### Accidentally Committed Credentials

**Solution:**
1. Remove from Git: `git rm --cached config.py`
2. Rotate all credentials immediately
3. Update `.gitignore`
4. Commit and push

### Can't Push to GitHub

**Solution:**
- Check remote URL: `git remote -v`
- Verify GitHub credentials
- Check branch name: `git branch`

## Questions?

See the main `README.md` for detailed setup instructions.
