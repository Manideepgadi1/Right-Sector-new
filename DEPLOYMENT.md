# Right Sector VPS Deployment Guide

## Quick Deployment Commands

### Option 1: Automated Deployment (Recommended)

```bash
# SSH to server
ssh root@82.25.105.18

# Download and run deployment script
curl -o /tmp/deploy.sh https://raw.githubusercontent.com/Manideepgadi1/Right-Sector-new/main/deploy.sh
chmod +x /tmp/deploy.sh
/tmp/deploy.sh
```

### Option 2: Manual Deployment

```bash
# SSH to server
ssh root@82.25.105.18

# Navigate to deployment directory
cd /var/www/html/tools

# Remove old version if exists
rm -rf fundoscope

# Clone from GitHub
git clone https://github.com/Manideepgadi1/Right-Sector-new.git fundoscope

# Set permissions
chmod -R 755 fundoscope
chown -R www-data:www-data fundoscope
```

## Verify Deployment

```bash
# Check files
ls -la /var/www/html/tools/fundoscope

# Test access
curl http://82.25.105.18/tools/fundoscope/
```

## Access

After deployment, access at:
```
http://82.25.105.18/tools/fundoscope
```

## Update Deployment

To update with new changes:

```bash
ssh root@82.25.105.18
cd /var/www/html/tools/fundoscope
git pull origin main
```

## Troubleshooting

### Permission Issues
```bash
ssh root@82.25.105.18
chmod -R 755 /var/www/html/tools/fundoscope
chown -R www-data:www-data /var/www/html/tools/fundoscope
```

### Apache/Nginx Not Serving
```bash
# Apache
systemctl restart apache2
systemctl status apache2

# Nginx
systemctl restart nginx
systemctl status nginx
```

### Check Apache/Nginx Logs
```bash
# Apache
tail -f /var/log/apache2/error.log

# Nginx
tail -f /var/log/nginx/error.log
```

## Server Requirements

- Apache or Nginx web server
- Git installed
- Access to `/var/www/html/tools/` directory

## Port Configuration

Default deployment assumes:
- HTTP on port 80
- Access path: `/tools/fundoscope`

## Security Notes

- Ensure proper file permissions (755 for directories, 644 for files)
- Keep SSH access secure
- Regular backups recommended
