# Use a minimal Python base image
FROM python:3.12-slim-bookworm

# Set non-interactive mode to avoid prompts during installation
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    git \
    wget \
    gpg \
    ffmpeg \
    coreutils \
    ca-certificates \
    bash \
    build-essential \
    libgl1 \
    apt-transport-https \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js and npm from the official source
RUN curl -fsSL https://deb.nodesource.com/setup_22.x | bash - && \
    apt-get install -y nodejs && \
    npm install -g prettier@3.4.2 && \
    rm -rf /var/lib/apt/lists/*

# Add Microsoft GPG Key & Repository for VS Code
RUN wget -qO- https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > /etc/apt/trusted.gpg.d/microsoft.gpg && \
    echo "deb [arch=amd64] https://packages.microsoft.com/repos/code stable main" > /etc/apt/sources.list.d/vscode.list && \
    apt-get update

# Install VS Code
RUN apt-get install -y code && rm -rf /var/lib/apt/lists/*

# Upgrade pip and install Python dependencies
RUN python3 -m pip install --no-cache-dir --upgrade pip setuptools wheel && \
    python3 -m pip install --no-cache-dir \
    fastapi \
    uvicorn \
    jellyfish \
    pandas \
    numpy \
    bs4 \
    # beautifulsoup4 \
    -U yt_dlp \
    requests \
    feedparser \
    pdfplumber \
    Pillow \
    pydub \
    whisper \
    python-dotenv \
    python-dateutil \
    pycountry \
    python-multipart

# Create and set working directory
WORKDIR /app

# Copy application files
COPY main.py .
COPY llm_functions.py .
COPY llm_tools_functions_calls.py .
COPY server.py .

# Expose the application port
EXPOSE 5000

# Set default command to start the FastAPI server with Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]
