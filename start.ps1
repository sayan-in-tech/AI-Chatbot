Write-Host 'AI Chatbot Startup Script' -ForegroundColor Cyan
Write-Host '=========================' -ForegroundColor Cyan
Write-Host ''

# Step 1: Check and create virtual environment
Write-Host 'Step 1: Checking virtual environment...' -ForegroundColor Yellow
if (-not (Test-Path '.venv')) {
    Write-Host 'Creating virtual environment...' -ForegroundColor Yellow
    python -m venv .venv
    Write-Host 'Virtual environment created' -ForegroundColor Green
} else {
    Write-Host 'Virtual environment already exists' -ForegroundColor Green
}

# Step 2: Activate virtual environment
Write-Host ''
Write-Host 'Step 2: Activating virtual environment...' -ForegroundColor Yellow
. .\.venv\Scripts\Activate.ps1

# Step 3: Install/upgrade Python dependencies (idempotent)
Write-Host ''
Write-Host 'Step 3: Installing Python dependencies (if needed)...' -ForegroundColor Yellow
python -m pip install --upgrade pip
pip install -r requirements.txt
Write-Host 'Python dependencies ready' -ForegroundColor Green

# Step 4: Check/install npm dependencies
Write-Host ''
Write-Host 'Step 4: Checking npm dependencies...' -ForegroundColor Yellow
Push-Location 'frontend'
if (-not (Test-Path 'node_modules')) {
    Write-Host 'Installing npm dependencies...' -ForegroundColor Yellow
    npm install
    Write-Host 'npm dependencies installed' -ForegroundColor Green
} else {
    Write-Host 'npm dependencies already installed' -ForegroundColor Green
}
Pop-Location

# Step 5 & 6: Start backend and frontend
Write-Host ''
Write-Host 'Step 5: Starting servers...' -ForegroundColor Yellow
Write-Host ''

# Start backend in a new PowerShell window
Write-Host 'Starting Backend (http://127.0.0.1:8000)...' -ForegroundColor Cyan
Start-Process powershell -ArgumentList @(
    '-NoExit',
    '-Command',
    "Set-Location `"$PWD`"; .\\.venv\\Scripts\\Activate.ps1; python -m backend.run"
)

Start-Sleep -Seconds 2

# Start frontend in a new PowerShell window
Write-Host 'Starting Frontend (http://localhost:5173)...' -ForegroundColor Cyan
Start-Process powershell -ArgumentList @(
    '-NoExit',
    '-Command',
    "Set-Location `"$PWD\\frontend`"; npm run dev"
)

Write-Host ''
Write-Host 'Backend:  http://127.0.0.1:8000' -ForegroundColor Green
Write-Host 'Frontend: http://localhost:5173' -ForegroundColor Green
Write-Host 'Docs:     http://127.0.0.1:8000/docs' -ForegroundColor Green
Write-Host ''
Write-Host 'Both servers are running in separate windows.' -ForegroundColor Magenta

