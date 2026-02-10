## Based on https://www.freecodecamp.org/news/run-python-gui-in-github-codespaces/

#!/usr/bin/env bash
set -e

SCRIPT_NAME="pygame-codespaces"
VNC_PORT=5900
NOVNC_PORT=6080
DISPLAY_NUM=1
LOG_DIR="/tmp/${SCRIPT_NAME}-logs"
PID_DIR="/tmp/${SCRIPT_NAME}-pids"

# Default resolution
DEFAULT_WIDTH=480
DEFAULT_HEIGHT=270
SCREEN_WIDTH=${DEFAULT_WIDTH}
SCREEN_HEIGHT=${DEFAULT_HEIGHT}

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() { echo -e "${BLUE}ℹ️  INFO:${NC} $1"; }
log_success() { echo -e "${GREEN}✅ SUCCESS:${NC} $1"; }
log_warning() { echo -e "${YELLOW}⚠️  WARNING:${NC} $1"; }
log_error() { echo -e "${RED}❌ ERROR:${NC} $1" >&2; }

# Parse resolution parameter
parse_resolution() {
    local resolution=$1
    if [[ "$resolution" =~ ^([0-9]+)x([0-9]+)$ ]]; then
        SCREEN_WIDTH="${BASH_REMATCH[1]}"
        SCREEN_HEIGHT="${BASH_REMATCH[2]}"
        log_info "Set resolution to ${SCREEN_WIDTH}x${SCREEN_HEIGHT}"
    else
        log_error "Invalid resolution format: $resolution. Use WIDTHxHEIGHT (e.g., 1024x768)"
        return 1
    fi
}

# Create necessary directories
create_dirs() {
    mkdir -p "$LOG_DIR" "$PID_DIR"
}

# Check if a process is running
is_process_running() {
    local pid_file="$1"
    if [[ -f "$pid_file" ]]; then
        local pid=$(cat "$pid_file")
        if kill -0 "$pid" 2>/dev/null; then
            return 0
        else
            rm -f "$pid_file"
            return 1
        fi
    fi
    return 1
}

# Save PID to file
save_pid() {
    local pid_file="$1"
    local pid="$2"
    echo "$pid" > "$pid_file"
}

# Stop process by PID file
stop_process() {
    local pid_file="$1"
    local process_name="$2"
    
    if is_process_running "$pid_file"; then
        local pid=$(cat "$pid_file")
        log_info "Stopping $process_name (PID: $pid)..."
        kill "$pid" 2>/dev/null || true
        sleep 1
        if kill -0 "$pid" 2>/dev/null; then
            log_warning "$process_name didn't stop gracefully, forcing..."
            kill -9 "$pid" 2>/dev/null || true
        fi
        rm -f "$pid_file"
        log_success "Stopped $process_name"
    else
        log_info "$process_name is not running"
    fi
}

init_command() {
    log_info "Initializing Pygame Codespaces environment..."
    
    if [[ -f "/etc/debian_version" ]]; then
        log_info "Updating package lists..."
        sudo apt-get update -y
        
        log_info "Installing system dependencies..."
        sudo apt-get install -y xvfb x11vnc fluxbox websockify novnc python3-pip
        
        log_info "Installing Pygame..."
        pip3 install pygame
        
        log_success "All dependencies installed successfully"
    else
        log_warning "Unsupported OS. Please install manually: xvfb, x11vnc, fluxbox, websockify, novnc, pygame"
        return 1
    fi
}

start_command() {
    local resolution="$1"
    
    if [[ -n "$resolution" ]]; then
        parse_resolution "$resolution" || return 1
    else
        log_info "Using default resolution: ${SCREEN_WIDTH}x${SCREEN_HEIGHT}"
    fi
    
    log_info "Starting Pygame Codespaces services (${SCREEN_WIDTH}x${SCREEN_HEIGHT} @ 30 FPS)..."
    create_dirs
    
    # Check if services are already running
    if is_process_running "$PID_DIR/xvfb.pid"; then
        log_warning "Services are already running. Use '$0 stop' to stop them first."
        return 1
    fi
    
    # Start Xvfb with specified resolution
    log_info "Starting virtual display (${SCREEN_WIDTH}x${SCREEN_HEIGHT})..."
    Xvfb :$DISPLAY_NUM -screen 0 ${SCREEN_WIDTH}x${SCREEN_HEIGHT}x24 -ac +extension GLX +render -noreset \
        > "$LOG_DIR/xvfb.log" 2>&1 &
    save_pid "$PID_DIR/xvfb.pid" $!
    sleep 2
    
    export DISPLAY=:$DISPLAY_NUM
    
    # Start Fluxbox
    log_info "Starting window manager..."
    fluxbox > "$LOG_DIR/fluxbox.log" 2>&1 &
    save_pid "$PID_DIR/fluxbox.pid" $!
    sleep 1
    
    # Start VNC server with frame rate limit
    log_info "Starting VNC server on port $VNC_PORT (30 FPS)..."
    x11vnc -display :$DISPLAY_NUM -nopw -forever -shared -rfbport $VNC_PORT \
        -wait 33 -defer 33 -ping 5 -loop -bg > "$LOG_DIR/x11vnc.log" 2>&1 &
    save_pid "$PID_DIR/x11vnc.pid" $!
    sleep 2
    
    # Start noVNC
    log_info "Starting noVNC on port $NOVNC_PORT..."
    websockify --web=/usr/share/novnc $NOVNC_PORT localhost:$VNC_PORT \
        > "$LOG_DIR/websockify.log" 2>&1 &
    save_pid "$PID_DIR/websockify.pid" $!
    sleep 2
    
    # Verify services are running
    local all_ok=true
    for service in xvfb fluxbox x11vnc websockify; do
        if is_process_running "$PID_DIR/$service.pid"; then
            log_success "$service is running"
        else
            log_error "$service failed to start"
            all_ok=false
        fi
    done
    
    if $all_ok; then
        log_success "All services started successfully!"
        echo ""
        echo -e "${GREEN}🎮 Pygame environment is ready!${NC}"
        echo ""
        echo "Resolution: ${SCREEN_WIDTH}x${SCREEN_HEIGHT}"
        echo "Target FPS: 30"
        echo ""
        echo "To access your GUI environment:"
        echo "1. Go to your Codespaces Ports tab"
        echo "2. Find port $NOVNC_PORT and set it to Public"
        echo "3. Click the 'Open in Browser' link"
        echo "4. Run your Pygame application with:"
        echo "   DISPLAY=:$DISPLAY_NUM python3 your_game.py"
        echo ""
        echo "Use '$0 stop' to stop all services"
        echo "Use '$0 status' to check service status"
    else
        log_error "Some services failed to start. Check logs in $LOG_DIR/"
        return 1
    fi
}

stop_command() {
    log_info "Stopping Pygame Codespaces services..."
    
    stop_process "$PID_DIR/websockify.pid" "noVNC"
    stop_process "$PID_DIR/x11vnc.pid" "VNC Server"
    stop_process "$PID_DIR/fluxbox.pid" "Fluxbox"
    stop_process "$PID_DIR/xvfb.pid" "Xvfb"
    
    log_success "All services stopped"
}

status_command() {
    log_info "Checking service status..."
    
    local services=("xvfb" "fluxbox" "x11vnc" "websockify")
    local all_running=true
    
    for service in "${services[@]}"; do
        local pid_file="$PID_DIR/$service.pid"
        if is_process_running "$pid_file"; then
            local pid=$(cat "$pid_file")
            echo -e "${GREEN}✓${NC} $service is running (PID: $pid)"
        else
            echo -e "${RED}✗${NC} $service is not running"
            all_running=false
        fi
    done
    
    if $all_running; then
        echo ""
        echo -e "${GREEN}All services are running. Environment is ready!${NC}"
        echo "Resolution: ${SCREEN_WIDTH}x${SCREEN_HEIGHT}"
    else
        echo ""
        echo -e "${YELLOW}Some services are not running. Use '$0 start' to start them.${NC}"
    fi
}

clean_command() {
    log_info "Cleaning up log and PID files..."
    rm -rf "$LOG_DIR" "$PID_DIR"
    log_success "Cleanup completed"
}

usage() {
    cat << EOF
Usage: $0 {init|start|stop|status|clean|help} [RESOLUTION]
Manage Pygame Codespaces environment
Commands:
    init                    - Install necessary dependencies
    start [RESOLUTION]      - Start all services (Xvfb, Fluxbox, VNC, noVNC)
                              RESOLUTION: WIDTHxHEIGHT (e.g., 1024x768, default: 480x270)
    stop                    - Stop all running services
    status                  - Show status of all services
    clean                   - Remove log and PID files
    help                    - Show this help message
Examples:
    $0 init                    # First time setup
    $0 start                   # Start with default 480x270 resolution
    $0 start 1024x768          # Start with 1024x768 resolution
    $0 start 800x600           # Start with 800x600 resolution
    $0 status                  # Check if services are running
    $0 stop                    # Stop the GUI environment
Environment runs at 30 FPS for optimal performance in Codespaces.
EOF
}

main() {
    case "${1:-}" in
        init)
            init_command
            ;;
        start)
            start_command "$2"
            ;;
        stop)
            stop_command
            ;;
        status)
            status_command
            ;;
        clean)
            clean_command
            ;;
        help|--help|-h)
            usage
            ;;
        *)
            if [[ -z "$1" ]]; then
                log_error "No command specified"
            else
                log_error "Unknown command: $1"
            fi
            echo ""
            usage
            exit 1
            ;;
    esac
}

# Run main function with all arguments
main "$@"