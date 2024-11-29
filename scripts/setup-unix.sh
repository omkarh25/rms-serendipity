#!/bin/bash

echo "Setting up RMS (Rating Management System)"
echo "========================================"

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "Error: Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "Error: Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Create necessary directories
echo "Creating necessary directories..."
mkdir -p backend/uploads
mkdir -p frontend/public

# Create .env file for backend if it doesn't exist
if [ ! -f backend/.env ]; then
    echo "Creating backend .env file..."
    cat > backend/.env << EOL
DEBUG=True
DATABASE_URL=postgresql://postgres:postgres@db:5432/rms
SECRET_KEY=your-secret-key-here
LOG_LEVEL=INFO
EOL
fi

# Create .env file for frontend if it doesn't exist
if [ ! -f frontend/.env ]; then
    echo "Creating frontend .env file..."
    cat > frontend/.env << EOL
NEXT_PUBLIC_API_URL=https://rms-docs.theserendipity.org/api/v1
EOL
fi

# Set execute permissions for scripts
chmod +x scripts/*.sh

echo "Starting Docker containers..."
docker-compose up -d

# Wait for database to be ready
echo "Waiting for database to be ready..."
sleep 10

echo "Setup completed successfully!"
echo ""
echo "You can now access:"
echo "- Frontend: https://rms-docs.theserendipity.org"
echo "- Backend API: https://rms-docs.theserendipity.org/api/v1"
echo "- API Documentation: https://rms-docs.theserendipity.org/docs"
echo ""
echo "To stop the services, run: docker-compose down"
echo "To view logs, run: docker-compose logs -f"
