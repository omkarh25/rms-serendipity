# RMS (Rating Management System)

A sophisticated rating management system built for Dhoom Studios to facilitate content creation with focus on truthfulness, entertainment, and philosophical aspects.

## Vision

RMS is based on the concept of "Mathu-Kathe" (two ears, one mouth - Hear all, Speak effectively). It helps in long-term creative content generation through three main components:

1. **Truthfulness**: Content with unbiased source references
2. **Entertainment**: Based on Navarasa model of emotions
3. **Philosophy**: Content evaluation through gender, race, and religious perspectives

## Tech Stack

- Frontend: NextJS with shadcn/ui and Tailwind CSS
- Backend: FastAPI
- Database: PostgreSQL
- Deployment: Docker

## Prerequisites

- Node.js (v18+)
- Python (v3.8+)
- Docker and Docker Compose
- PostgreSQL

## Project Structure

```
rms-serendipity/
├── frontend/          # NextJS frontend application
├── backend/           # FastAPI backend application
├── docs/             # Project documentation
├── scripts/          # Setup and utility scripts
├── tests/            # Test suites
└── docker-compose.yml # Docker compose configuration
```

## Local Development Setup

### Using Scripts

#### Windows
```bash
./scripts/setup-windows.sh
```

#### Linux/Mac
```bash
./scripts/setup-unix.sh
```

### Manual Setup

1. **Frontend Setup**
```bash
cd frontend
npm install
npm run dev
```

2. **Backend Setup**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

3. **Database Setup**
```bash
docker-compose up -d db
```

## Docker Deployment

```bash
docker-compose up -d
```

## Testing

```bash
# Frontend tests
cd frontend && npm test

# Backend tests
cd backend && pytest

# Load tests
cd tests && python -m pytest load_tests/
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is proprietary and owned by Dhoom Studios.
