# Smart AI - AI-Powered Elderly Care Companion

> An empathetic AI companion system designed specifically for elderly care, featuring nurse-like persona, memory retention, health monitoring, and voice-first interface.

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-in%20development-yellow.svg)]()

---

## Overview

Smart AI provides elderly individuals with a compassionate, intelligent companion that enhances their quality of life through:

- 🗣️ **Voice-First Interface** - Natural conversation via speech
- 🧠 **Memory Retention** - Remembers past conversations and context
- 💊 **Health Monitoring** - Tracks health signals from conversations
- 👨‍⚕️ **Caregiver Integration** - Alerts and insights for family/caregivers
- 📱 **Offline-First** - Works without constant internet connection
- 🔒 **HIPAA Compliant** - Enterprise-grade security and privacy

---

## Project Structure

```
seva-ai/
├── docs/                       # Comprehensive documentation
├── database/                   # Database schemas and migrations
├── backend/                    # FastAPI backend service
├── mobile-app/                 # React Native mobile application
├── admin-dashboard/            # Caregiver web dashboard
├── shared/                     # Shared code and types
├── infrastructure/             # DevOps and deployment configs
├── .github/workflows/          # CI/CD pipelines
├── PLAN.md                     # Project roadmap
└── TASKS.md                    # Task breakdown
```

### Service Overview

| Directory | Description | Tech Stack | Status |
|-----------|-------------|------------|--------|
| **[docs/](./docs/)** | Architecture, API docs, guides | Markdown | ✅ Complete |
| **[database/](./database/)** | PostgreSQL & Weaviate schemas | SQL, Python | 📝 Planned |
| **[backend/](./backend/)** | API service, RAG, health monitoring | FastAPI, Python | 📝 Planned |
| **[mobile-app/](./mobile-app/)** | iOS/Android app for elderly users | React Native, TypeScript | 📝 Planned |
| **[admin-dashboard/](./admin-dashboard/)** | Caregiver monitoring portal | React, TypeScript | 📝 Planned |
| **[shared/](./shared/)** | Shared types and constants | TypeScript | 📝 Planned |
| **[infrastructure/](./infrastructure/)** | Kubernetes, Docker, CI/CD | K8s, Docker | 📝 Planned |

---

## Quick Start

### Prerequisites

- **Node.js** 18+ (for mobile app and dashboard)
- **Python** 3.11+ (for backend)
- **Docker** & **Docker Compose** (for local development)
- **PostgreSQL** 15+ (or use Docker)
- **Weaviate** (or use Docker)

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/MindweaveTech/seva-ai.git
   cd seva-ai
   ```

2. **Start infrastructure services**
   ```bash
   cd infrastructure/docker
   docker-compose up -d
   # Starts PostgreSQL, Weaviate, Redis
   ```

3. **Setup backend**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   cp .env.example .env
   # Edit .env with your API keys
   alembic upgrade head  # Run migrations
   python -m app.main    # Start server
   ```

4. **Setup mobile app**
   ```bash
   cd mobile-app
   npm install
   cp .env.example .env
   # Edit .env with backend URL
   npm start  # Start Expo
   ```

5. **Setup admin dashboard**
   ```bash
   cd admin-dashboard
   npm install
   cp .env.example .env
   npm run dev  # Start dev server
   ```

---

## Documentation

### Core Documentation
- **[Architecture Guide](./docs/ARCHITECTURE.md)** - Complete system architecture
- **[Implementation Guide](./docs/IMPLEMENTATION_GUIDE.md)** - Step-by-step development guide
- **[Database Setup](./docs/DATABASE_SETUP.md)** - Database schemas and migrations
- **[Technical Summary](./docs/TECHNICAL_SUMMARY.md)** - Quick reference guide

### Project Management
- **[Project Plan](./PLAN.md)** - Roadmap, timeline, team structure
- **[Task Breakdown](./TASKS.md)** - Detailed task list (300+ tasks)

### Service-Specific Docs
- [Backend README](./backend/README.md)
- [Mobile App README](./mobile-app/README.md)
- [Admin Dashboard README](./admin-dashboard/README.md)
- [Database README](./database/README.md)

---

## Technology Stack

### Mobile Application
- **React Native** with Expo - Cross-platform mobile development
- **TypeScript** - Type safety
- **WatermelonDB** - Local offline database
- **Zustand** - State management
- **React Navigation** - Navigation

### Backend Service
- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - ORM with async support
- **Pydantic** - Data validation
- **Alembic** - Database migrations

### Databases
- **PostgreSQL** - Primary relational database
- **Weaviate** - Vector database for RAG
- **Redis** - Caching and sessions

### AI/ML Services
- **Claude API** (Anthropic) - Conversational AI
- **OpenAI Embeddings** - Text embeddings
- **Google Cloud Speech** - STT/TTS

### Infrastructure
- **Kubernetes** - Container orchestration
- **Docker** - Containerization
- **GitHub Actions** - CI/CD
- **Prometheus & Grafana** - Monitoring

---

## Key Features

### For Elderly Users
- 🎙️ **Voice Conversation** - Speak naturally, get voice responses
- 💭 **Memory** - AI remembers your health history and preferences
- 🏥 **Health Tracking** - Gentle monitoring through conversation
- 📵 **Offline Mode** - Works without internet connection
- 🌙 **Daily Check-ins** - Regular wellness conversations
- 🚨 **Emergency Support** - Quick access to caregivers

### For Caregivers
- 📊 **Health Dashboard** - Monitor patient wellness
- 🔔 **Smart Alerts** - Get notified of concerning patterns
- 📈 **Health Trends** - Visualize health metrics over time
- 💬 **Conversation Summaries** - Review key discussion points
- 👥 **Multi-Patient Management** - Monitor multiple elderly users
- 📱 **Mobile & Web Access** - Check in from anywhere

---

## Development Roadmap

### Phase 0: Foundation (Weeks 1-2) - **In Progress**
- [x] Project setup and architecture
- [ ] Development environment
- [ ] Database initialization
- [ ] CI/CD pipelines

### Phase 1: Authentication & Chat (Weeks 3-4)
- [ ] User authentication system
- [ ] Basic chat functionality
- [ ] Claude API integration
- [ ] Mobile chat UI

### Phase 2: Memory & RAG (Weeks 5-6)
- [ ] Embedding generation
- [ ] Vector database integration
- [ ] RAG pipeline
- [ ] User profile management

### Phase 3: Voice (Week 7)
- [ ] Speech-to-text integration
- [ ] Text-to-speech integration
- [ ] Voice UI components

### Phase 4: Offline Support (Week 8)
- [ ] Local database
- [ ] Sync engine
- [ ] Offline capabilities

### Phase 5: Health Monitoring (Weeks 9-10)
- [ ] Health metrics tracking
- [ ] Pattern detection
- [ ] Caregiver alerts

### Phase 6: Admin Dashboard (Weeks 11-13)
- [ ] Dashboard foundation
- [ ] User management
- [ ] Health monitoring UI
- [ ] Analytics

### Phase 7-10: Security, Testing, Deployment, Launch (Weeks 14-20)

See [PLAN.md](./PLAN.md) for detailed roadmap.

---

## Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Workflow
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Code Standards
- **Backend:** Python 3.11+, Black formatting, 90%+ test coverage
- **Frontend:** TypeScript strict mode, ESLint, 85%+ test coverage
- **Commits:** Conventional Commits format
- **PRs:** Require 1+ approval, all tests passing

---

## Team

### Core Team
- **Backend Engineers** - API development, database, RAG pipeline
- **Mobile Engineers** - React Native app, offline sync
- **Frontend Engineer** - Admin dashboard
- **ML Engineer** - RAG optimization, health analytics
- **DevOps Engineer** - Infrastructure, CI/CD, monitoring
- **QA Engineer** - Testing, quality assurance

See [PLAN.md](./PLAN.md) for detailed team structure.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Security

Security is paramount when handling health data. We follow industry best practices:

- 🔐 **Encryption at rest** (AES-256)
- 🔒 **Encryption in transit** (TLS 1.3)
- 🎫 **JWT authentication** with refresh tokens
- 📝 **Audit logging** for all sensitive operations
- 🛡️ **HIPAA compliance** framework
- 🔍 **Regular security audits**

**Report security vulnerabilities:** security@mindweavetech.com (or use GitHub Security Advisories)

---

## Support

- **Documentation:** [docs/](./docs/)
- **Issues:** [GitHub Issues](https://github.com/MindweaveTech/seva-ai/issues)
- **Discussions:** [GitHub Discussions](https://github.com/MindweaveTech/seva-ai/discussions)
- **Email:** support@mindweavetech.com

---

## Acknowledgments

- **Anthropic** - Claude API for empathetic AI conversations
- **OpenAI** - Embedding models for semantic search
- **Google Cloud** - Speech services
- **React Native Community** - Mobile framework and ecosystem
- **FastAPI Community** - Modern Python web framework

---

## Status

**Current Phase:** Phase 0 - Foundation & Architecture ✅
**Next Milestone:** Development environment setup
**Timeline:** 20-week MVP development
**Last Updated:** 2025-10-20

---

<p align="center">
  <strong>Built with ❤️ by MindweaveTech</strong><br>
  Making elderly care more compassionate through AI
</p>
