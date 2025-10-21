#!/bin/bash
# Start Expo Metro bundler in background for iPhone testing

set -e

echo "🚀 Starting Expo Metro Bundler for iPhone..."

# Navigate to mobile app directory
cd "$(dirname "$0")/mobile-app"

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install --legacy-peer-deps
fi

# Kill any existing expo processes
pkill -f "expo start" || true
pkill -f "metro" || true

# Start Expo in background with tunnel mode on custom port
echo "📱 Starting Expo with --tunnel mode (accessible from anywhere)..."
nohup npx expo start --tunnel --clear --port 19000 > ../expo.log 2>&1 &

EXPO_PID=$!
echo "✅ Expo started with PID: $EXPO_PID"

# Wait a few seconds for startup
sleep 5

echo ""
echo "📋 Expo Metro Bundler is running!"
echo "   Log file: $(pwd)/../expo.log"
echo "   PID: $EXPO_PID"
echo ""
echo "To view logs:"
echo "   tail -f expo.log"
echo ""
echo "To stop Expo:"
echo "   pkill -f 'expo start'"
echo "   # or"
echo "   kill $EXPO_PID"
echo ""
echo "📱 Open Expo Go app on your iPhone and scan the QR code"
echo "   (QR code is in the logs above or run: tail -f ../expo.log)"
echo ""
