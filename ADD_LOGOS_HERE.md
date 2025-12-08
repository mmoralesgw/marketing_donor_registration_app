# 📸 Add Your Logo Images

## Quick Instructions

1. **Save your two logo images** from the screenshots you provided:
   - First image (Goodwill + Gulliver): Save as `goodwill_gulliver_logo.png`
   - Second image (Onda Verde): Save as `onda_verde_logo.png`

2. **Place them in the `static` folder**:
   ```
   CaptureDonationForm/
   └── static/
       ├── goodwill_gulliver_logo.png  ← Add here
       ├── onda_verde_logo.png         ← Add here
       └── README.md
   ```

3. **Test locally**:
   - Run your app: `python app.py`
   - Open http://localhost:5000
   - You should see both logos at the top

4. **Deploy to Azure**:
   ```bash
   git add static/
   git commit -m "Add logo images"
   git push
   ```

## Image Specifications

- **Format**: PNG (preferred) or JPG
- **Size**: Recommended height 120-150px
- **Background**: Transparent PNG works best
- **Quality**: High resolution for crisp display

## What I've Already Done

✅ Created the `static` folder
✅ Updated Flask to serve static files
✅ Added logo display code to index.html
✅ Configured for Azure deployment

## Need Help?

If the logos don't appear:
1. Check the browser console (F12) for errors
2. Verify the filenames match exactly (case-sensitive)
3. Make sure the images are in the `static` folder
4. Refresh the page (Ctrl+F5)
