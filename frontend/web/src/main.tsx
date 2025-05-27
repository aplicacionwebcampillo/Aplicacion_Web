import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './index.css';
import { CarritoProvider } from "./context/CarritoContext";
import { useAuth } from "./context/useAuth";

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
   <useAuth>
    <CarritoProvider>
      <App />
    </CarritoProvider>
    </useAuth>
  </React.StrictMode>,
);

