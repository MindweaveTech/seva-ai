# Smart AI - Mobile App Setup Guide

## Prerequisites

- Node.js 18+ installed
- npm or yarn
- Expo CLI (`npm install -g expo-cli`)
- iOS Simulator (Mac only) or Android Emulator
- Backend API running on `http://localhost:8000`

## Installation

```bash
# Navigate to mobile app directory
cd mobile-app

# Install dependencies
npm install

# Start the Expo development server
npm start
```

## Running the App

### iOS Simulator (Mac only)

```bash
npm run ios
```

Or press `i` in the Expo CLI menu after running `npm start`.

### Android Emulator

```bash
npm run android
```

Or press `a` in the Expo CLI menu after running `npm start`.

### Web Browser (for testing)

```bash
npm run web
```

Or press `w` in the Expo CLI menu.

## Environment Configuration

Create a `.env` file in the `mobile-app/` directory:

```env
# API Configuration
API_URL=http://localhost:8000/api/v1

# For testing on physical device, use your machine's IP
# API_URL=http://192.168.1.XXX:8000/api/v1
```

**Note:** Update `src/services/api/client.ts` if you change the API URL.

## Project Structure

```
mobile-app/
├── src/
│   ├── navigation/
│   │   └── AppNavigator.tsx       # Main navigation setup
│   ├── screens/
│   │   ├── LoginScreen.tsx        # Login UI
│   │   ├── RegisterScreen.tsx     # Registration UI
│   │   ├── ChatScreen.tsx         # Chat interface
│   │   └── SessionsScreen.tsx     # Conversation history
│   ├── services/
│   │   └── api/
│   │       ├── client.ts          # Axios instance with interceptors
│   │       ├── auth.ts            # Auth API calls
│   │       └── chat.ts            # Chat API calls
│   └── store/
│       ├── authStore.ts           # Auth state (Zustand)
│       └── chatStore.ts           # Chat state (Zustand)
├── App.tsx                        # App entry point
├── package.json
└── tsconfig.json
```

## Features Implemented

### Authentication
- [x] User registration with validation
- [x] Login with email/password
- [x] JWT token management (access + refresh)
- [x] Auto token refresh on 401 errors
- [x] Persistent login (AsyncStorage)
- [x] Logout functionality

### Chat
- [x] Send messages to AI companion
- [x] View conversation history
- [x] Create new sessions
- [x] View previous sessions
- [x] Delete sessions
- [x] Real-time message updates

### UI/UX
- [x] Form validation with error messages
- [x] Loading states and spinners
- [x] Keyboard handling
- [x] Message bubbles (user vs AI)
- [x] Responsive layout
- [x] Pull to refresh (sessions)

## Navigation Flow

```
App Launch
   │
   ├─ Not Authenticated → Auth Stack
   │                         ├── Login Screen
   │                         └── Register Screen
   │
   └─ Authenticated → Main Stack
                         ├── Sessions Screen (default)
                         └── Chat Screen
```

## State Management

Uses **Zustand** for simple, performant state management:

- **authStore**: User authentication state, login/register/logout actions
- **chatStore**: Chat messages, sessions, send message actions

## API Integration

All API calls go through `src/services/api/client.ts` which:

- Automatically adds `Authorization: Bearer <token>` header
- Intercepts 401 responses and refreshes tokens
- Queues failed requests and retries after refresh
- Handles network errors gracefully

## Testing on Physical Device

To test on a real phone:

1. Ensure your phone and computer are on the same WiFi network
2. Find your computer's local IP address:
   ```bash
   # On Mac/Linux
   ifconfig | grep "inet "

   # On Windows
   ipconfig
   ```
3. Update `src/services/api/client.ts`:
   ```typescript
   const API_URL = 'http://192.168.1.XXX:8000/api/v1';
   ```
4. Scan the QR code from Expo CLI with Expo Go app

## Common Issues

### "Network request failed"

- Make sure backend is running on `http://localhost:8000`
- If testing on physical device, use your computer's IP instead of localhost
- Check that API_URL is correct

### "Unable to resolve module"

```bash
# Clear cache and reinstall
rm -rf node_modules
npm install
npx expo start -c
```

### iOS build fails

```bash
# Reset iOS simulator
npx expo start -c --ios
```

### TypeScript errors

```bash
# Run type check
npm run type-check
```

## Available Scripts

```bash
# Development
npm start              # Start Expo dev server
npm run ios            # Run on iOS simulator
npm run android        # Run on Android emulator
npm run web            # Run in web browser

# Code Quality
npm run lint           # Run ESLint
npm run lint:fix       # Auto-fix ESLint issues
npm run type-check     # Run TypeScript compiler
npm run format         # Format code with Prettier

# Testing
npm test               # Run Jest tests
npm run test:watch     # Run tests in watch mode
npm run test:coverage  # Run tests with coverage report
```

## Next Steps

1. **Run the app**: `npm start` and press `i` for iOS or `a` for Android
2. **Test registration**: Create a new account
3. **Test login**: Sign in with your account
4. **Test chat**: Send a message to the AI companion
5. **Test sessions**: View conversation history

## Development Workflow

1. Make sure backend is running:
   ```bash
   cd ../backend
   docker-compose -f ../infrastructure/docker/docker-compose.dev.yml up -d
   uvicorn app.main:app --reload
   ```

2. Start mobile app:
   ```bash
   cd mobile-app
   npm start
   ```

3. Make changes to code - changes hot reload automatically

## Troubleshooting

**App crashes on startup:**
- Check that all dependencies are installed: `npm install`
- Clear Expo cache: `npx expo start -c`

**Can't connect to backend:**
- Verify backend is running: `curl http://localhost:8000/api/v1/health`
- Check network configuration (localhost vs IP address)
- Ensure no firewall blocking port 8000

**TypeScript errors:**
- Run `npm run type-check` to see all errors
- Most common: missing type definitions or incorrect prop types

## Production Build

Not yet configured. Will be added in Phase 2 with:
- Expo EAS Build for iOS/Android
- Environment-specific configurations
- App store deployment

---

**Status:** Phase 1 Complete - Mobile UI implemented
**Last Updated:** 2025-10-21
