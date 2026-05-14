# WidgetProject Auth

A full-stack authentication application combining a **React/Vite frontend** with a **FastAPI backend** integrated with **WorkOS** for secure user authentication and management.

## Project Overview

WidgetProject Auth is a modern web application demonstrating enterprise-grade authentication implementation. It provides a seamless authentication experience using WorkOS's AuthKit, allowing secure user login and session management.

## Architecture

```
WidgetProject_Auth/
├── workos/
│   ├── backend/          # FastAPI backend server
│   │   ├── main.py       # Main application & API routes
│   │   └── requirements.txt
│   └── frontend/         # React frontend application
│       ├── src/
│       │   ├── App.jsx
│       │   ├── main.jsx
│       │   └── index.css
│       ├── package.json
│       ├── vite.config.js
│       └── eslint.config.js
```

## Tech Stack

### Backend
- **FastAPI** - Modern, fast Python web framework
- **WorkOS** - Enterprise authentication & user management
- **CORS Middleware** - Cross-origin request handling

### Frontend
- **React 19** - UI library
- **Vite** - Fast build tool and dev server
- **Axios** - HTTP client
- **ESLint** - Code quality

## Getting Started

### Prerequisites
- Python 3.8+
- Node.js 16+
- WorkOS account with API credentials

### Environment Setup

Create a `.env` file in the backend directory with:
```env
WORKOS_API_KEY=your_api_key
WORKOS_CLIENT_ID=your_client_id
FRONTEND_URL=http://localhost:5173
BACKEND_URL=http://localhost:8000
WORKOS_COOKIE_PASSWORD=your_cookie_password
```

### Backend Setup
```bash
cd workos/backend
pip install -r requirements.txt
uvicorn main:app --reload
```

The backend server will be available at `http://localhost:8000`

### Frontend Setup
```bash
cd workos/frontend
npm install
npm run dev
```

The frontend application will be available at `http://localhost:5173`

## Available Scripts

### Backend
- `uvicorn main:app --reload` - Start development server with hot reload

### Frontend
- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run lint` - Run ESLint
- `npm run preview` - Preview production build

## API Endpoints

- `GET /auth/login` - Initiates WorkOS login flow
- `GET /auth/callback` - Handles OAuth callback from WorkOS

## Authentication Flow

1. User clicks "Login" on the frontend
2. Frontend redirects to `/auth/login` endpoint
3. Backend redirects to WorkOS authorization URL
4. User authenticates via WorkOS
5. WorkOS redirects back to `/auth/callback`
6. Backend creates secure session
7. User is logged in

## Dependencies

### Backend
- fastapi
- python-dotenv
- workos
- uvicorn

### Frontend
- react
- react-dom
- axios
- vite

## Development

### Code Quality
- Run linter: `npm run lint` (frontend)
- Fix linting issues: `npm run lint -- --fix` (frontend)

### Building for Production

Frontend:
```bash
npm run build
```

Backend:
```bash
# Deploy with production ASGI server (e.g., Gunicorn)
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
```

## Contributing

1. Create a feature branch
2. Make your changes
3. Ensure code passes linting
4. Commit with clear messages
5. Push and create a pull request

## Environment Variables Reference

| Variable | Description |
|----------|-------------|
| `WORKOS_API_KEY` | WorkOS API key for backend authentication |
| `WORKOS_CLIENT_ID` | WorkOS client ID for OAuth flow |
| `FRONTEND_URL` | Frontend application URL (for CORS) |
| `BACKEND_URL` | Backend application URL |
| `WORKOS_COOKIE_PASSWORD` | Password for secure session cookies |

## License

This project is provided as-is for educational and development purposes.

## Support

For WorkOS documentation, visit: https://workos.com/docs
