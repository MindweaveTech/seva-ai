#!/bin/bash
# Test login with test user credentials

echo "Testing login with test user..."
echo "Email: test@smartai.com"
echo "Password: TestPass123!"
echo ""

# Make sure backend is running
if ! curl -s http://localhost:8000/health > /dev/null; then
    echo "❌ Backend is not running!"
    echo ""
    echo "Start the backend first:"
    echo "  cd backend"
    echo "  docker-compose -f ../infrastructure/docker/docker-compose.dev.yml up -d"
    echo "  uvicorn app.main:app --reload"
    exit 1
fi

echo "✅ Backend is running"
echo ""

# Test login
echo "Attempting login..."
response=$(curl -s -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@smartai.com",
    "password": "TestPass123!"
  }')

# Check if we got tokens
if echo "$response" | grep -q "access_token"; then
    echo "✅ Login successful!"
    echo ""
    echo "Response:"
    echo "$response" | python3 -m json.tool
    echo ""

    # Extract access token
    access_token=$(echo "$response" | python3 -c "import sys, json; print(json.load(sys.stdin)['access_token'])")

    echo "Testing authenticated request..."
    user_response=$(curl -s http://localhost:8000/api/v1/auth/me \
      -H "Authorization: Bearer $access_token")

    echo "Current user:"
    echo "$user_response" | python3 -m json.tool
    echo ""
    echo "✅ All tests passed!"
else
    echo "❌ Login failed!"
    echo ""
    echo "Response:"
    echo "$response"
    exit 1
fi
