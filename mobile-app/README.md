# Smart AI - Mobile App

React Native mobile application for elderly users to interact with their AI companion.

## Overview

The mobile app provides:
- Voice-first conversational interface
- Offline-first architecture with sync
- Simple, accessible UI for elderly users
- Health tracking and daily check-ins
- Emergency contact access

## Tech Stack

- **Framework:** React Native with Expo
- **Language:** TypeScript
- **State Management:** Zustand
- **Local Database:** WatermelonDB
- **Navigation:** React Navigation
- **Voice:** react-native-voice, Expo AV
- **Testing:** Jest, React Native Testing Library, Detox

## Project Structure

```
mobile-app/
├── src/
│   ├── components/         # Reusable UI components
│   │   ├── chat/
│   │   ├── voice/
│   │   ├── common/
│   │   └── health/
│   ├── screens/            # App screens
│   │   ├── Auth/
│   │   ├── Chat/
│   │   ├── Profile/
│   │   ├── Health/
│   │   └── Settings/
│   ├── navigation/         # Navigation configuration
│   │   └── AppNavigator.tsx
│   ├── services/           # API clients and services
│   │   ├── api/
│   │   ├── auth/
│   │   ├── chat/
│   │   ├── voice/
│   │   └── sync/
│   ├── store/              # State management
│   │   ├── authStore.ts
│   │   ├── chatStore.ts
│   │   └── syncStore.ts
│   ├── database/           # Local database
│   │   ├── models/
│   │   └── schema.ts
│   ├── utils/              # Helper functions
│   │   ├── audio.ts
│   │   ├── date.ts
│   │   └── validation.ts
│   ├── types/              # TypeScript types
│   │   └── index.ts
│   ├── constants/          # App constants
│   │   ├── colors.ts
│   │   └── config.ts
│   └── App.tsx             # Root component
├── assets/                 # Images, fonts, etc.
├── __tests__/              # Tests
│   ├── components/
│   ├── screens/
│   └── integration/
├── app.json                # Expo configuration
├── package.json
├── tsconfig.json
├── .env.example
└── README.md
```

## Getting Started

### Prerequisites

- Node.js 18+
- npm or yarn
- Expo CLI
- iOS Simulator (Mac) or Android Emulator

### Installation

1. **Install dependencies**
   ```bash
   npm install
   # or
   yarn install
   ```

2. **Setup environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with backend URL
   ```

3. **Start development server**
   ```bash
   npm start
   # or
   expo start
   ```

4. **Run on device/simulator**
   ```bash
   # iOS
   npm run ios

   # Android
   npm run android
   ```

### Environment Variables

Required variables in `.env`:

```env
# Backend API
API_URL=http://localhost:8000/api/v1

# Environment
ENVIRONMENT=development

# Feature Flags
ENABLE_VOICE=true
ENABLE_OFFLINE=true
```

## Development

### Running Tests

```bash
# Run all tests
npm test

# Run with coverage
npm run test:coverage

# Run E2E tests
npm run test:e2e

# Watch mode
npm run test:watch
```

### Code Quality

```bash
# Lint
npm run lint

# Fix linting issues
npm run lint:fix

# Type check
npm run type-check

# Format code
npm run format
```

### Building

```bash
# Development build
expo build:ios
expo build:android

# Production build
eas build --platform ios
eas build --platform android
```

## Features

### Voice Interface

The app provides voice-first interaction:

```typescript
import { VoiceButton } from '@/components/voice/VoiceButton';

<VoiceButton
  onTranscript={(text) => sendMessage(text)}
  onError={(error) => handleError(error)}
/>
```

**Features:**
- Tap-to-talk interface
- Real-time transcription
- Visual feedback (waveform)
- Error handling and retry

### Offline Support

Messages are queued locally and synced when online:

```typescript
import { useSyncStore } from '@/store/syncStore';

const { queueMessage, syncPendingMessages } = useSyncStore();

// Send message (works offline)
await queueMessage({
  text: 'Hello',
  timestamp: Date.now(),
});

// Auto-sync when back online
useEffect(() => {
  if (isOnline) {
    syncPendingMessages();
  }
}, [isOnline]);
```

### State Management

Using Zustand for simple, performant state:

```typescript
// store/chatStore.ts
import create from 'zustand';

interface ChatStore {
  messages: Message[];
  addMessage: (message: Message) => void;
  isTyping: boolean;
  setIsTyping: (typing: boolean) => void;
}

export const useChatStore = create<ChatStore>((set) => ({
  messages: [],
  addMessage: (message) =>
    set((state) => ({ messages: [...state.messages, message] })),
  isTyping: false,
  setIsTyping: (typing) => set({ isTyping: typing }),
}));
```

### Local Database

WatermelonDB for offline storage:

```typescript
// database/models/Message.ts
import { Model } from '@nozbe/watermelondb';
import { field, date, readonly } from '@nozbe/watermelondb/decorators';

export class Message extends Model {
  static table = 'messages';

  @field('text') text!: string;
  @field('sender') sender!: 'user' | 'ai';
  @readonly @date('created_at') createdAt!: Date;
  @field('synced') synced!: boolean;
}
```

## UI/UX Guidelines

### Accessibility

**Large UI Elements:**
- Minimum button size: 60x60 points
- Font size: Minimum 18px
- High contrast colors
- Clear spacing between elements

**Voice Support:**
- Prominent voice button
- Clear audio feedback
- Voice guidance for all actions

**Screen Reader:**
- All images have alt text
- Proper heading hierarchy
- Descriptive labels

### Design System

**Colors:**
```typescript
export const colors = {
  primary: '#4A90E2',
  secondary: '#7ED321',
  background: '#FFFFFF',
  text: '#333333',
  textLight: '#666666',
  error: '#D0021B',
  success: '#7ED321',
  warning: '#F5A623',
};
```

**Typography:**
```typescript
export const typography = {
  h1: { fontSize: 32, fontWeight: 'bold' },
  h2: { fontSize: 24, fontWeight: 'bold' },
  body: { fontSize: 18, fontWeight: 'normal' },
  caption: { fontSize: 14, fontWeight: 'normal' },
};
```

## Testing

### Unit Tests

```typescript
// __tests__/components/VoiceButton.test.tsx
import { render, fireEvent } from '@testing-library/react-native';
import { VoiceButton } from '@/components/voice/VoiceButton';

describe('VoiceButton', () => {
  it('calls onTranscript when recording completes', async () => {
    const onTranscript = jest.fn();
    const { getByTestId } = render(
      <VoiceButton onTranscript={onTranscript} />
    );

    const button = getByTestId('voice-button');
    fireEvent.press(button);

    // Simulate recording completion
    await waitFor(() => {
      expect(onTranscript).toHaveBeenCalledWith('test transcript');
    });
  });
});
```

### E2E Tests (Detox)

```typescript
// e2e/chat.test.ts
describe('Chat Flow', () => {
  beforeAll(async () => {
    await device.launchApp();
  });

  it('should send and receive message', async () => {
    await element(by.id('message-input')).typeText('Hello');
    await element(by.id('send-button')).tap();

    await waitFor(element(by.text('Hello')))
      .toBeVisible()
      .withTimeout(2000);
  });
});
```

## Performance

### Optimization Tips

**FlatList Optimization:**
```typescript
<FlatList
  data={messages}
  renderItem={renderMessage}
  keyExtractor={(item) => item.id}
  removeClippedSubviews={true}
  maxToRenderPerBatch={10}
  windowSize={5}
  getItemLayout={(data, index) => ({
    length: ITEM_HEIGHT,
    offset: ITEM_HEIGHT * index,
    index,
  })}
/>
```

**Image Optimization:**
- Use WebP format
- Resize images appropriately
- Lazy load off-screen images
- Cache images locally

**State Updates:**
- Minimize re-renders with React.memo
- Use useCallback for functions
- Batch state updates
- Avoid inline object creation

### Performance Targets
- App startup time: <2s
- Screen transition: <300ms
- Scroll FPS: 60fps
- Voice latency: <3s (tap to response)

## Deployment

### App Store (iOS)

1. **Build production app**
   ```bash
   eas build --platform ios --profile production
   ```

2. **Submit to App Store**
   ```bash
   eas submit --platform ios
   ```

### Google Play (Android)

1. **Build production app**
   ```bash
   eas build --platform android --profile production
   ```

2. **Submit to Play Store**
   ```bash
   eas submit --platform android
   ```

### OTA Updates

For non-native changes:
```bash
eas update --branch production
```

## Troubleshooting

### Common Issues

**Metro bundler errors**
```bash
npm start -- --reset-cache
```

**iOS pod errors**
```bash
cd ios && pod install && cd ..
```

**Android build errors**
```bash
cd android && ./gradlew clean && cd ..
```

**Voice permission denied**
- Check Info.plist (iOS) for microphone permission
- Check AndroidManifest.xml for RECORD_AUDIO permission

## Contributing

See main repository [CONTRIBUTING.md](../CONTRIBUTING.md)

## License

MIT License - see LICENSE file for details
