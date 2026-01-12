# Installation & Deployment Guide

Complete step-by-step instructions for installing and deploying the Disruption Management System.

## 📑 Table of Contents

- [System Requirements](#system-requirements)
- [Development Installation](#development-installation)
- [Production Deployment](#production-deployment)
- [Docker Deployment](#docker-deployment)
- [Cloud Deployment](#cloud-deployment)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)
- [Maintenance](#maintenance)

---

## System Requirements

### Minimum Requirements

- **OS:** macOS, Linux, or Windows
- **Python:** 3.9 or higher
- **RAM:** 2GB minimum
- **Disk:** 500MB for application + data
- **Internet:** For package downloads

### Recommended Setup

- **OS:** Ubuntu 20.04 LTS or macOS 10.15+
- **Python:** 3.11+
- **RAM:** 4GB+
- **Disk:** 2GB+ SSD
- **CPU:** 2+ cores

### Optional Dependencies

- **Ollama:** For AI recommendations (v0.1.0+)
  - Download: https://ollama.ai
  - Models: mistral, neural-chat, etc.

---

## Development Installation

### Step 1: Clone Repository

```bash
git clone https://github.com/RahulGosavi94/hack-ai-thon.git
cd hack-ai-thon
```

### Step 2: Create Python Virtual Environment

**On macOS/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**On Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**Verify activation:**
```bash
which python  # Should show path to .venv
```

### Step 3: Upgrade pip

```bash
pip install --upgrade pip setuptools wheel
```

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

**Contents of requirements.txt:**
```
Flask==3.1.3
python-dotenv==1.0.0
requests==2.31.0
```

### Step 5: Set Environment Variables

Create `.env` file:

```bash
cat > .env << EOF
# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=dev-secret-key-change-in-production
FLASK_APP=app.py

# Ollama Configuration (optional)
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=mistral
OLLAMA_ENABLED=True

# Application Configuration
APP_PORT=5000
APP_HOST=127.0.0.1
EOF
```

### Step 6: Initialize Data

```bash
# Generate test data
python3 generate_data.py

# Or load existing data
python3 load_data.py
```

### Step 7: Verify Installation

```bash
# Run tests
python3 test_eligibility.py
python3 test_delay_reconciliation.py

# Check Flask app starts
python3 app.py
```

**Expected output:**
```
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
```

### Step 8: Access Application

Open browser and navigate to:
```
http://localhost:5000
```

---

## Production Deployment

### Pre-Deployment Checklist

- [ ] Code reviewed and tested
- [ ] All tests passing
- [ ] Environment variables configured
- [ ] Dependencies locked (requirements.txt)
- [ ] Database backups created
- [ ] Security review completed

### Step 1: Update Configuration

Edit `.env` for production:

```bash
cat > .env.production << EOF
# Flask Configuration
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=your-very-secure-random-key-here-min-32-chars
FLASK_APP=app.py

# Ollama Configuration
OLLAMA_URL=https://ollama.yourcompany.com
OLLAMA_MODEL=mistral
OLLAMA_ENABLED=True

# Application Configuration
APP_PORT=5000
APP_HOST=0.0.0.0
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database Configuration (if using Cosmos DB)
COSMOS_DB_URL=your-cosmos-db-connection-string
COSMOS_DB_KEY=your-cosmos-db-key
EOF
```

### Step 2: Optimize Application

Update `app.py` for production:

```python
# Enable caching
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 31536000

# Disable debug mode
app.config['DEBUG'] = False
app.config['TESTING'] = False

# Enable compression
from flask_compress import Compress
Compress(app)

# Configure logging
import logging
from logging.handlers import RotatingFileHandler
import os

if not os.path.exists('logs'):
    os.mkdir('logs')

file_handler = RotatingFileHandler('logs/app.log', 
    maxBytes=10240000, backupCount=10)
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
file_handler.setLevel(logging.INFO)
app.logger.addHandler(file_handler)
```

### Step 3: Use Production WSGI Server

**Install Gunicorn:**
```bash
pip install gunicorn
```

**Create `wsgi.py`:**
```python
from app import app

if __name__ == "__main__":
    app.run()
```

**Run with Gunicorn:**
```bash
# Single worker
gunicorn -w 1 -b 0.0.0.0:5000 wsgi:app

# Multiple workers (for production)
gunicorn -w 4 -b 0.0.0.0:5000 \
    --worker-class=sync \
    --worker-connections=1000 \
    --max-requests=1000 \
    --timeout=60 \
    wsgi:app
```

### Step 4: Set Up Reverse Proxy (Nginx)

Create `/etc/nginx/sites-available/hack-ai-thon`:

```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;

    # SSL certificates (use Let's Encrypt)
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-Frame-Options "SAMEORIGIN" always;

    # Proxy to Gunicorn
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
    }

    # Static files
    location /static/ {
        alias /var/www/hack-ai-thon/static/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
}
```

**Enable site:**
```bash
sudo ln -s /etc/nginx/sites-available/hack-ai-thon \
    /etc/nginx/sites-enabled/

# Test configuration
sudo nginx -t

# Reload
sudo systemctl reload nginx
```

### Step 5: Set Up Systemd Service

Create `/etc/systemd/system/hack-ai-thon.service`:

```ini
[Unit]
Description=Disruption Management System
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/hack-ai-thon

Environment="PATH=/var/www/hack-ai-thon/.venv/bin"
ExecStart=/var/www/hack-ai-thon/.venv/bin/gunicorn \
    -w 4 -b 127.0.0.1:5000 wsgi:app

Restart=on-failure
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

**Start service:**
```bash
sudo systemctl daemon-reload
sudo systemctl start hack-ai-thon
sudo systemctl enable hack-ai-thon

# Check status
sudo systemctl status hack-ai-thon
```

---

## Docker Deployment

### Create Dockerfile

```dockerfile
# Multi-stage build
FROM python:3.11-slim as builder

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Production stage
FROM python:3.11-slim

WORKDIR /app

# Copy Python dependencies from builder
COPY --from=builder /root/.local /root/.local

# Copy application code
COPY . .

# Set environment variables
ENV PATH=/root/.local/bin:$PATH
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=app.py

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:5000/health')"

# Expose port
EXPOSE 5000

# Start application
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "--timeout", "60", "wsgi:app"]
```

### Create Docker Compose

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
      - OLLAMA_URL=http://ollama:11434
    depends_on:
      - ollama
    restart: unless-stopped

  ollama:
    image: ollama/ollama:latest
    ports:
      - "11434:11434"
    volumes:
      - ollama_data:/root/.ollama
    environment:
      - OLLAMA_HOST=0.0.0.0:11434
    restart: unless-stopped

  nginx:
    image: nginx:latest
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/nginx/ssl:ro
    depends_on:
      - web
    restart: unless-stopped

volumes:
  ollama_data:
```

### Build and Run

```bash
# Build Docker image
docker build -t hack-ai-thon:latest .

# Run with Docker Compose
docker-compose up -d

# Check logs
docker-compose logs -f web

# Stop
docker-compose down
```

---

## Cloud Deployment

### Azure App Service

```bash
# Install Azure CLI
brew install azure-cli  # macOS
# or download from https://aka.ms/azcli

# Login to Azure
az login

# Create resource group
az group create --name hack-ai-thon-rg \
    --location eastus

# Create App Service Plan
az appservice plan create \
    --name hack-ai-thon-plan \
    --resource-group hack-ai-thon-rg \
    --sku B1

# Create web app
az webapp create \
    --name hack-ai-thon-app \
    --resource-group hack-ai-thon-rg \
    --plan hack-ai-thon-plan \
    --runtime "python|3.11"

# Deploy from Git
az webapp deployment source config-zip \
    --resource-group hack-ai-thon-rg \
    --name hack-ai-thon-app \
    --src deploy.zip
```

### AWS EC2

```bash
# Launch EC2 instance
aws ec2 run-instances \
    --image-id ami-0c55b159cbfafe1f0 \
    --instance-type t2.micro \
    --security-groups hack-ai-thon

# Connect to instance
ssh -i your-key.pem ec2-user@your-instance-ip

# Install dependencies
sudo yum update -y
sudo yum install -y python3 python3-pip

# Deploy application
git clone https://github.com/RahulGosavi94/hack-ai-thon.git
cd hack-ai-thon
pip3 install -r requirements.txt
python3 -m gunicorn -w 4 -b 0.0.0.0:5000 wsgi:app
```

### Heroku

```bash
# Install Heroku CLI
brew tap heroku/brew && brew install heroku

# Login
heroku login

# Create app
heroku create hack-ai-thon

# Add Procfile
echo "web: gunicorn wsgi:app" > Procfile

# Deploy
git push heroku main

# View logs
heroku logs -t
```

---

## Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `FLASK_ENV` | development | Flask environment mode |
| `FLASK_DEBUG` | True | Debug mode (disable in production) |
| `SECRET_KEY` | dev-key | Session secret (change in production) |
| `OLLAMA_URL` | http://localhost:11434 | Ollama server URL |
| `OLLAMA_MODEL` | mistral | LLM model name |
| `APP_PORT` | 5000 | Flask server port |
| `APP_HOST` | 127.0.0.1 | Flask server host |

### Database Configuration

For production, migrate to Azure Cosmos DB:

```python
from azure.cosmos import CosmosClient

# Connection
client = CosmosClient.from_connection_string(
    os.getenv('COSMOS_DB_CONNECTION_STRING')
)
database = client.get_database_client('hack-ai-thon')
```

### Logging Configuration

```python
import logging
from logging.handlers import RotatingFileHandler

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        RotatingFileHandler('app.log', maxBytes=10485760, backupCount=10),
        logging.StreamHandler()
    ]
)
```

---

## Troubleshooting

### Port Already in Use

```bash
# Find process using port 5000
lsof -i :5000

# Kill process
kill -9 <PID>

# Or use different port
python3 app.py --port 8000
```

### Virtual Environment Issues

```bash
# Deactivate current env
deactivate

# Remove and recreate
rm -rf .venv
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Ollama Connection Failed

```bash
# Check if Ollama is running
curl http://localhost:11434

# Start Ollama
ollama serve

# Verify model is loaded
ollama list

# Pull model if needed
ollama pull mistral
```

### Database Connection Issues

```bash
# Test database connection
python3 -c "import app; print(app.db_status())"

# Check logs
tail -f logs/app.log
```

---

## Maintenance

### Regular Backups

```bash
# Backup data directory
tar -czf backups/data-$(date +%Y%m%d).tar.gz test_data/

# Keep 30 days of backups
find backups -name "data-*.tar.gz" -mtime +30 -delete
```

### Log Management

```bash
# Rotate logs
logrotate -f /etc/logrotate.d/hack-ai-thon

# View recent logs
tail -n 100 logs/app.log

# Search logs
grep "ERROR" logs/app.log
```

### Performance Monitoring

```bash
# Monitor resource usage
watch -n 1 'ps aux | grep gunicorn'

# Check response times
curl -w "Time: %{time_total}s\n" http://localhost:5000/api/flights
```

### Update Dependencies

```bash
# Check for updates
pip list --outdated

# Update specific package
pip install --upgrade Flask

# Update all
pip install --upgrade -r requirements.txt
```

---

## Security Checklist

- [ ] Change `SECRET_KEY` in production
- [ ] Enable HTTPS/SSL
- [ ] Set `FLASK_DEBUG=False`
- [ ] Configure firewall rules
- [ ] Enable CORS for trusted domains only
- [ ] Validate all user inputs
- [ ] Use environment variables for secrets
- [ ] Regular security updates
- [ ] Monitor logs for suspicious activity
- [ ] Implement rate limiting

---

## Performance Tuning

### Database Optimization

```python
# Add indexes for common queries
db.passengers.create_index([('flight_id', 1)])
db.passengers.create_index([('tier', 1)])
db.disruptions.create_index([('flight_id', 1)])
```

### Caching

```python
from flask_caching import Cache

cache = Cache(app, config={
    'CACHE_TYPE': 'simple',
    'CACHE_DEFAULT_TIMEOUT': 300
})

@app.route('/api/flights')
@cache.cached(timeout=300)
def get_flights():
    # Cached response
```

### Load Balancing

```nginx
upstream backend {
    server 127.0.0.1:5001;
    server 127.0.0.1:5002;
    server 127.0.0.1:5003;
}

server {
    location / {
        proxy_pass http://backend;
    }
}
```

---

## Next Steps

1. Deploy to development environment
2. Run comprehensive tests
3. Deploy to staging environment
4. Load testing and optimization
5. Deploy to production
6. Monitor and maintain

---

**Last Updated:** January 12, 2026  
**Version:** 1.0.0
