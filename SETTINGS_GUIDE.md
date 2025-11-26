# Email Settings Guide

The Marketing Donor Registration Form now includes a **Settings Page** where you can customize the email message sent to donors.

## Accessing Settings

1. **From the main page:** Click the "⚙️ Settings" button in the top-right corner
2. **Direct URL:** Navigate to `/settings.html` or `http://localhost:5000/settings`

## Customizing Email Messages

### Available Variables

Use these variables in your email template - they will be automatically replaced with actual donor information:

- `{firstName}` - Donor's first name
- `{lastName}` - Donor's last name
- `{donationType}` - Type of donation (Cash or Merchandise)
- `{donationDate}` - Date of donation (formatted as "Month Day, Year")
- `{location}` - Donation location

### Example Template

```
Dear {firstName} {lastName},

Thank you for your {donationType} donation on {donationDate} at {location}.

We truly appreciate your support!

Best regards,
Goodwill South Florida
```

### Preview Feature

As you type, the preview section shows how your email will look with sample data:
- First Name: John
- Last Name: Doe
- Donation Type: Merchandise
- Date: January 15, 2024
- Location: Main Office

## Saving Changes

1. **Edit the template** in the text area
2. **Preview your changes** in real-time
3. Click **"💾 Save Changes"** to save
4. All future emails will use your new template

## Resetting to Default

If you want to restore the original Goodwill South Florida message:

1. Click **"🔄 Reset to Default"**
2. Confirm the action
3. The default template will be restored

**Note:** This action cannot be undone, but you can always customize it again.

## Default Template

The default template includes:
- Goodwill South Florida's mission statement
- Information about serving 6,000 people
- Environmental impact (28 million pounds)
- Details about 35 Goodwill stores
- Donation details
- Thank you message

## Template Storage

- Templates are saved in `email_template.txt`
- The file is automatically created when you save changes
- If the file is deleted, the default template is used
- The file is excluded from Git (in `.gitignore`)

## Tips for Writing Email Templates

### Best Practices

1. **Keep it personal** - Use the name variables
2. **Be concise** - Donors appreciate brief, clear messages
3. **Include key info** - Always show donation details
4. **Express gratitude** - Thank donors sincerely
5. **Add contact info** - Include how to reach you

### Formatting

- Use line breaks for readability
- Keep paragraphs short
- Use bullet points for lists
- Include a clear signature

### Example Variations

**Short and Simple:**
```
Dear {firstName} {lastName},

Thank you for your generous {donationType} donation!

Donation Details:
- Date: {donationDate}
- Location: {location}

Your support makes a difference.

Goodwill South Florida
```

**Detailed:**
```
Dear {firstName} {lastName},

We are deeply grateful for your {donationType} donation received on {donationDate} at our {location} location.

Your contribution helps us serve thousands of people in Miami-Dade, Broward, and Monroe Counties. Every donation supports our training programs and helps keep items out of landfills.

Thank you for being part of our mission!

Warmly,
The Goodwill South Florida Team
```

## For Azure Deployment

The email template file (`email_template.txt`) will be stored in the app's file system:
- **Local:** Saved in the project directory
- **Azure:** Saved in the app's ephemeral storage

**Important for Production:**
- Consider using Azure Blob Storage for persistent template storage
- Or store templates in a database
- Current implementation uses local file storage

## Troubleshooting

### Template Not Saving
- Check file permissions
- Ensure the app has write access to the directory
- Check browser console for errors

### Variables Not Replacing
- Make sure you use the exact variable names with curly braces
- Variables are case-sensitive: `{firstName}` not `{firstname}`

### Preview Not Updating
- The preview updates automatically as you type
- If it doesn't, try refreshing the page

## API Endpoints

For developers integrating with the system:

- `GET /api/email-template` - Get current template
- `POST /api/email-template` - Update template
- `POST /api/email-template/reset` - Reset to default

## Security Notes

- Only authorized users should access the settings page
- Consider adding authentication in production
- Template changes affect all future emails
- Test your template before saving

## Future Enhancements

Potential features to add:
- Multiple template versions
- A/B testing
- Template history/versioning
- Rich text editor
- Email preview with actual donor data
- Template library
