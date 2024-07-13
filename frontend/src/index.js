import React from 'react';
import ReactDOM from 'react-dom';
import App from './App';
import { HelmetProvider } from 'react-helmet-async';

ReactDOM.render(
    <HelmetProvider>
        <React.StrictMode>
            <App />
        </React.StrictMode>
    </HelmetProvider>,
    document.getElementById('root')
);
