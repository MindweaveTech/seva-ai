#!/bin/bash
# Stop Expo Metro bundler

echo "🛑 Stopping Expo Metro Bundler..."

# Kill expo processes
pkill -f "expo start" && echo "✅ Expo process killed" || echo "⚠️  No Expo process found"
pkill -f "metro" && echo "✅ Metro process killed" || echo "⚠️  No Metro process found"

echo "✅ Done!"
