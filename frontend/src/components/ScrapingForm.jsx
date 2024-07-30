import React, { useState } from 'react';
import './ScrapingForm.css';
import axios from "axios";
import { Helmet } from 'react-helmet-async';

const ScrapingForm = () => {
    const [formData, setFormData] = useState({
    city: '',
    check_in: '',
    check_out: '',
    group_adults: 1,
    num_rooms: 1,
    group_children: 0,
    selected_currency: '',
    hotel_filter: false,
    });

    const [submitMessage, setSubmitMessage] = useState('');
    const [errorMessage, setErrorMessage] = useState('');
    const [scrapingMessage, setScrapingMessage] = useState('');

    const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
        setFormData({
          ...formData,
          [name]: type === 'checkbox' ? checked : value,
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setScrapingMessage('Scraping data...');
        setErrorMessage(''); // Clear any previous error messages

        try {
            await axios.post('http://localhost:8000/scraping/', formData);
            setSubmitMessage('Form submitted successfully');
            window.location.href = '/hotel_data_table_page/';
        } catch (error) {
            if (error.response) {
                console.error('Error response:', error.response.data);
                console.error('Status code:', error.response.status);

                if (error.response.data.error === 'SystemExit') {
                    setErrorMessage('No places found that can satisfy this booking. Please re-enter the form.');
                } else if (error.response.status === 500) {
                    setErrorMessage('Internal server error. Please try again later.');
                } else {
                    setErrorMessage('An error occurred while submitting the form.');
                }
            } else if (error.request) {
                console.error('No response received:', error.request);
                setErrorMessage('No response received from the server. Please check your internet connection.');
            } else {
                console.error('Error setting up the request:', error.message);
                setErrorMessage('An unexpected error occurred. Please try again later.');
            }
        } finally {
            setScrapingMessage('');
        }
    };

    return (
        <>
            <Helmet>
                <title>Find the Best Place to Stay with Price/Review - Form</title>
            </Helmet>
            <h1 style={{textAlign: 'center'}}>Finding the Best Place to Stay with Price/Review from Booking.com</h1>
            <p style={{textAlign: 'center', fontSize: '16px'}}>
                Enter the hotel booking details below to scrape the hotel data
            </p>
            <form onSubmit={handleSubmit} className="form">
              <div className="formGroup">
                  <label htmlFor="city">City:</label>
                  <input type="text" id="city" name="city" value={formData.city} onChange={handleChange} maxLength={100}
                         className="input" required/>
              </div>
              <div className="formGroup">
                  <label htmlFor="check_in">Check-in:</label>
                  <input type="date" id="check_in" name="check_in" value={formData.check_in} onChange={handleChange}
                         className="input" required/>
              </div>
              <div className="formGroup">
                  <label htmlFor="check_out">Check-out:</label>
                  <input type="date" id="check_out" name="check_out" value={formData.check_out} onChange={handleChange}
                         className="input" required/>
              </div>
              <div className="formGroup">
                  <label htmlFor="group_adults">Adults:</label>
                  <input type="number" id="group_adults" name="group_adults" value={formData.group_adults}
                         onChange={handleChange} min={1} className="input"/>
              </div>
              <div className="formGroup">
                  <label htmlFor="num_rooms">Rooms:</label>
                  <input type="number" id="num_rooms" name="num_rooms" value={formData.num_rooms}
                         onChange={handleChange} min={1} className="input"/>
              </div>
              <div className="formGroup">
                  <label htmlFor="group_children">Children:</label>
                  <input type="number" id="group_children" name="group_children" value={formData.group_children}
                         onChange={handleChange} min={0} className="input"/>
              </div>
              <div className="formGroup">
                  <label htmlFor="selected_currency">Currency:</label>
                  <input type="text" id="selected_currency" name="selected_currency" value={formData.selected_currency}
                         onChange={handleChange} maxLength={10} className="input" required/>
              </div>
              <div className="formGroup">
                  <label htmlFor="hotel_filter">Scrape Hotel Properties Only:</label>
                  <input type="checkbox" id="hotel_filter" name="hotel_filter" checked={formData.hotel_filter}
                         onChange={handleChange} className="checkbox"/>
              </div>
              <button type="submit" className="submitButton">Submit</button>
                {scrapingMessage && <p className="message">{scrapingMessage}</p>}
                {submitMessage && <p className="message">{submitMessage}</p>}
                {errorMessage && <p className="errorMessage">{errorMessage}</p>}
            </form>
        </>
    );
};

export default ScrapingForm;
