# SecureSight

SecureSight is a comprehensive web application designed to enhance cybersecurity operations through automated scanning, analysis, and monitoring.

## ✨ Features

- 🔐 **Secure Authentication** - JWT-based authentication with auto-logout
- 🎯 **Automated Scanning** - Quick, deep, and passive reconnaissance modes
- 🍯 **Honeypot Integration** - Monitor Dionaea and Cowrie honeypots
- 🔬 **Malware Analysis** - Static analysis with YARA signatures
- 📊 **Real-time Dashboard** - Live statistics and monitoring
- 🎨 **Modern UI** - Glassmorphism design with dark theme
- 🚀 **Fast & Responsive** - Built with React + FastAPI

## 🏗️ Structure

- **backend/** - FastAPI application for API and orchestration
- **frontend/** - React application (Vite + TypeScript) for the user interface
- **honeypots/** - Honeypot configurations (Cowrie, Dionaea)
- **scripts/** - Utility scripts for automation

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose (recommended)
- Node.js 18+ (for local frontend dev)
- Python 3.10+ (for local backend dev)
- MySQL or PostgreSQL database

### Option 1: Using Scripts (Windows - Easiest)

```bash
# Install dependencies
install.bat

# Start development servers
start-dev.bat
```

### Option 2: Using Docker (Recommended)

```bash
docker-compose up --build
```

Access the application:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Option 3: Local Development

#### Backend
```bash
cd backend
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload
```

#### Frontend
```bash
cd frontend
npm install
npm run dev
```

## 📚 Documentation

- **[SETUP.md](SETUP.md)** - Comprehensive setup and troubleshooting guide
- **[QUICKREF.md](QUICKREF.md)** - Quick reference for common commands
- **[FIXES.md](FIXES.md)** - Detailed list of all fixes and improvements
- **[ANALYSIS.md](ANALYSIS.md)** - Complete analysis and fix report

## 🔧 Configuration

### Backend Environment Variables

Create `backend/.env`:

```env
DATABASE_URL=mysql+aiomysql://root:password@localhost:3306/securesight
SECRET_KEY=your-super-secret-key-change-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=30
KAFKA_BOOTSTRAP_SERVERS=localhost:9092
```

### Frontend Environment Variables

Create `frontend/.env`:

```env
VITE_API_URL=http://localhost:8000/api/v1
```

## 🎨 Design System

- **Primary Color:** Cyan (#06b6d4)
- **Theme:** Dark mode optimized for security operations
- **Style:** Glassmorphism with animated backgrounds
- **Typography:** Modern sans-serif with monospace for code

## 🔒 Security Features

- ✅ JWT-based authentication
- ✅ Password hashing with bcrypt
- ✅ CORS protection
- ✅ Request timeout protection
- ✅ Auto-logout on token expiry
- ✅ Input validation
- ✅ Secure user registration

## 🛠️ Technology Stack

### Backend
- FastAPI - Modern Python web framework
- SQLAlchemy - ORM for database operations
- Alembic - Database migrations
- JWT - Authentication tokens
- Celery - Async task processing
- Redis - Caching and message broker

### Frontend
- React 18 - UI library
- TypeScript - Type safety
- Vite - Build tool
- Tailwind CSS - Styling
- Axios - HTTP client
- React Router - Navigation

## 📊 API Endpoints

### Authentication
- `POST /api/v1/login/access-token` - Login
- `GET /api/v1/users/me` - Get current user

### Users
- `POST /api/v1/users/` - Register new user
- `GET /api/v1/users/` - List users (admin only)

### Scans
- `GET /api/v1/scans/` - List scans
- `POST /api/v1/scans/` - Create new scan

### Honeypots
- `GET /api/v1/honeypots/logs` - Get honeypot logs

### Analysis
- `POST /api/v1/analysis/upload` - Upload file for analysis

## 🐛 Troubleshooting

See [SETUP.md](SETUP.md) for detailed troubleshooting guide.

Common issues:
- **CORS errors:** Ensure frontend is on port 5173 or 3000
- **Cannot connect:** Check if backend is running on port 8000
- **Registration fails:** Verify database connection and migrations
- **Styles not loading:** Run `npm install` to install Tailwind

## 🧪 Testing

```bash
# Test backend health
curl http://localhost:8000/health

# Access API documentation
open http://localhost:8000/docs
```

## 📦 Building for Production

### Frontend
```bash
cd frontend
npm run build
```

### Backend
```bash
cd backend
pip install gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- FastAPI for the excellent web framework
- React team for the UI library
- Tailwind CSS for the styling system
- All open-source contributors

## 📞 Support

For issues and questions:
1. Check the documentation in the `docs/` folder
2. Review [SETUP.md](SETUP.md) for setup issues
3. Check [QUICKREF.md](QUICKREF.md) for quick commands
4. Review API documentation at `/docs`

---

**Built with ❤️ for cybersecurity professionals**
