#!/bin/bash
# Preserve settings files during Azure deployment

SETTINGS_DIR="/home/site/persistent_settings"
FILES_TO_PRESERVE=(
    "donation_locations.json"
    "form_title.txt"
    "email_template.txt"
)

# Create persistent directory if it doesn't exist
mkdir -p "$SETTINGS_DIR"

# Before deployment: Backup existing settings
if [ "$1" == "backup" ]; then
    echo "Backing up settings..."
    for file in "${FILES_TO_PRESERVE[@]}"; do
        if [ -f "/home/site/wwwroot/$file" ]; then
            cp "/home/site/wwwroot/$file" "$SETTINGS_DIR/$file"
            echo "Backed up: $file"
        fi
    done
fi

# After deployment: Restore settings
if [ "$1" == "restore" ]; then
    echo "Restoring settings..."
    for file in "${FILES_TO_PRESERVE[@]}"; do
        if [ -f "$SETTINGS_DIR/$file" ]; then
            cp "$SETTINGS_DIR/$file" "/home/site/wwwroot/$file"
            echo "Restored: $file"
        fi
    done
fi
