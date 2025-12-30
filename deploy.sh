#!/bin/bash

# Right Sector Deployment Script
# Deploy to: http://82.25.105.18/tools/fundoscope

echo "=================================="
echo "Right Sector Deployment Script"
echo "=================================="
echo ""

# Configuration
DEPLOY_PATH="/var/www/html/tools"
PROJECT_NAME="fundoscope"
REPO_URL="https://github.com/Manideepgadi1/Right-Sector-new.git"
FULL_PATH="$DEPLOY_PATH/$PROJECT_NAME"

# Step 1: Check if tools directory exists
echo "Step 1: Checking deployment directory..."
if [ ! -d "$DEPLOY_PATH" ]; then
    echo "Creating $DEPLOY_PATH..."
    mkdir -p "$DEPLOY_PATH"
fi

# Step 2: Navigate to deployment directory
cd "$DEPLOY_PATH" || exit 1
echo "✓ In directory: $(pwd)"
echo ""

# Step 3: Check if old project exists
echo "Step 2: Checking for existing project..."
if [ -d "$PROJECT_NAME" ]; then
    echo "Found existing project at $FULL_PATH"
    echo "Removing old version..."
    rm -rf "$PROJECT_NAME"
    echo "✓ Old version removed"
else
    echo "No existing project found"
fi
echo ""

# Step 4: Clone from GitHub
echo "Step 3: Cloning from GitHub..."
echo "Repository: $REPO_URL"
git clone "$REPO_URL" "$PROJECT_NAME"

if [ $? -eq 0 ]; then
    echo "✓ Successfully cloned repository"
else
    echo "✗ Failed to clone repository"
    exit 1
fi
echo ""

# Step 5: Set permissions
echo "Step 4: Setting permissions..."
chmod -R 755 "$FULL_PATH"
chown -R www-data:www-data "$FULL_PATH" 2>/dev/null || echo "Note: Could not set www-data ownership (may need to run as root)"
echo "✓ Permissions set"
echo ""

# Step 6: Verify deployment
echo "Step 5: Verifying deployment..."
if [ -f "$FULL_PATH/index.html" ]; then
    echo "✓ index.html found"
else
    echo "✗ index.html not found!"
    exit 1
fi

if [ -f "$FULL_PATH/data/indices_with_short_names.json" ]; then
    echo "✓ Data file found"
else
    echo "✗ Data file not found!"
    exit 1
fi
echo ""

# Step 7: Summary
echo "=================================="
echo "Deployment Summary"
echo "=================================="
echo "Status: SUCCESS ✓"
echo "Location: $FULL_PATH"
echo "Access URL: http://82.25.105.18/tools/fundoscope"
echo ""
echo "Files deployed:"
ls -lh "$FULL_PATH" | head -10
echo ""
echo "=================================="
echo "Deployment Complete!"
echo "=================================="
