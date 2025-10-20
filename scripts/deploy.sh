#!/bin/bash

# StudySync Production Deployment Script
set -e

echo "🚀 Starting StudySync deployment..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
PROJECT_NAME="studysync"
DOCKER_COMPOSE_FILE="docker-compose.production.yml"

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if required files exist
check_requirements() {
    print_status "Checking deployment requirements..."
    
    if [ ! -f ".env.production" ]; then
        print_error ".env.production file not found!"
        print_status "Please create .env.production with your production environment variables"
        exit 1
    fi
    
    if [ ! -f "$DOCKER_COMPOSE_FILE" ]; then
        print_error "$DOCKER_COMPOSE_FILE not found!"
        exit 1
    fi
    
    # Check if Docker is running
    if ! docker info > /dev/null 2>&1; then
        print_error "Docker is not running. Please start Docker and try again."
        exit 1
    fi
    
    print_status "✅ All requirements met"
}

# Build and deploy
deploy() {
    print_status "Building and deploying $PROJECT_NAME..."
    
    # Load production environment variables
    export $(cat .env.production | xargs)
    
    # Stop existing containers
    print_status "Stopping existing containers..."
    docker-compose -f $DOCKER_COMPOSE_FILE down || true
    
    # Build new images
    print_status "Building new images..."
    docker-compose -f $DOCKER_COMPOSE_FILE build --no-cache
    
    # Start services
    print_status "Starting services..."
    docker-compose -f $DOCKER_COMPOSE_FILE up -d
    
    # Wait for services to be ready
    print_status "Waiting for services to start..."
    sleep 10
    
    # Health check
    check_health
}

# Health check function
check_health() {
    print_status "Performing health checks..."
    
    # Check backend health
    if curl -f http://localhost:8000/health > /dev/null 2>&1; then
        print_status "✅ Backend is healthy"
    else
        print_error "❌ Backend health check failed"
        show_logs
        exit 1
    fi
    
    # Check frontend
    if curl -f http://localhost:3000/health > /dev/null 2>&1; then
        print_status "✅ Frontend is healthy"
    else
        print_warning "Frontend health check failed (this may be normal)"
    fi
    
    print_status "🎉 Deployment completed successfully!"
    print_status "Services are available at:"
    print_status "  - Frontend: http://localhost:3000"
    print_status "  - Backend API: http://localhost:8000"
    print_status "  - API Docs: http://localhost:8000/docs"
}

# Show container logs
show_logs() {
    print_status "Showing recent logs..."
    docker-compose -f $DOCKER_COMPOSE_FILE logs --tail=50
}

# Cleanup function
cleanup() {
    print_status "Cleaning up old images and containers..."
    docker system prune -f
    print_status "Cleanup completed"
}

# Main execution
main() {
    case "${1:-deploy}" in
        "deploy")
            check_requirements
            deploy
            ;;
        "logs")
            show_logs
            ;;
        "stop")
            print_status "Stopping all services..."
            docker-compose -f $DOCKER_COMPOSE_FILE down
            ;;
        "restart")
            print_status "Restarting services..."
            docker-compose -f $DOCKER_COMPOSE_FILE restart
            ;;
        "cleanup")
            cleanup
            ;;
        "status")
            docker-compose -f $DOCKER_COMPOSE_FILE ps
            ;;
        *)
            echo "Usage: $0 {deploy|logs|stop|restart|cleanup|status}"
            echo ""
            echo "Commands:"
            echo "  deploy   - Build and deploy the application (default)"
            echo "  logs     - Show application logs"
            echo "  stop     - Stop all services"
            echo "  restart  - Restart all services"
            echo "  cleanup  - Clean up old Docker images"
            echo "  status   - Show service status"
            exit 1
            ;;
    esac
}

# Execute main function with all arguments
main "$@"