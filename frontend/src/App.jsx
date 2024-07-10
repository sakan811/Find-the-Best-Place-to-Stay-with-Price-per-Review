import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import ScrapingForm from './components/ScrapingForm';
import HotelTable from './components/HotelTable';

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<ScrapingForm />} />
        <Route path="/hotel_data_table_page" element={<HotelTable />} />
      </Routes>
    </Router>
  );
};

export default App;
