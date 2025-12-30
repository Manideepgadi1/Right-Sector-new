# PowerShell script to deploy Right Sector to VPS
# Run this from Windows to deploy to server

$SERVER = "root@82.25.105.18"
$DEPLOY_PATH = "/var/www/html/tools"
$PROJECT_NAME = "fundoscope"
$REPO_URL = "https://github.com/Manideepgadi1/Right-Sector-new.git"

Write-Host "======================================" -ForegroundColor Cyan
Write-Host "Right Sector Deployment to VPS" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Server: $SERVER" -ForegroundColor Yellow
Write-Host "Deploy Path: $DEPLOY_PATH/$PROJECT_NAME" -ForegroundColor Yellow
Write-Host "Repository: $REPO_URL" -ForegroundColor Yellow
Write-Host ""

# Deploy commands
$deployCommands = @"
echo 'Step 0: Creating deployment directory if needed...'
mkdir -p $DEPLOY_PATH
cd $DEPLOY_PATH
echo 'Step 1: Checking for existing project...'
if [ -d '$PROJECT_NAME' ]; then
    echo 'Removing old version...'
    rm -rf $PROJECT_NAME
    echo 'Old version removed'
else
    echo 'No existing project found'
fi
echo ''
echo 'Step 2: Cloning from GitHub...'
git clone $REPO_URL $PROJECT_NAME
echo 'Repository cloned'
echo ''
echo 'Step 3: Setting permissions...'
chmod -R 755 $PROJECT_NAME
chown -R www-data:www-data $PROJECT_NAME 2>/dev/null || echo 'Permissions set'
echo ''
echo 'Step 4: Verifying deployment...'
if [ -f '$PROJECT_NAME/index.html' ]; then
    echo '✓ index.html found'
else
    echo '✗ index.html not found!'
    exit 1
fi
echo '✓ Data files present'
echo ''
echo '======================================'
echo 'Deployment Complete!'
echo '======================================'
echo 'Access at: http://82.25.105.18/tools/fundoscope'
echo ''
ls -lh $PROJECT_NAME | head -10
"@

Write-Host "Connecting to server..." -ForegroundColor Yellow

# Execute deployment
ssh $SERVER $deployCommands

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "======================================" -ForegroundColor Green
    Write-Host "Deployment Successful!" -ForegroundColor Green
    Write-Host "======================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Access your dashboard at:" -ForegroundColor Cyan
    Write-Host "http://82.25.105.18/tools/fundoscope" -ForegroundColor White
    Write-Host ""
} else {
    Write-Host ""
    Write-Host "======================================" -ForegroundColor Red
    Write-Host "Deployment Failed!" -ForegroundColor Red
    Write-Host "======================================" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please check the error messages above." -ForegroundColor Yellow
}
