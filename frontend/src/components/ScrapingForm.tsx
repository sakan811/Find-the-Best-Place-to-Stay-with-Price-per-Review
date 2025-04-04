import React, { useState, ChangeEvent, FormEvent } from 'react';
import './ScrapingForm.css';
import axios, {AxiosError, AxiosResponse} from 'axios';

interface SystemExit extends AxiosError {
  response: AxiosResponse & {
    data: {
      error: string;
    };
  };
}

// Define the shape of form data
interface FormData {
  city: string;
  country: string;
  check_in: string;
  check_out: string;
  group_adults: number;
  num_rooms: number;
  group_children: number;
  selected_currency: string;
  hotel_filter: boolean;
}

const ScrapingForm: React.FC = () => {
  const [formData, setFormData] = useState<FormData>({
    city: '',
    country: '',
    check_in: '',
    check_out: '',
    group_adults: 1,
    num_rooms: 1,
    group_children: 0,
    selected_currency: '',
    hotel_filter: false,
  });

  const [submitMessage, setSubmitMessage] = useState<string>('');
  const [errorMessage, setErrorMessage] = useState<string>('');
  const [scrapingMessage, setScrapingMessage] = useState<string>('');

  const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
    const { name, value, type, checked } = e.target;
    setFormData({
      ...formData,
      [name]: type === 'checkbox' ? checked : value,
    });
  };

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setScrapingMessage('Scraping data...');
    setErrorMessage(''); // Clear any previous error messages

    try {
      await axios.post('http://localhost:8000/scraping/', formData);
      setSubmitMessage('Form submitted successfully');
      window.location.href = '/hotel_data_table_page/';
    } catch (error: unknown) {
      console.error('Error:', error);
      const axiosError = error as AxiosError;
      if (axiosError.isAxiosError) {
        const systemError = axiosError as SystemExit;
        if (systemError.response?.data?.error === 'SystemExit') {
        setErrorMessage('No places found that can satisfy this booking. Please re-enter the form.');
        } else if (axiosError.response?.status === 500) {
        setErrorMessage('Internal server error. Please try again later.');
        } else {
        setErrorMessage('An error occurred while submitting the form.');
        }
      }
    } finally {
      setScrapingMessage('');
    }
  };

  return (
    <>
      <title>Find the Best Place to Stay with Price/Review - Form</title>
      <h1 style={{ textAlign: 'center' }}>Finding the Best Place to Stay with Price/Review from Booking.com</h1>
      <p style={{ textAlign: 'center', fontSize: '16px' }}>
        Enter the hotel booking details below to scrape the hotel data
      </p>
      <form onSubmit={handleSubmit} className="form">
        <div className="formGroup">
          <label htmlFor="city">City:</label>
          <input
              type="text"
              id="city"
              name="city"
              value={formData.city}
              onChange={handleChange}
              maxLength={100}
              className="input"
              required
          />
        </div>
        <div className="formGroup">
          <label htmlFor="country">Country:</label>
          <input
              type="text"
              id="country"
              name="country"
              value={formData.country}
              onChange={handleChange}
              maxLength={100}
              className="input"
              required
          />
        </div>
        <div className="formGroup">
          <label htmlFor="check_in">Check-in:</label>
          <input
              type="date"
              id="check_in"
              name="check_in"
              value={formData.check_in}
              onChange={handleChange}
              className="input"
              required
          />
        </div>
        <div className="formGroup">
          <label htmlFor="check_out">Check-out:</label>
          <input
              type="date"
              id="check_out"
              name="check_out"
              value={formData.check_out}
              onChange={handleChange}
              className="input"
              required
          />
        </div>
        <div className="formGroup">
          <label htmlFor="group_adults">Adults:</label>
          <input
              type="number"
              id="group_adults"
              name="group_adults"
              value={formData.group_adults}
              onChange={handleChange}
              min={1}
              className="input"
          />
        </div>
        <div className="formGroup">
          <label htmlFor="num_rooms">Rooms:</label>
          <input
              type="number"
              id="num_rooms"
              name="num_rooms"
              value={formData.num_rooms}
              onChange={handleChange}
              min={1}
              className="input"
          />
        </div>
        <div className="formGroup">
          <label htmlFor="group_children">Children:</label>
          <input
              type="number"
              id="group_children"
              name="group_children"
              value={formData.group_children}
              onChange={handleChange}
              min={0}
              className="input"
          />
        </div>
        <div className="formGroup">
          <label htmlFor="selected_currency">Currency:</label>
          <input
              type="text"
              id="selected_currency"
              name="selected_currency"
              value={formData.selected_currency}
              onChange={handleChange}
              maxLength={10}
              className="input"
              required
          />
        </div>
        <div className="formGroup">
          <label htmlFor="hotel_filter">Scrape Hotel Properties Only:</label>
          <input
              type="checkbox"
              id="hotel_filter"
              name="hotel_filter"
              checked={formData.hotel_filter}
              onChange={handleChange}
              className="checkbox"
          />
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
