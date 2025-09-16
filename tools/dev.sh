#!/usr/bin/env bash
set -e


# Check for 'entr'
if ! command -v entr &> /dev/null; then
    echo "⚠️  'entr' is not installed."
    echo "On Debian/Ubuntu: sudo apt install entr"
    echo "On MacOS: brew install entr"
    read -p "Do you want to continue anyway? [y/N]: " answer
    if [[ ! "$answer" =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi


IMAGE="power_py"
CONTAINER="power_py"

rebuild() {
    echo "Rebuilding image..."
    docker build -t "$IMAGE" .

    if [ "$(docker ps -aq -f name=$CONTAINER)" ]; then
        echo "Stopping old container..."
        docker stop "$CONTAINER" >/dev/null 2>&1 || true
        docker rm "$CONTAINER" >/dev/null 2>&1 || true
    fi

    echo "Starting new container..."
    docker run --name "$CONTAINER" \
        -v "$(pwd):/app" \
        -w /app/src \
        "$IMAGE"
}

watch() {
    echo "Watching for changes..."
    find . -type f \( -name "*.py" -o -iname "dockerfile" \) | entr -r ./tools/dev.sh run
}

case "$1" in
    run) rebuild ;;
    watch) watch ;;
    *) echo "Usage: $0 {run|watch}" ;;
esac
