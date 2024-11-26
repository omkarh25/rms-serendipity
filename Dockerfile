FROM python:3.11-slim

# Accept build arguments
ARG NEXT_PUBLIC_BASE_URL
# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV TZ=Asia/Kolkata
ENV NODE_ENV=development
ENV NEXT_PUBLIC_BASE_URL=${NEXT_PUBLIC_BASE_URL}

# Install dependencies with proper error handling and package lists update
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    libmagic1 \
    libffi-dev \
    libssl-dev \
    libxml2-dev \
    libxslt1-dev \
    python3-dev \
    python3-pip \
    python3-venv \
    tzdata \
    supervisor && \
    # Install Node.js using curl
    curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && \
    apt-get install -y nodejs && \
    # Clean up
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    # Verify installations
    node --version && \
    npm --version

# Set working directory
WORKDIR /app

# Copy the entire application code
COPY . .

# Copy supervisord configuration file explicitly
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Install Python dependencies
RUN pip3 install --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

# Install frontend dependencies and build
WORKDIR /app/frontend
RUN npm install && \
    npm install -D tailwindcss postcss autoprefixer && \
    npm install -D @types/node @types/react @types/react-dom typescript

# Setup backend directory
WORKDIR /app/backend
RUN mkdir -p /app/backend

# Create a non-root user
RUN useradd -m -U app_user && \
    chown -R app_user:app_user /app

# Set the writing permissions for the app_user
RUN chown -R app_user:app_user /app

# Set working directory back to root
WORKDIR /app

# Expose ports for frontend and backend
EXPOSE 8056 8057

# Switch to non-root user
USER app_user

# Command to start supervisord
CMD ["supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
