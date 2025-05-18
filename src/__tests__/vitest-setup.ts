import { beforeEach, vi, expect } from 'vitest';
import * as matchers from '@testing-library/jest-dom/matchers';

// Extend Vitest's expect with Jest DOM matchers
expect.extend(matchers);

// Mock Next.js router
vi.mock('next/navigation', () => ({
  useRouter: vi.fn(() => ({
    push: vi.fn(),
    back: vi.fn(),
    forward: vi.fn(),
  })),
}));

// Create a mock localStorage for testing
const localStorageMock = (() => {
  let store: Record<string, string> = {};
  return {
    getItem: vi.fn((key: string) => store[key] || null),
    setItem: vi.fn((key: string, value: string) => {
      store[key] = value.toString();
    }),
    removeItem: vi.fn((key: string) => {
      delete store[key];
    }),
    clear: vi.fn(() => {
      store = {};
    }),
  };
})();

// Set up global mocks
Object.defineProperty(window, 'localStorage', {
  value: localStorageMock,
});

// Reset localStorage between tests
beforeEach(() => {
  localStorageMock.clear();
  vi.clearAllMocks();
});