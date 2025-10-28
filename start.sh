#!/bin/bash
# AI Chatbot Startup Script

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m' # No Color

echo -e "${CYAN}AI Chatbot Startup Script${NC}"
echo -e "${CYAN}============================${NC}"
echo ""

# Step 1: Check and create virtual environment
echo -e "${YELLOW}Step 1: Checking virtual environment...${NC}"
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
    echo -e "${GREEN}Virtual environment created${NC}"
else
    echo -e "${GREEN}Virtual environment already exists${NC}"
fi

# Step 2: Activate virtual environment
echo ""
echo -e "${YELLOW}Step 2: Activating virtual environment...${NC}"
source .venv/bin/activate

# Step 3: Check if requirements are installed
echo ""
echo -e "${YELLOW}Step 3: Checking Python dependencies...${NC}"

# Check if key packages are installed
python3 -c "import fastapi, uvicorn" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Installing requirements..."
    pip install --upgrade pip
    pip install -r requirements.txt
    echo -e "${GREEN}Requirements installed${NC}"
else
    echo -e "${GREEN}Requirements already installed${NC}"
fi

# Step 4: Check if npm dependencies are installed
echo ""
echo -e "${YELLOW}Step 4: Checking npm dependencies...${NC}"

cd frontend

if [ ! -d "node_modules" ]; then
    echo "Installing npm dependencies..."
    npm install
    echo -e "${GREEN}npm dependencies installed${NC}"
else
    echo -e "${GREEN}npm dependencies already installed${NC}"
fi

cd ..

# Step 5 & 6: Start backend and frontend
echo ""
echo -e "${YELLOW}Step 5: Starting servers...${NC}"
echo ""

# Start backend in background
echo -e "${CYAN}Starting Backend (http://127.0.0.1:8000)...${NC}"
gnome-terminal -- bash -c "source .venv/bin/activate && python -m backend.run; exec bash" 2>/dev/null || \
xterm -e "source .venv/bin/activate && python -m backend.run; exec bash" 2>/dev/null || \
(osascript -e 'tell app "Terminal" to do script "cd \"'$PWD'\" && source .venv/bin/activate && python -m backend.run"' 2>/dev/null || \
(osascript -e 'tell app "iTerm" to do script "cd \"'$PWD'\" && source .venv/bin/activate && python -m backend.run"' 2>/dev/null || \
(tmux new-session -d -s chatbot-backend "source .venv/bin/activate && python -m backend.run" 2>/dev/null)))

# Wait a bit for backend to start
sleep 3

# Start frontend in background
echo -e "${CYAN}Starting Frontend (http://localhost:5173)...${NC}"
cd frontend
gnome-terminal -- bash -c "npm run dev; exec bash" 2>/dev/null || \
xterm -e "npm run dev; exec bash" 2>/dev/null || \
(osascript -e 'tell app "Terminal" to do script "cd \"'$PWD/frontend'\" && npm run dev"' 2>/dev/null || \
(osascript -e 'tell app "iTerm" to do script "cd \"'$PWD/frontend'\" && npm run dev"' 2>/dev/null || \
(tmux new-session -d -s chatbot-frontend "cd frontend && npm run dev" 2>/dev/null)))

cd ..

echo ""
echo -e "${GREEN}Backend running at: http://127.0.0.1:8000${NC}"
echo -e "${GREEN}Frontend running at: http://localhost:5173${NC}"
echo -e "${GREEN}API Documentation: http://127.0.0.1:8000/docs${NC}"
echo ""
echo -e "${MAGENTA}Both servers are running in separate terminal windows.${NC}"
echo -e "${MAGENTA}Close those windows to stop the servers.${NC}"
echo ""
echo -e "${CYAN}Script completed!${NC}"

