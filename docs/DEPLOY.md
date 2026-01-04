# 🚀 Deployment Guide

## Quick Start with Docker

### Prerequisites
- Docker Desktop installed
- 8GB RAM minimum (16GB recommended)
- 10GB free disk space

### Option 1: Docker Compose (Recommended)

**1. Clone the repository:**
```bash
git clone https://github.com/kitsakisGk/RAG-datachat-Assistant.git
cd RAG-datachat-Assistant
```

**2. Start all services:**
```bash
docker-compose up -d
```

**3. Access the application:**
- App: http://localhost:8501
- Ollama API: http://localhost:11434

**4. Stop services:**
```bash
docker-compose down
```

### Option 2: Docker Only

**1. Build the image:**
```bash
docker build -t rag-datachat .
```

**2. Run Ollama separately:**
```bash
docker run -d -p 11434:11434 --name ollama ollama/ollama
docker exec ollama ollama pull mistral
```

**3. Run the app:**
```bash
docker run -d -p 8501:8501 \
  --name rag-app \
  -e OLLAMA_BASE_URL=http://host.docker.internal:11434 \
  -v $(pwd)/data:/app/data \
  rag-datachat
```

## Cloud Deployment

### Railway.app

**1. Install Railway CLI:**
```bash
npm install -g @railway/cli
```

**2. Login and deploy:**
```bash
railway login
railway init
railway up
```

**3. Add Ollama service:**
- Go to Railway dashboard
- Add new service → Docker Image
- Image: `ollama/ollama:latest`
- Port: 11434
- Run: `ollama serve && ollama pull mistral`

**4. Configure environment:**
```
OLLAMA_BASE_URL=http://ollama.railway.internal:11434
```

### Fly.io

**1. Install Fly CLI:**
```bash
curl -L https://fly.io/install.sh | sh
```

**2. Launch app:**
```bash
fly launch
```

**3. Deploy:**
```bash
fly deploy
```

### DigitalOcean App Platform

**1. Connect GitHub repository**

**2. Configure build:**
- Type: Dockerfile
- Port: 8501

**3. Add environment variables:**
```
OLLAMA_BASE_URL=http://localhost:11434
```

**4. Deploy!**

## Environment Variables

```bash
# Ollama Configuration
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=mistral

# Application
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0

# Vector Database
CHROMA_PERSIST_DIR=/app/data/vector_store

# Logging
LOG_LEVEL=INFO
LOG_DIR=/app/logs
```

## Production Checklist

- [ ] Set up HTTPS (use nginx/caddy as reverse proxy)
- [ ] Configure authentication (Streamlit supports OAuth)
- [ ] Set up monitoring (Prometheus + Grafana)
- [ ] Configure backups for vector database
- [ ] Set resource limits in docker-compose.yml
- [ ] Use environment variables for secrets
- [ ] Set up CI/CD pipeline (GitHub Actions)
- [ ] Configure log aggregation (ELK stack)

## Performance Tuning

### For CPU-only deployments:
```yaml
# docker-compose.yml
services:
  ollama:
    deploy:
      resources:
        limits:
          cpus: '4'
          memory: 8G
```

### For GPU deployments:
```yaml
services:
  ollama:
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
```

## Troubleshooting

**Ollama not responding:**
```bash
docker logs rag-ollama
docker exec -it rag-ollama ollama list
```

**App can't connect to Ollama:**
- Check network: `docker network ls`
- Test connection: `curl http://ollama:11434/api/tags`

**Out of memory:**
- Increase Docker memory limit in Docker Desktop settings
- Use smaller model: `ollama pull phi` (1.3GB instead of 4.4GB)

## Monitoring

**View logs:**
```bash
docker-compose logs -f app
docker-compose logs -f ollama
```

**Check resource usage:**
```bash
docker stats
```

## Cost Estimates

### Self-Hosted (DigitalOcean)
- Droplet (4GB RAM): $24/month
- Droplet (8GB RAM): $48/month
- Droplet (16GB RAM): $96/month

### Managed (Railway/Fly.io)
- Hobby: $5-10/month
- Pro: $20-50/month
- Production: $100+/month

## Support

For issues and questions:
- GitHub Issues: https://github.com/kitsakisGk/RAG-datachat-Assistant/issues
- Email: kitsakisgk@gmail.com
