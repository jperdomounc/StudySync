#!/bin/bash

# StudySync Setup Script - Prepares environment for deployment
set -e

echo "🔧 Setting up StudySync for production deployment..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_section() {
    echo -e "\n${BLUE}=== $1 ===${NC}\n"
}

# Generate secure JWT secret
generate_jwt_secret() {
    openssl rand -base64 32
}

# Generate secure passwords
generate_password() {
    openssl rand -base64 16
}

print_section "Environment Setup"

# Check if production env file exists
if [ -f ".env.production" ]; then
    print_warning ".env.production already exists. Backing up to .env.production.backup"
    cp .env.production .env.production.backup
fi

# Generate production environment file
print_status "Generating production environment file..."

cat > .env.production << EOF
# StudySync Production Environment Variables
# Generated on $(date)

# MongoDB Configuration
MONGO_ROOT_USERNAME=admin
MONGO_ROOT_PASSWORD=$(generate_password)
MONGODB_URL=mongodb://admin:$(generate_password)@mongodb:27017/studysync?authSource=admin
DATABASE_NAME=studysync

# JWT Configuration
JWT_SECRET_KEY=$(generate_jwt_secret)
JWT_ALGORITHM=HS256

# Server Configuration
HOST=0.0.0.0
PORT=8000
ENVIRONMENT=production

# CORS Configuration (UPDATE WITH YOUR DOMAIN)
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# Security
BCRYPT_ROUNDS=12

# API URL for frontend (UPDATE WITH YOUR DOMAIN)
API_URL=https://api.yourdomain.com

# Optional: Monitoring
LOG_LEVEL=INFO
EOF

print_status "✅ Production environment file created"

print_section "Docker Setup"

# Create necessary directories
print_status "Creating required directories..."
mkdir -p mongodb logs nginx/ssl

# Create .dockerignore files
print_status "Creating .dockerignore files..."

cat > backend/.dockerignore << EOF
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
.env
.env.*
.DS_Store
.git/
.gitignore
README.md
Dockerfile
.dockerignore
logs/
*.log
EOF

cat > frontend/.dockerignore << EOF
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*
.DS_Store
.env
.env.*
.git/
.gitignore
README.md
Dockerfile
.dockerignore
dist/
EOF

print_status "✅ Docker configuration completed"

print_section "Security Setup"

# Create nginx directory and basic SSL setup instructions
print_status "Setting up nginx configuration..."

mkdir -p nginx

cat > nginx/production.conf << EOF
events {
    worker_connections 1024;
}

http {
    upstream backend {
        server backend:8000;
    }
    
    upstream frontend {
        server frontend:80;
    }
    
    # Rate limiting
    limit_req_zone \$binary_remote_addr zone=api:10m rate=10r/s;
    limit_req_zone \$binary_remote_addr zone=login:10m rate=5r/m;
    
    server {
        listen 80;
        server_name yourdomain.com www.yourdomain.com;
        
        # Redirect HTTP to HTTPS
        return 301 https://\$server_name\$request_uri;
    }
    
    server {
        listen 443 ssl http2;
        server_name yourdomain.com www.yourdomain.com;
        
        # SSL Configuration (add your certificates)
        # ssl_certificate /etc/nginx/ssl/cert.pem;
        # ssl_certificate_key /etc/nginx/ssl/key.pem;
        
        # Security headers
        add_header X-Frame-Options DENY;
        add_header X-Content-Type-Options nosniff;
        add_header X-XSS-Protection "1; mode=block";
        
        # Frontend
        location / {
            proxy_pass http://frontend;
            proxy_set_header Host \$host;
            proxy_set_header X-Real-IP \$remote_addr;
        }
        
        # API
        location /api/ {
            limit_req zone=api burst=20 nodelay;
            proxy_pass http://backend/;
            proxy_set_header Host \$host;
            proxy_set_header X-Real-IP \$remote_addr;
            proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto \$scheme;
        }
        
        # Auth endpoints with stricter rate limiting
        location ~ ^/api/auth/(login|register) {
            limit_req zone=login burst=5 nodelay;
            proxy_pass http://backend;
            proxy_set_header Host \$host;
            proxy_set_header X-Real-IP \$remote_addr;
            proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto \$scheme;
        }
    }
}
EOF

print_status "✅ Nginx configuration created"

print_section "Final Steps"

# Create gitignore entries for sensitive files
if [ ! -f ".gitignore" ]; then
    touch .gitignore
fi

# Add production files to gitignore
grep -qxF ".env.production" .gitignore || echo ".env.production" >> .gitignore
grep -qxF "logs/" .gitignore || echo "logs/" >> .gitignore
grep -qxF "nginx/ssl/" .gitignore || echo "nginx/ssl/" >> .gitignore

print_status "✅ Updated .gitignore"

# Make scripts executable
chmod +x scripts/*.sh

print_status "✅ Made scripts executable"

print_section "Setup Complete!"

echo -e "${GREEN}🎉 StudySync is ready for production deployment!${NC}"
echo ""
echo "Next steps:"
echo "1. Update .env.production with your actual domain and MongoDB credentials"
echo "2. Set up SSL certificates in nginx/ssl/ directory"
echo "3. Update CORS_ORIGINS in .env.production with your domain"
echo "4. Run: ./scripts/deploy.sh to start deployment"
echo ""
print_warning "IMPORTANT: Review and update .env.production before deploying!"
print_warning "Never commit .env.production to version control!"