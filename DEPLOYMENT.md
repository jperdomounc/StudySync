# StudySync Production Deployment Guide

This guide covers deploying StudySync to production using Docker containers.

## Quick Start

1. **Setup Environment**
   ```bash
   ./scripts/setup.sh
   ```

2. **Configure Production Variables**
   ```bash
   # Edit the generated .env.production file
   nano .env.production
   ```

3. **Deploy**
   ```bash
   ./scripts/deploy.sh
   ```

## Detailed Deployment Steps

### 1. Prerequisites

- Docker and Docker Compose installed
- Domain name configured (optional but recommended)
- SSL certificates (for HTTPS)
- MongoDB Atlas account (recommended for production database)

### 2. Environment Configuration

The setup script generates a `.env.production` file with secure defaults. **You must update:**

- `CORS_ORIGINS`: Your production domain(s)
- `MONGODB_URL`: Your MongoDB connection string
- `API_URL`: Your API endpoint URL
- Domain names in `nginx/production.conf`

### 3. Database Options

#### Option A: MongoDB Atlas (Recommended)
1. Create a MongoDB Atlas cluster
2. Update `MONGODB_URL` in `.env.production`
3. Whitelist your server's IP address

#### Option B: Self-hosted MongoDB
- Use the included MongoDB container
- Ensure proper backup and security measures

### 4. SSL/HTTPS Setup

1. Obtain SSL certificates (Let's Encrypt recommended):
   ```bash
   # Using Certbot
   sudo certbot certonly --standalone -d yourdomain.com
   ```

2. Copy certificates to `nginx/ssl/` directory
3. Update nginx configuration with certificate paths

### 5. Deployment Commands

```bash
# Full deployment
./scripts/deploy.sh

# View logs
./scripts/deploy.sh logs

# Stop services
./scripts/deploy.sh stop

# Restart services
./scripts/deploy.sh restart

# Check status
./scripts/deploy.sh status

# Cleanup old images
./scripts/deploy.sh cleanup
```

## Production Checklist

### Security
- [ ] JWT secret key is randomly generated (32+ characters)
- [ ] Database credentials are secure
- [ ] CORS origins are restricted to your domain
- [ ] SSL certificates are configured
- [ ] Rate limiting is enabled
- [ ] Security headers are configured

### Performance
- [ ] Database indexes are created
- [ ] Frontend assets are minified and compressed
- [ ] Docker images are optimized
- [ ] Health checks are configured
- [ ] Monitoring is set up

### Monitoring
- [ ] Health endpoints respond correctly
- [ ] Log aggregation is configured
- [ ] Error tracking is set up
- [ ] Uptime monitoring is configured

## Architecture

```
Internet → Nginx (Port 80/443)
           ↓
           Frontend Container (Port 3000)
           ↓
           Backend Container (Port 8000)
           ↓
           MongoDB Container/Atlas
```

## Scaling

### Horizontal Scaling
- Use Docker Swarm or Kubernetes for container orchestration
- Add multiple backend instances with load balancing
- Use Redis for session storage across instances

### Database Scaling
- MongoDB Atlas auto-scaling
- Read replicas for read-heavy workloads
- Database sharding for very large datasets

## Backup Strategy

### Database Backups
```bash
# Automated MongoDB backup
docker exec mongodb mongodump --out /backup/$(date +%Y%m%d_%H%M%S)
```

### Application Backups
- Code is version-controlled (Git)
- Environment files should be securely backed up
- Docker images can be rebuilt from source

## Monitoring and Maintenance

### Health Checks
- Backend: `GET /health`
- Frontend: `GET /health` 
- Database: Included in backend health check

### Log Locations
- Backend: `docker logs studysync-backend`
- Frontend: `docker logs studysync-frontend`
- Database: `docker logs studysync-mongodb`

### Updates
1. Pull latest code
2. Rebuild images: `docker-compose build`
3. Deploy: `./scripts/deploy.sh`
4. Verify health checks pass

## Troubleshooting

### Common Issues

**Services won't start**
- Check Docker daemon is running
- Verify environment variables are correct
- Check port availability

**Database connection fails**
- Verify MongoDB is running
- Check connection string format
- Ensure network connectivity

**Frontend can't reach backend**
- Check CORS configuration
- Verify API URL in frontend build
- Check network connectivity between containers

### Getting Help

1. Check service logs: `./scripts/deploy.sh logs`
2. Verify service status: `./scripts/deploy.sh status`
3. Test health endpoints manually
4. Check Docker network configuration

## Security Considerations

### Production Security Measures
- Use HTTPS only
- Implement rate limiting
- Regular security updates
- Monitor for unusual activity
- Use secrets management
- Regular backup testing

### Environment Variables
Never commit these files:
- `.env.production`
- SSL certificates
- Database credentials
- Any files with secrets

## Performance Optimization

### Database
- Ensure proper indexing
- Monitor query performance
- Use connection pooling
- Implement caching where appropriate

### Frontend
- Assets are minified and compressed
- Implement CDN for static assets
- Use browser caching headers
- Optimize images and resources

### Backend
- Use production ASGI server (Uvicorn)
- Implement response caching
- Monitor memory usage
- Use connection pooling