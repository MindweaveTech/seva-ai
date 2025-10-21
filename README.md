# Smart AI - AI-Powered Elderly Care Companion

> An empathetic AI companion system designed specifically for elderly care, featuring nurse-like persona, memory retention, health monitoring, and voice-first interface.

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-Phase%201%20Complete-green.svg)]()
[![Progress](https://img.shields.io/badge/progress-45%25-blue.svg)]()

---

## 🎉 What's Working Now (Phase 1 Complete!)

- ✅ **User Authentication** - Register, login, logout with JWT tokens
- ✅ **AI Chat** - Conversation with Claude 3.5 Sonnet (nurse persona)
- ✅ **Mobile App** - Complete UI with login, chat, and session management
- ✅ **Conversation History** - View and manage past conversations
- ✅ **Auto Token Refresh** - Seamless authentication experience
- ✅ **Test User** - Ready-to-use test account (see [TEST_USER.md](./TEST_USER.md))
- ✅ **API Documentation** - Interactive Swagger UI at `/docs`
- ✅ **Database** - PostgreSQL with 12 tables initialized

**Try it now:** Clone the repo, start Docker services, run the backend, and launch the mobile app!

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
| **[database/](./database/)** | PostgreSQL & Weaviate schemas | SQL, Python | ✅ Schema Complete |
| **[backend/](./backend/)** | API service, Claude AI integration | FastAPI, Python 3.11+ | ✅ Phase 1 Complete |
| **[mobile-app/](./mobile-app/)** | iOS/Android app for elderly users | React Native, Expo, TypeScript | ✅ Phase 1 Complete |
| **[admin-dashboard/](./admin-dashboard/)** | Caregiver monitoring portal | React, Vite, Tailwind CSS | 🚧 Scaffold Ready |
| **[infrastructure/](./infrastructure/)** | Docker Compose, CI/CD | Docker, GitHub Actions | ✅ Dev Environment Ready |

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
   docker-compose -f infrastructure/docker/docker-compose.dev.yml up -d
   # Starts PostgreSQL, Weaviate, Redis, Adminer
   ```

3. **Setup backend**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   cp .env.example .env
   # Add your ANTHROPIC_API_KEY to .env

   # Database is already initialized!
   # Or run: alembic upgrade head

   uvicorn app.main:app --reload
   # Backend runs at http://localhost:8000
   # API docs at http://localhost:8000/docs
   ```

4. **Setup mobile app**
   ```bash
   cd mobile-app
   npm install
   # Backend URL is pre-configured for localhost
   npm start  # Start Expo
   # Press 'i' for iOS or 'a' for Android
   ```

5. **Login with test user**
   ```
   Email:    test@smartai.com
   Password: TestPass123!
   ```

   See [TEST_USER.md](./TEST_USER.md) for details.

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
- **React Native** with Expo ~49.0 - Cross-platform mobile development
- **TypeScript** 5.1+ (strict mode) - Type safety
- **Zustand** 4.4+ - Lightweight state management
- **React Navigation** 6.1+ - Stack navigation
- **Axios** 1.6+ - HTTP client with interceptors
- **AsyncStorage** - Persistent token storage

### Backend Service
- **FastAPI** - Modern async Python web framework
- **SQLAlchemy** 2.0+ - ORM with async support
- **Pydantic** v2 - Data validation and settings
- **Alembic** - Database migrations
- **Anthropic Python SDK** - Claude API integration
- **Uvicorn** - ASGI server

### Databases
- **PostgreSQL** 15+ - Primary relational database (12 tables)
- **Weaviate** 1.22.4 - Vector database for RAG (Phase 2)
- **Redis** 7 - Caching and sessions (optional)

### AI/ML Services
- **Claude 3.5 Sonnet** (2024-10-22) - Latest Anthropic conversational AI
- **OpenAI Embeddings** - Text embeddings (Phase 2)
- **Expo AV** - Audio recording/playback (Phase 3)

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

### Phase 0: Foundation (Weeks 1-2) - ✅ **Complete**
- [x] Project setup and architecture
- [x] Development environment (Docker Compose)
- [x] Database initialization (12 tables)
- [x] CI/CD pipelines (GitHub Actions)
- [x] Backend/Mobile/Dashboard scaffolding

### Phase 1: Authentication & Chat (Weeks 3-4) - ✅ **Complete**
- [x] JWT authentication (access + refresh tokens)
- [x] User registration and login
- [x] Claude 3.5 Sonnet integration
- [x] Chat API with conversation history
- [x] Mobile UI (Login, Register, Chat, Sessions)
- [x] Navigation and state management
- [x] Auto token refresh
- [x] Test user created

### Phase 2: Memory System & RAG (Weeks 5-6) - 📝 **Planned**
- [ ] Weaviate vector database integration
- [ ] Conversation embeddings
- [ ] Semantic search
- [ ] Long-term memory retrieval

### Phase 3: Voice Integration (Weeks 7-8) - 📝 **Planned**
- [ ] Speech-to-text
- [ ] Text-to-speech
- [ ] Audio recording
- [ ] Voice commands

### Phase 4: Offline Support (Weeks 9-10) - 📝 **Planned**
- [ ] WatermelonDB integration
- [ ] Sync engine
- [ ] Offline message queue
- [ ] Conflict resolution

### Phase 5: Health Monitoring (Weeks 11-12) - 📝 **Planned**
- [ ] Health metrics tracking
- [ ] Sentiment analysis
- [ ] Pattern detection
- [ ] Caregiver alerts

### Phase 6: Admin Dashboard (Weeks 13-15) - 📝 **Planned**
- [ ] Dashboard UI implementation
- [ ] User management
- [ ] Health monitoring visualization
- [ ] Analytics and reporting

### Phase 7-10: Security, Testing, Production (Weeks 16-20) - 📝 **Planned**
- [ ] Comprehensive testing
- [ ] Security hardening
- [ ] HIPAA compliance audit
- [ ] Production deployment

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
