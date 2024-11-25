# Setup script for RMS (Rating Management System) on Windows
Write-Host "Setting up RMS (Rating Management System)" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green

# Check if Docker is installed
if (!(Get-Command docker -ErrorAction SilentlyContinue)) {
    Write-Host "Error: Docker is not installed. Please install Docker Desktop for Windows first." -ForegroundColor Red
    exit 1
}

# Check if Docker is running
$dockerStatus = docker info 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: Docker is not running. Please start Docker Desktop." -ForegroundColor Red
    exit 1
}

# Create necessary directories
Write-Host "Creating necessary directories..." -ForegroundColor Yellow
New-Item -ItemType Directory -Force -Path "backend\uploads" | Out-Null
New-Item -ItemType Directory -Force -Path "frontend\public" | Out-Null

# Create .env file for backend if it doesn't exist
if (!(Test-Path "backend\.env")) {
    Write-Host "Creating backend .env file..." -ForegroundColor Yellow
    @"
DEBUG=True
DATABASE_URL=postgresql://postgres:postgres@db:5432/rms
SECRET_KEY=your-secret-key-here
ALLOWED_ORIGINS=http://localhost:3000
LOG_LEVEL=INFO
"@ | Out-File -FilePath "backend\.env" -Encoding UTF8
}

# Create .env file for frontend if it doesn't exist
if (!(Test-Path "frontend\.env")) {
    Write-Host "Creating frontend .env file..." -ForegroundColor Yellow
    @"
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
"@ | Out-File -FilePath "frontend\.env" -Encoding UTF8
}

# Start Docker containers
Write-Host "Starting Docker containers..." -ForegroundColor Yellow
docker-compose up -d

# Wait for database to be ready
Write-Host "Waiting for database to be ready..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

Write-Host "`nSetup completed successfully!" -ForegroundColor Green
Write-Host "`nYou can now access:"
Write-Host "- Frontend: http://localhost:3000" -ForegroundColor Cyan
Write-Host "- Backend API: http://localhost:8000" -ForegroundColor Cyan
Write-Host "- API Documentation: http://localhost:8000/docs" -ForegroundColor Cyan

Write-Host "`nUseful commands:"
Write-Host "- To stop the services: docker-compose down" -ForegroundColor Yellow
Write-Host "- To view logs: docker-compose logs -f" -ForegroundColor Yellow

# Add error handling for common issues
if ($LASTEXITCODE -ne 0) {
    Write-Host "`nError: Something went wrong during setup." -ForegroundColor Red
    Write-Host "Common solutions:" -ForegroundColor Yellow
    Write-Host "1. Make sure Docker Desktop is running"
    Write-Host "2. Check if ports 3000 and 8000 are available"
    Write-Host "3. Try running 'docker-compose down' and then run this script again"
    exit 1
}
