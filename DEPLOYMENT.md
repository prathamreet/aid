# Railway Deployment Guide

## Quick Deployment Steps

### 1. Push to GitHub
```bash
git add .
git commit -m "Ready for Railway deployment"
git push origin main
```

### 2. Deploy on Railway
1. Go to [Railway.app](https://railway.app)
2. Sign up with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your `aid` repository
5. Railway will automatically detect it's a Python app

### 3. Set Environment Variables
In Railway dashboard, go to your project → Variables tab:

**Required Variables:**
```
SECRET_KEY=meow_meow
MONGO_HOST=mongodb+srv://prathamreetworkspace:SUVkozktC7ekjwJi@cluster0.lvwidjo.mongodb.net
MONGO_DB_NAME=production
```

**Optional Variables:**
```
PORT=8000
PYTHONPATH=/app
```

### 4. Deploy
- Railway will automatically build and deploy
- Your app will be available at: `https://your-app-name.railway.app`

## Configuration Files

### railway.json
- Configures build and deployment settings
- Uses Gunicorn for production server
- Sets up health checks

### Procfile (Backup)
- Alternative deployment configuration
- Used by some platforms as fallback

## Database Setup

### Production Database
Your app is configured to use:
- **Host:** MongoDB Atlas cluster
- **Database:** `production` (set via MONGO_DB_NAME)

### Important Notes
1. Make sure your MongoDB Atlas cluster allows connections from Railway IPs (0.0.0.0/0 or Railway-specific IPs)
2. Your connection string should include authentication credentials
3. Database name will be `production` (different from local `development`)

## Monitoring

### Railway Dashboard
- View logs in real-time
- Monitor resource usage
- Check deployment history
- Manage environment variables

### Health Check
- Endpoint: `/` (your home page)
- Railway will ping this every 100 seconds
- Automatic restarts on failure

## Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Check MongoDB Atlas IP whitelist
   - Verify connection string credentials
   - Ensure MONGO_DB_NAME is set correctly

2. **App Won't Start**
   - Check Railway logs for detailed error messages
   - Verify all required environment variables are set
   - Ensure requirements.txt includes all dependencies

3. **Static Files Issues**
   - Flask serves static files automatically in production
   - No additional configuration needed

### Logs Access
```bash
# View logs in Railway dashboard or use CLI
railway logs
```

## Custom Domain (Optional)

1. Go to Railway dashboard → Settings → Domains
2. Add your custom domain
3. Update DNS settings as instructed
4. Railway provides automatic SSL certificates

## Scaling

Railway automatically handles:
- Server scaling based on traffic
- Resource allocation
- Load balancing

For high-traffic applications, consider upgrading to Railway Pro for better performance and resources.