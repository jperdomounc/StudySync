# StudySync Cloud Deployment Guide
**Vercel + Railway + MongoDB Atlas**

Deploy StudySync to the cloud with this modern, scalable stack that costs ~$0-25/month.

## 🚀 Quick Deploy Links

- **Frontend**: [![Deploy to Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2Fyourusername%2FStudySync%2Ftree%2Fmain%2Ffrontend)
- **Backend**: [![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template/new?template=https%3A%2F%2Fgithub.com%2Fyourusername%2FStudySync%2Ftree%2Fmain%2Fbackend)

## 📋 Prerequisites

1. GitHub repository with your StudySync code
2. Accounts on:
   - [Vercel](https://vercel.com) (Frontend hosting)
   - [Railway](https://railway.app) (Backend hosting) 
   - [MongoDB Atlas](https://cloud.mongodb.com) (Database hosting)

## 🗄️ Step 1: MongoDB Atlas Setup

### Create Database
1. Go to [MongoDB Atlas](https://cloud.mongodb.com)
2. Create a new cluster (free tier is fine for development)
3. Choose **AWS**, **Google Cloud**, or **Azure** as provider
4. Select the **M0 Sandbox** (free tier)

### Configure Database Access
1. **Database Access** → **Add New Database User**
   ```
   Username: studysync
   Password: [Generate secure password]
   Built-in Role: Read and write to any database
   ```

2. **Network Access** → **Add IP Address**
   ```
   For Railway: Add 0.0.0.0/0 (allow from anywhere)
   Or add specific Railway IPs for better security
   ```

### Get Connection String
1. **Database** → **Connect** → **Connect your application**
2. Copy connection string:
   ```
   mongodb+srv://studysync:<password>@cluster0.xxxxx.mongodb.net/studysync?retryWrites=true&w=majority
   ```

## 🚂 Step 2: Railway Backend Deployment

### Deploy to Railway
1. Go to [Railway](https://railway.app)
2. Click **New Project** → **Deploy from GitHub repo**
3. Select your StudySync repository
4. Choose the `backend` folder as the root directory

### Environment Variables
Add these variables in Railway Dashboard → Variables:

```env
# Database
MONGODB_URL=mongodb+srv://studysync:YOUR_PASSWORD@cluster0.xxxxx.mongodb.net/studysync?retryWrites=true&w=majority
DATABASE_NAME=studysync

# Security (generate a secure 32+ character secret)
JWT_SECRET_KEY=your-super-secure-jwt-secret-key-at-least-32-characters-long
JWT_ALGORITHM=HS256

# Server
HOST=0.0.0.0
ENVIRONMENT=production

# CORS (will be your Vercel domain)
CORS_ORIGINS=https://your-app-name.vercel.app

# Security
BCRYPT_ROUNDS=12
```

### Generate JWT Secret
```bash
# Generate secure JWT secret (run locally)
openssl rand -base64 32
```

### Deploy
1. Railway will auto-deploy from your GitHub repo
2. Note your Railway app URL: `https://your-app.up.railway.app`
3. Test health endpoint: `https://your-app.up.railway.app/health`

## 🚢 Step 3: Vercel Frontend Deployment

### Deploy to Vercel
1. Go to [Vercel](https://vercel.com)
2. Click **New Project** → **Import Git Repository**
3. Select your StudySync repository
4. Set **Framework Preset**: Vite
5. Set **Root Directory**: `frontend`

### Environment Variables
Add in Vercel Dashboard → Settings → Environment Variables:

```env
REACT_APP_API_URL=https://your-railway-app.up.railway.app
```

### Build Settings
Vercel should auto-detect, but verify:
```
Build Command: npm run vercel-build
Output Directory: dist
Install Command: npm install
```

### Deploy
1. Click **Deploy** 
2. Vercel will build and deploy your frontend
3. Note your Vercel app URL: `https://your-app.vercel.app`

## 🔗 Step 4: Connect Services

### Update Backend CORS
1. Go to Railway → Your Backend → Variables
2. Update `CORS_ORIGINS` with your Vercel URL:
   ```
   CORS_ORIGINS=https://your-app.vercel.app,https://yourdomain.com
   ```

### Test Full Stack
1. Visit your Vercel app URL
2. Try registering with a UNC email
3. Check Railway logs if issues occur

## 🎛️ Configuration Summary

### Costs (Monthly)
- **MongoDB Atlas**: $0 (M0 free tier)
- **Railway**: $0-20 (500 hours free, then $0.000463/GB-hour)
- **Vercel**: $0 (hobby plan)
- **Total**: ~$0-20/month

### URLs
- **Frontend**: `https://your-app.vercel.app`
- **Backend API**: `https://your-backend.up.railway.app` 
- **API Docs**: `https://your-backend.up.railway.app/docs`

## 🔧 Environment Variables Cheat Sheet

### Railway (Backend)
```env
MONGODB_URL=mongodb+srv://...
DATABASE_NAME=studysync
JWT_SECRET_KEY=32+_character_secret_key
JWT_ALGORITHM=HS256
HOST=0.0.0.0
ENVIRONMENT=production
CORS_ORIGINS=https://your-app.vercel.app
BCRYPT_ROUNDS=12
```

### Vercel (Frontend)  
```env
REACT_APP_API_URL=https://your-railway-backend.up.railway.app
```

## 🔍 Monitoring & Maintenance

### Health Checks
- **Backend**: `https://your-backend.up.railway.app/health`
- **Frontend**: Check Vercel deployments dashboard
- **Database**: MongoDB Atlas monitoring dashboard

### Logs
- **Railway**: Dashboard → Deployments → View Logs
- **Vercel**: Dashboard → Functions → View Function Logs  
- **MongoDB**: Atlas → Database → Monitoring

### Updates
1. **Automatic**: Both Railway and Vercel auto-deploy on git push
2. **Manual**: Trigger rebuilds from respective dashboards
3. **Database**: Atlas handles maintenance automatically

## 🚨 Troubleshooting

### Common Issues

**Backend won't start**
```bash
# Check Railway logs for errors
# Common fixes:
# 1. Verify MONGODB_URL format
# 2. Check MongoDB Atlas IP whitelist
# 3. Verify environment variables are set
```

**Frontend can't reach backend**
```bash
# Check CORS configuration
# 1. Verify CORS_ORIGINS in Railway includes Vercel URL
# 2. Check REACT_APP_API_URL in Vercel points to Railway
# 3. Ensure Railway service is running
```

**Database connection failed**
```bash
# MongoDB Atlas issues:
# 1. Check connection string format
# 2. Verify database user credentials
# 3. Check network access (IP whitelist)
# 4. Ensure database exists
```

### Getting Help
1. **Railway**: Check deployment logs
2. **Vercel**: Check function logs
3. **MongoDB**: Check connection logs
4. Test endpoints manually with curl/Postman

## 🔐 Security Best Practices

### Production Security
- ✅ Use HTTPS only (automatic with Vercel/Railway)
- ✅ Secure JWT secret (32+ characters)
- ✅ Restrict CORS origins to your domains
- ✅ Use MongoDB Atlas (managed security)
- ✅ Regular dependency updates

### Monitoring
- Set up MongoDB Atlas alerts
- Monitor Railway resource usage
- Use Vercel Analytics for frontend metrics
- Implement error tracking (Sentry recommended)

## 📈 Scaling

### Traffic Growth
- **Frontend**: Vercel automatically scales
- **Backend**: Railway auto-scales with usage
- **Database**: MongoDB Atlas auto-scaling available

### Performance Optimization
- Enable Vercel Edge Functions for faster responses
- Use Railway's built-in caching
- Implement MongoDB indexes (already included)
- Consider CDN for static assets

## 🎯 Going Live Checklist

- [ ] MongoDB Atlas cluster created and configured
- [ ] Railway backend deployed and healthy
- [ ] Vercel frontend deployed and accessible
- [ ] Environment variables configured on all platforms
- [ ] CORS properly configured
- [ ] Database connection working
- [ ] Authentication flow working
- [ ] Custom domain configured (optional)
- [ ] SSL certificates active (automatic)
- [ ] Monitoring and alerts set up

**🎉 Your StudySync application is now live and ready for UNC students!**