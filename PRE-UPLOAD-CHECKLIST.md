# Pre-Upload Checklist ✅

Before uploading to GitHub, verify these items:

## ✅ Security Check

- [ ] `config.py` is in `.gitignore`
- [ ] `donors.csv` is in `.gitignore`
- [ ] `email_template.txt` is in `.gitignore`
- [ ] `*.pdf` is in `.gitignore`
- [ ] No credentials in any committed files
- [ ] `config.example.py` has placeholder values only

## ✅ Files to Upload

- [ ] `app.py` - Main application
- [ ] `index.html` - Donor form
- [ ] `settings.html` - Settings page
- [ ] `requirements.txt` - Dependencies
- [ ] `config.example.py` - Configuration template
- [ ] `.gitignore` - Ignore rules
- [ ] `README.md` - Main documentation
- [ ] All guide files (*.md)

## ✅ Files to EXCLUDE

- [ ] `config.py` - Contains real credentials
- [ ] `donors.csv` - Contains donor data
- [ ] `email_template.txt` - Custom template
- [ ] `*.pdf` - Generated receipts
- [ ] `__pycache__/` - Python cache
- [ ] `.vscode/` - IDE settings

## ✅ Documentation

- [ ] README.md is up to date
- [ ] QUICKSTART.md exists
- [ ] GITHUB_SETUP.md exists
- [ ] All setup guides are included

## ✅ Code Quality

- [ ] No syntax errors
- [ ] No hardcoded credentials
- [ ] Comments are clear
- [ ] Code is formatted

## Quick Commands

### 1. Initialize Git
```bash
git init
```

### 2. Verify What Will Be Committed
```bash
git status
```

**IMPORTANT:** Make sure `config.py` is NOT listed!

### 3. Add Files
```bash
git add .
```

### 4. Commit
```bash
git commit -m "Initial commit: Marketing Donor Registration Form"
```

### 5. Create GitHub Repo
- Go to https://github.com
- Click "New repository"
- Name: `donor-management-system`
- Choose Private or Public
- Don't initialize with README
- Create repository

### 6. Push to GitHub
```bash
git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPO-NAME.git
git branch -M main
git push -u origin main
```

## After Upload

### Verify on GitHub

1. Go to your repository on GitHub
2. Check that `config.py` is NOT visible
3. Check that `config.example.py` IS visible
4. Verify README displays correctly

### For Team Members

Share these instructions:
1. Clone the repository
2. Copy `config.example.py` to `config.py`
3. Update `config.py` with actual credentials
4. Install dependencies: `pip install -r requirements.txt`
5. Run: `python app.py`

## Security Reminders

🔒 **Never commit:**
- Passwords
- API keys
- Client secrets
- Tenant IDs
- Personal data

✅ **Always:**
- Use `.gitignore`
- Use `config.example.py` for templates
- Rotate credentials if accidentally committed
- Make repo private if needed

## Need Help?

See `GITHUB_SETUP.md` for detailed instructions.
