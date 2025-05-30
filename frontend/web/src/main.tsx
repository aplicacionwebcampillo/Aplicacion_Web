import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './index.css';
import { CarritoProvider } from "./context/CarritoContext";
import { HashRouter } from "react-router-dom";

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
   <HashRouter>
    <CarritoProvider>
      <App />
    </CarritoProvider>
   </HashRouter>
  </React.StrictMode>,
);

