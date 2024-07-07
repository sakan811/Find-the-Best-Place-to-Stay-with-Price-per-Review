import React from 'react';
import ReactDOM from 'react-dom';
import ScrapingForm from './ScrapingForm';
import HotelTable from "./HotelTable";

document.getElementById('root') && ReactDOM.render(<ScrapingForm />, document.getElementById('root'));
document.getElementById('hotelTable') && ReactDOM.render(<HotelTable />, document.getElementById('hotelTable'));
