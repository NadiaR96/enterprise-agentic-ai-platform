import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import AIChat from '../AIChat';

// Mock localStorage
const localStorageMock = {
  getItem: jest.fn(),
  setItem: jest.fn(),
  removeItem: jest.fn(),
  clear: jest.fn(),
};
Object.defineProperty(global, 'localStorage', {
  value: localStorageMock,
  configurable: true,
  writable: true,
});
Object.defineProperty(global, 'fetch', {
  value: jest.fn(),
  configurable: true,
  writable: true,
});
if (typeof window !== 'undefined') {
  Object.defineProperty(window, 'localStorage', {
    value: localStorageMock,
    configurable: true,
    writable: true,
  });
  Object.defineProperty(window, 'fetch', {
    value: global.fetch,
    configurable: true,
    writable: true,
  });
}

describe('AIChat Component', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    global.fetch.mockReset();
    if (typeof window !== 'undefined') {
      Object.defineProperty(window, 'fetch', {
        value: global.fetch,
        configurable: true,
        writable: true,
      });
      Object.defineProperty(window, 'localStorage', {
        value: localStorageMock,
        configurable: true,
        writable: true,
      });
    }
    localStorageMock.getItem.mockReturnValue(null);
  });

  describe('Authentication Flow', () => {
    test('shows login form when not authenticated', () => {
      render(<AIChat />);

      expect(screen.getByRole('heading', { name: 'Login' })).toBeInTheDocument();
      expect(screen.getByPlaceholderText('Username')).toBeInTheDocument();
      expect(screen.getByPlaceholderText('Password')).toBeInTheDocument();
    });

    test('successful login shows chat interface', async () => {
      const mockToken = 'mock-jwt-token';
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ access_token: mockToken, token_type: 'bearer' }),
      }).mockResolvedValueOnce({
        ok: true,
        json: async () => ({ user_id: 'testuser', roles: ['user'] }),
      });

      render(<AIChat />);

      await userEvent.type(screen.getByPlaceholderText('Username'), 'admin');
      await userEvent.type(screen.getByPlaceholderText('Password'), 'admin');
      fireEvent.click(screen.getByRole('button', { name: 'Login' }));

      await waitFor(() => {
        expect(screen.getByText('AI Chat - User: testuser (user)')).toBeInTheDocument();
      });

      await waitFor(() => {
        expect(localStorageMock.setItem).toHaveBeenCalledWith('token', mockToken);
      });
    });

    test('login failure shows error', async () => {
      global.fetch.mockResolvedValueOnce({
        ok: false,
        status: 401,
      });

      render(<AIChat />);

      await userEvent.type(screen.getByPlaceholderText('Username'), 'admin');
      await userEvent.type(screen.getByPlaceholderText('Password'), 'wrongpassword');
      fireEvent.click(screen.getByRole('button', { name: 'Login' }));

      await waitFor(() => {
        expect(screen.getByText('Login failed')).toBeInTheDocument();
      });
    });

    test('logout clears authentication', async () => {
      // Mock authenticated state
      localStorageMock.getItem.mockReturnValue('mock-token');
      global.fetch
        .mockResolvedValueOnce({
          ok: true,
          json: async () => ({ user_id: 'testuser', roles: ['user'] }),
        })
        .mockResolvedValueOnce({
          ok: true,
          json: async () => ({ history: [] }),
        });

      render(<AIChat />);

      await waitFor(() => {
        expect(screen.getByRole('button', { name: 'Logout' })).toBeInTheDocument();
      });

      fireEvent.click(screen.getByRole('button', { name: 'Logout' }));

      expect(localStorageMock.removeItem).toHaveBeenCalledWith('token');
      expect(screen.getByRole('heading', { name: 'Login' })).toBeInTheDocument();
    });
  });

  describe('Chat Functionality', () => {
    beforeEach(() => {
      // Mock authenticated state
      localStorageMock.getItem.mockReturnValue('mock-token');
      global.fetch.mockResolvedValue({
        ok: true,
        json: async () => ({ user_id: 'testuser', roles: ['user'] }),
      });
    });

    test('sends query and displays response', async () => {
      global.fetch
        .mockResolvedValueOnce({
          ok: true,
          json: async () => ({ user_id: 'testuser', roles: ['user'] }),
        })
        .mockResolvedValueOnce({
          ok: true,
          json: async () => ({ history: [] }),
        })
        .mockResolvedValueOnce({
          ok: true,
          json: async () => ({
            response: { answer: 'Test answer', confidence: 0.9 },
            user_id: 'testuser'
          }),
        });

      render(<AIChat />);

      await waitFor(() => {
        expect(screen.getByPlaceholderText('Type your query...')).toBeInTheDocument();
      });

      const input = screen.getByPlaceholderText('Type your query...');
      const sendButton = screen.getByText('Send');

      await userEvent.type(input, 'What is AI?');
      fireEvent.click(sendButton);

      await waitFor(() => {
        expect(screen.getByText(/What is AI\?/i)).toBeInTheDocument();
        expect(screen.getByText(/Test answer/i)).toBeInTheDocument();
        expect(screen.getByText(/Confidence:\s*90%/i)).toBeInTheDocument();
      });
    });

    test('handles API errors gracefully', async () => {
      global.fetch
        .mockResolvedValueOnce({
          ok: true,
          json: async () => ({ user_id: 'testuser', roles: ['user'] }),
        })
        .mockResolvedValueOnce({
          ok: true,
          json: async () => ({ history: [] }),
        })
        .mockResolvedValueOnce({
          ok: false,
          status: 500,
        });

      render(<AIChat />);

      await waitFor(() => {
        expect(screen.getByPlaceholderText('Type your query...')).toBeInTheDocument();
      });

      const input = screen.getByPlaceholderText('Type your query...');
      const sendButton = screen.getByText('Send');

      await userEvent.type(input, 'Test query');
      fireEvent.click(sendButton);

      await waitFor(() => {
        expect(screen.getByText('Failed to send query. Check backend.')).toBeInTheDocument();
      });
    });

    test('shows loading state during query', async () => {
      global.fetch
        .mockResolvedValueOnce({
          ok: true,
          json: async () => ({ user_id: 'testuser', roles: ['user'] }),
        })
        .mockResolvedValueOnce({
          ok: true,
          json: async () => ({ history: [] }),
        })
        .mockResolvedValueOnce(new Promise(resolve =>
          setTimeout(() => resolve({
            ok: true,
            json: async () => ({
              response: { answer: 'Delayed answer', confidence: 0.8 },
              user_id: 'testuser'
            }),
          }), 100)
        ));

      render(<AIChat />);

      await waitFor(() => {
        expect(screen.getByPlaceholderText('Type your query...')).toBeInTheDocument();
      });

      const input = screen.getByPlaceholderText('Type your query...');
      const sendButton = screen.getByText('Send');

      await userEvent.type(input, 'Test query');
      fireEvent.click(sendButton);

      expect(screen.getByText('Sending...')).toBeInTheDocument();

      await waitFor(() => {
        expect(screen.getByText(/Delayed answer/i)).toBeInTheDocument();
      });
    });
  });

  describe('User Interface', () => {
    beforeEach(() => {
      // Mock authenticated state
      localStorageMock.getItem.mockReturnValue('mock-token');
      global.fetch.mockResolvedValue({
        ok: true,
        json: async () => ({ user_id: 'testuser', roles: ['user'] }),
      });
    });

    test('displays user information in header', async () => {
      render(<AIChat />);

      await waitFor(() => {
        expect(screen.getByText('AI Chat - User: testuser (user)')).toBeInTheDocument();
      });
    });

    test('input field is cleared after sending query', async () => {
      global.fetch
        .mockResolvedValueOnce({
          ok: true,
          json: async () => ({ user_id: 'testuser', roles: ['user'] }),
        })
        .mockResolvedValueOnce({
          ok: true,
          json: async () => ({ history: [] }),
        })
        .mockResolvedValueOnce({
          ok: true,
          json: async () => ({
            response: { answer: 'Test answer', confidence: 0.9 },
            user_id: 'testuser'
          }),
        });

      render(<AIChat />);

      await waitFor(() => {
        expect(screen.getByPlaceholderText('Type your query...')).toBeInTheDocument();
      });

      const input = screen.getByPlaceholderText('Type your query...');
      await userEvent.type(input, 'Test query');
      fireEvent.click(screen.getByText('Send'));

      await waitFor(() => {
        expect(input.value).toBe('');
      });
    });
  });
});