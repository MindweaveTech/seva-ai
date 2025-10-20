# Smart AI - Admin Dashboard

Web-based dashboard for caregivers and administrators to monitor patients and manage the system.

## Overview

The admin dashboard provides:
- Patient health monitoring and insights
- Alert and notification management
- Conversation summaries and history
- User management (for admins)
- Analytics and reporting
- System configuration

## Tech Stack

- **Framework:** React 18+ (or Next.js 14+)
- **Language:** TypeScript
- **UI Library:** Material-UI (or Ant Design)
- **State Management:** Zustand or React Query
- **Charts:** Recharts
- **Testing:** Jest, React Testing Library, Playwright
- **Build Tool:** Vite

## Project Structure

```
admin-dashboard/
├── src/
│   ├── components/         # Reusable components
│   │   ├── layout/
│   │   ├── charts/
│   │   ├── tables/
│   │   └── common/
│   ├── pages/              # Page components
│   │   ├── Dashboard/
│   │   ├── Patients/
│   │   ├── Alerts/
│   │   ├── Analytics/
│   │   ├── Users/
│   │   └── Settings/
│   ├── services/           # API clients
│   │   ├── api/
│   │   ├── auth/
│   │   └── patients/
│   ├── store/              # State management
│   │   ├── authStore.ts
│   │   ├── patientsStore.ts
│   │   └── alertsStore.ts
│   ├── hooks/              # Custom hooks
│   │   ├── useAuth.ts
│   │   ├── usePatients.ts
│   │   └── useAlerts.ts
│   ├── utils/              # Helper functions
│   │   ├── date.ts
│   │   ├── charts.ts
│   │   └── export.ts
│   ├── types/              # TypeScript types
│   │   └── index.ts
│   ├── constants/          # Constants
│   │   └── config.ts
│   ├── theme/              # Theme configuration
│   │   └── index.ts
│   └── App.tsx
├── public/                 # Static assets
├── __tests__/              # Tests
├── package.json
├── tsconfig.json
├── vite.config.ts
├── .env.example
└── README.md
```

## Getting Started

### Prerequisites

- Node.js 18+
- npm or yarn

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
   # Edit .env with backend API URL
   ```

3. **Start development server**
   ```bash
   npm run dev
   # or
   yarn dev
   ```

   Dashboard will be available at: http://localhost:3000

### Environment Variables

```env
# Backend API
VITE_API_URL=http://localhost:8000/api/v1

# Environment
VITE_ENVIRONMENT=development

# Feature Flags
VITE_ENABLE_ANALYTICS=true
```

## Development

### Running Tests

```bash
# Unit tests
npm test

# Coverage
npm run test:coverage

# E2E tests
npm run test:e2e

# Watch mode
npm run test:watch
```

### Code Quality

```bash
# Lint
npm run lint

# Fix linting
npm run lint:fix

# Type check
npm run type-check

# Format
npm run format
```

### Building

```bash
# Development build
npm run build

# Preview production build
npm run preview
```

## Features

### Dashboard Overview

Main dashboard shows:
- Active patient count
- Recent alerts
- Health trend summaries
- Engagement metrics
- Quick actions

```typescript
// pages/Dashboard/DashboardPage.tsx
export const DashboardPage = () => {
  const { patients } = usePatients();
  const { alerts } = useAlerts();

  return (
    <Grid container spacing={3}>
      <Grid item xs={12} md={3}>
        <StatCard
          title="Active Patients"
          value={patients.length}
          icon={<PeopleIcon />}
        />
      </Grid>
      <Grid item xs={12} md={3}>
        <StatCard
          title="Alerts Today"
          value={alerts.today}
          icon={<AlertIcon />}
        />
      </Grid>
      {/* More cards... */}
    </Grid>
  );
};
```

### Patient Management

View and manage patient profiles:

```typescript
// pages/Patients/PatientList.tsx
export const PatientList = () => {
  const { patients, loading } = usePatients();

  return (
    <DataTable
      columns={[
        { field: 'name', headerName: 'Patient Name' },
        { field: 'age', headerName: 'Age' },
        { field: 'lastActive', headerName: 'Last Active' },
        { field: 'healthScore', headerName: 'Health Score' },
      ]}
      rows={patients}
      loading={loading}
      onRowClick={(patient) => navigate(`/patients/${patient.id}`)}
    />
  );
};
```

### Health Monitoring

View patient health metrics and trends:

```typescript
// components/charts/HealthTrendChart.tsx
export const HealthTrendChart = ({ patientId }: Props) => {
  const { healthData } = useHealthData(patientId);

  return (
    <LineChart width={600} height={300} data={healthData}>
      <XAxis dataKey="date" />
      <YAxis />
      <Tooltip />
      <Legend />
      <Line
        type="monotone"
        dataKey="bloodPressure"
        stroke="#8884d8"
      />
      <Line
        type="monotone"
        dataKey="heartRate"
        stroke="#82ca9d"
      />
    </LineChart>
  );
};
```

### Alert Management

Manage and respond to alerts:

```typescript
// pages/Alerts/AlertsPage.tsx
export const AlertsPage = () => {
  const { alerts, acknowledgeAlert } = useAlerts();

  const handleAcknowledge = async (alertId: string) => {
    await acknowledgeAlert(alertId);
  };

  return (
    <AlertList
      alerts={alerts}
      onAcknowledge={handleAcknowledge}
    />
  );
};
```

### Analytics & Reports

Generate reports and visualizations:

```typescript
// pages/Analytics/AnalyticsPage.tsx
export const AnalyticsPage = () => {
  const [dateRange, setDateRange] = useState({
    start: startOfMonth(new Date()),
    end: new Date(),
  });

  const { analytics } = useAnalytics(dateRange);

  return (
    <>
      <DateRangePicker
        value={dateRange}
        onChange={setDateRange}
      />
      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <EngagementChart data={analytics.engagement} />
        </Grid>
        <Grid item xs={12} md={6}>
          <HealthOutcomesChart data={analytics.outcomes} />
        </Grid>
      </Grid>
      <ExportButton
        data={analytics}
        filename="analytics-report"
      />
    </>
  );
};
```

## Authentication

Using JWT tokens for authentication:

```typescript
// hooks/useAuth.ts
export const useAuth = () => {
  const navigate = useNavigate();

  const login = async (email: string, password: string) => {
    const response = await api.post('/auth/login', {
      email,
      password,
    });

    const { access_token, refresh_token } = response.data;

    localStorage.setItem('access_token', access_token);
    localStorage.setItem('refresh_token', refresh_token);

    navigate('/dashboard');
  };

  const logout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    navigate('/login');
  };

  return { login, logout };
};
```

## API Integration

API client with authentication:

```typescript
// services/api/client.ts
import axios from 'axios';

export const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
});

// Request interceptor
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Response interceptor
apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      // Refresh token logic
      const refreshToken = localStorage.getItem('refresh_token');
      if (refreshToken) {
        try {
          const response = await axios.post('/auth/refresh', {
            refresh_token: refreshToken,
          });
          const { access_token } = response.data;
          localStorage.setItem('access_token', access_token);
          error.config.headers.Authorization = `Bearer ${access_token}`;
          return axios(error.config);
        } catch {
          // Redirect to login
          window.location.href = '/login';
        }
      }
    }
    return Promise.reject(error);
  }
);
```

## Theme Customization

Material-UI theme:

```typescript
// theme/index.ts
import { createTheme } from '@mui/material/styles';

export const theme = createTheme({
  palette: {
    primary: {
      main: '#4A90E2',
    },
    secondary: {
      main: '#7ED321',
    },
    error: {
      main: '#D0021B',
    },
  },
  typography: {
    fontFamily: '"Inter", "Roboto", "Helvetica", "Arial", sans-serif',
    h1: {
      fontSize: '2.5rem',
      fontWeight: 600,
    },
    h2: {
      fontSize: '2rem',
      fontWeight: 600,
    },
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: 8,
          textTransform: 'none',
        },
      },
    },
  },
});
```

## Testing

### Unit Tests

```typescript
// __tests__/components/StatCard.test.tsx
import { render, screen } from '@testing-library/react';
import { StatCard } from '@/components/StatCard';
import PeopleIcon from '@mui/icons-material/People';

describe('StatCard', () => {
  it('renders title and value', () => {
    render(
      <StatCard
        title="Active Patients"
        value={42}
        icon={<PeopleIcon />}
      />
    );

    expect(screen.getByText('Active Patients')).toBeInTheDocument();
    expect(screen.getByText('42')).toBeInTheDocument();
  });
});
```

### E2E Tests

```typescript
// e2e/dashboard.spec.ts
import { test, expect } from '@playwright/test';

test('dashboard displays patient count', async ({ page }) => {
  await page.goto('http://localhost:3000/dashboard');

  await page.waitForSelector('[data-testid="patient-count"]');

  const patientCount = await page.textContent(
    '[data-testid="patient-count"]'
  );

  expect(parseInt(patientCount || '0')).toBeGreaterThan(0);
});
```

## Deployment

### Build for Production

```bash
npm run build
```

### Deploy to Vercel

```bash
npm install -g vercel
vercel --prod
```

### Deploy to Netlify

```bash
npm install -g netlify-cli
netlify deploy --prod
```

### Docker

```dockerfile
# Dockerfile
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

## Performance

### Optimization Tips

**Code Splitting:**
```typescript
import { lazy, Suspense } from 'react';

const DashboardPage = lazy(() => import('./pages/Dashboard'));
const PatientsPage = lazy(() => import('./pages/Patients'));

<Suspense fallback={<Loading />}>
  <Routes>
    <Route path="/dashboard" element={<DashboardPage />} />
    <Route path="/patients" element={<PatientsPage />} />
  </Routes>
</Suspense>
```

**Memoization:**
```typescript
import { useMemo } from 'react';

const PatientList = ({ patients }: Props) => {
  const sortedPatients = useMemo(
    () => patients.sort((a, b) => a.name.localeCompare(b.name)),
    [patients]
  );

  return <DataTable data={sortedPatients} />;
};
```

**Virtual Scrolling:**
For large lists, use react-window or react-virtualized.

### Performance Targets
- First Contentful Paint: <1.5s
- Time to Interactive: <3s
- Lighthouse Score: 90+

## Troubleshooting

### Common Issues

**Build errors**
```bash
rm -rf node_modules package-lock.json
npm install
```

**Vite HMR not working**
- Check if port 3000 is available
- Clear browser cache
- Restart dev server

**API connection errors**
- Verify VITE_API_URL in .env
- Check CORS configuration on backend
- Verify network connectivity

## Contributing

See main repository [CONTRIBUTING.md](../CONTRIBUTING.md)

## License

MIT License - see LICENSE file for details
