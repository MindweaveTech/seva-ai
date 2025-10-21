# Smart AI - Deployment Guide

## Production Deployment to seva-ai.mindweave.tech

This guide covers deploying the Smart AI application to your production server.

---

## Prerequisites

- Server with Docker and Docker Compose installed
- Domain: `seva-ai.mindweave.tech` pointing to server IP `4.213.183.139`
- Anthropic API key for Claude
- SSH access to the server

---

## Step-by-Step Deployment

### 1. **Setup DNS Record**

Create an A record pointing to your server:

```
seva-ai.mindweave.tech  →  4.213.183.139
```

### 2. **Clone Repository on Server**

```bash
ssh user@4.213.183.139

# Clone the repository
git clone https://github.com/MindweaveTech/seva-ai.git
cd seva-ai
```

### 3. **Configure Environment**

```bash
cd infrastructure/docker

# Copy and edit environment file
cp .env.example .env
nano .env
```

Add your API keys to `.env`:

```env
# PostgreSQL
POSTGRES_DB=seva_ai
POSTGRES_USER=seva_user
POSTGRES_PASSWORD=<strong_password_here>

# Redis
REDIS_PASSWORD=<strong_password_here>

# Backend API Keys
ANTHROPIC_API_KEY=<your_anthropic_api_key>
OPENAI_API_KEY=<your_openai_api_key>
SECRET_KEY=<generate_with_openssl_rand_hex_32>
```

Generate SECRET_KEY:
```bash
openssl rand -hex 32
```

### 4. **Start Services with Docker Compose**

```bash
# From infrastructure/docker directory
docker-compose -f docker-compose.dev.yml up -d --build
```

This starts:
- PostgreSQL (database)
- Weaviate (vector database)
- Redis (cache)
- Backend API (FastAPI)
- Nginx (reverse proxy on port 80)
- Adminer (database UI on port 8081)

### 5. **Verify Services**

```bash
# Check all containers are running
docker ps

# Should show:
# - seva-nginx
# - seva-backend
# - seva-postgres
# - seva-weaviate
# - seva-redis (may fail if port 6379 in use)
# - seva-adminer

# Check logs
docker logs seva-backend
docker logs seva-nginx
```

### 6. **Test API**

```bash
# Health check
curl http://seva-ai.mindweave.tech/health

# API docs
open http://seva-ai.mindweave.tech/docs
```

### 7. **Update Mobile App**

The mobile app is already configured to use `seva-ai.mindweave.tech`.

```bash
cd mobile-app
npm install
npm start
```

On your iPhone:
- Open Expo Go
- Scan QR code
- App will connect to `http://seva-ai.mindweave.tech/api/v1`

---

## Architecture

```
iPhone (Expo Go)
    ↓
http://seva-ai.mindweave.tech/api/v1
    ↓
Nginx (Port 80) - CORS, Reverse Proxy
    ↓
Backend API (Port 8000) - FastAPI
    ↓
PostgreSQL (Port 5432) - Database
```

---

## Firewall Configuration

Ensure these ports are open:

```bash
# Required
sudo ufw allow 80/tcp    # HTTP (Nginx)

# Optional - for direct access
sudo ufw allow 8000/tcp  # Backend API
sudo ufw allow 8081/tcp  # Adminer DB UI
sudo ufw allow 5432/tcp  # PostgreSQL (if remote access needed)
```

---

## SSL/HTTPS Setup (Recommended)

For production, add SSL certificate:

### Option 1: Let's Encrypt (Free)

```bash
# Install certbot
sudo apt install certbot python3-certbot-nginx

# Get certificate
sudo certbot --nginx -d seva-ai.mindweave.tech

# Auto-renewal
sudo certbot renew --dry-run
```

### Option 2: Update Nginx Config for HTTPS

Create `infrastructure/nginx/nginx-ssl.conf`:

```nginx
server {
    listen 80;
    server_name seva-ai.mindweave.tech;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name seva-ai.mindweave.tech;

    ssl_certificate /etc/letsencrypt/live/seva-ai.mindweave.tech/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/seva-ai.mindweave.tech/privkey.pem;

    # Rest of configuration...
}
```

Then update mobile app to use HTTPS:

```env
EXPO_PUBLIC_API_URL=https://seva-ai.mindweave.tech/api/v1
```

---

## Monitoring

### View Logs

```bash
# Backend logs
docker logs -f seva-backend

# Nginx logs
docker logs -f seva-nginx

# All services
docker-compose logs -f
```

### Database Access

Via Adminer: http://seva-ai.mindweave.tech:8081

- Server: `postgres`
- Username: `seva_user`
- Password: (from .env)
- Database: `seva_ai`

---

## Backup & Restore

### Backup Database

```bash
# Backup
docker exec seva-postgres pg_dump -U seva_user seva_ai > backup_$(date +%Y%m%d).sql

# Restore
docker exec -i seva-postgres psql -U seva_user seva_ai < backup_20251021.sql
```

### Backup Volumes

```bash
# PostgreSQL data
docker run --rm -v docker_postgres_data:/data -v $(pwd):/backup alpine tar czf /backup/postgres_backup.tar.gz /data

# Weaviate data
docker run --rm -v docker_weaviate_data:/data -v $(pwd):/backup alpine tar czf /backup/weaviate_backup.tar.gz /data
```

---

## Updating the Application

```bash
# Pull latest changes
git pull origin master

# Rebuild and restart
cd infrastructure/docker
docker-compose -f docker-compose.dev.yml up -d --build

# Check if database migrations are needed
docker exec seva-backend alembic upgrade head
```

---

## Troubleshooting

### Backend Won't Start

```bash
# Check logs
docker logs seva-backend

# Common issues:
# - Missing ANTHROPIC_API_KEY in .env
# - Database not ready (wait for postgres health check)
# - Port 8000 already in use
```

### Nginx Can't Connect to Backend

```bash
# Verify backend is running
docker ps | grep seva-backend

# Test backend directly
curl http://localhost:8000/health

# Check nginx logs
docker logs seva-nginx
```

### Mobile App Can't Connect

```bash
# Test from your phone's browser
http://seva-ai.mindweave.tech/health

# Check CORS headers
curl -H "Origin: http://localhost" -I http://seva-ai.mindweave.tech/health

# Verify .env has correct URL
cat mobile-app/.env
```

### Database Connection Issues

```bash
# Check postgres is running
docker exec seva-postgres pg_isready

# Test connection
docker exec seva-postgres psql -U seva_user -d seva_ai -c "SELECT 1"

# Check DATABASE_URL in backend
docker exec seva-backend env | grep DATABASE_URL
```

---

## Security Checklist

- [ ] Change default passwords in `.env`
- [ ] Generate strong SECRET_KEY
- [ ] Setup SSL/HTTPS with Let's Encrypt
- [ ] Configure firewall (ufw)
- [ ] Disable PostgreSQL remote access (port 5432)
- [ ] Use environment-specific API keys
- [ ] Setup automated backups
- [ ] Enable fail2ban for SSH protection
- [ ] Review Nginx security headers

---

## Performance Optimization

### For Production:

1. **Update docker-compose for production**
   - Remove volume mounts (use built images)
   - Set restart policies
   - Add resource limits

2. **Optimize Nginx**
   - Enable caching
   - Adjust worker_connections
   - Add rate limiting

3. **Database Tuning**
   - Configure connection pooling
   - Add indexes
   - Enable query optimization

4. **Backend**
   - Use gunicorn with multiple workers
   - Enable Redis caching
   - Configure async worker pool

---

## Current Status

✅ Infrastructure configured
✅ Nginx reverse proxy ready
✅ Backend Dockerized
✅ Mobile app configured for domain
⏳ SSL certificate (pending)
⏳ Production deployment (pending)

---

**Domain:** seva-ai.mindweave.tech
**Server IP:** 4.213.183.139
**Last Updated:** 2025-10-21
