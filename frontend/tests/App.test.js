import React from 'react';
import { render, screen } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import App from "../src/App";
import '@testing-library/jest-dom';


// Mock the child components
jest.mock('../src/components/ScrapingForm', () => () => <div>Mocked ScrapingForm</div>);
jest.mock('../src/components/HotelTable', () => () => <div>Mocked HotelTable</div>);

// Mock react-router-dom
jest.mock('react-router-dom', () => ({
  ...jest.requireActual('react-router-dom'),
  BrowserRouter: ({ children }) => <div>{children}</div>,
}));

describe('App Component', () => {
  test('renders ScrapingForm on the root path', () => {
    render(
      <MemoryRouter initialEntries={['/']}>
        <App />
      </MemoryRouter>
    );
    expect(screen.getByText('Mocked ScrapingForm')).toBeInTheDocument();
  });

  test('renders HotelTable on the /hotel_data_table_page path', () => {
    render(
      <MemoryRouter initialEntries={['/hotel_data_table_page']}>
        <App />
      </MemoryRouter>
    );
    expect(screen.getByText('Mocked HotelTable')).toBeInTheDocument();
  });
});