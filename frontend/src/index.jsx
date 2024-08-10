import React from 'react';
import App from './App';
import { HelmetProvider } from 'react-helmet-async';
import {createRoot} from "react-dom/client";

createRoot(document.getElementById('root')).render(
    <HelmetProvider>
        <React.StrictMode>
            <App />
        </React.StrictMode>
    </HelmetProvider>
);
