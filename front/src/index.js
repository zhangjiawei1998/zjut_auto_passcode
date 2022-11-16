import React from 'react';
import ReactDOM from 'react-dom/client';
import { HashRouter,BrowserRouter, Routes, Route, } from 'react-router-dom';
import './index.css';
// routes
import Passcode from './routes/passcode';
import JoinAutoClock from './routes/joinAutoClock';
const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <HashRouter>
    <Routes>
      <Route path='/' element={<JoinAutoClock />} />
      <Route path='/passcode' element={<Passcode />} />
    </Routes>
  </HashRouter>
);


