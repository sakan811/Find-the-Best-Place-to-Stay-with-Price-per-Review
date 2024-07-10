import React, { useState, useEffect } from 'react';
import { Table, Button, Alert } from 'react-bootstrap';
import axios from 'axios';
import './HotelTable.css';

const HotelTable = () => {
    const [data, setData] = useState([]);
    const [bookingDetails, setBookingDetails] = useState([]);
    const [successMsg, setSuccessMsg] = useState(false);
    const [errorMsg, setErrorMsg] = useState(false);

    useEffect(() => {
        fetchData();
        fetchBookingDetails();
    }, []);

    const fetchData = async () => {
        try {
            const response = await axios.get('/get_hotel_data_from_db/');
            const responseData = response.data.hotel_data;
            console.log('Fetched data:', responseData);  // Debugging statement
            setData(responseData);
        } catch (error) {
            console.error('Error fetching data:', error);
        }
    };

    const fetchBookingDetails = async () => {
        try {
            const response = await axios.get('/get_booking_details_from_db/');
            const responseData = response.data.booking_data;
            console.log('Fetched data:', responseData);  // Debugging statement
            setBookingDetails(responseData);
        } catch (error) {
            console.error('Error fetching data:', error);
        }
    };

    const saveData = async () => {
        try {
            await axios.post('/save/', {});
            setSuccessMsg(true);
            setErrorMsg(false);
        } catch (error) {
            console.error('Error saving data:', error);
            setSuccessMsg(false);
            setErrorMsg(true);
        }
    };

    const goToFormPage = () => {
        try {
            window.location.href = '/';
        } catch (error) {
            console.error('Error redirecting to form page:', error);
        }
    };

    const formatNumber = (value) => {
        const number = parseFloat(value);
        return isNaN(number) ? value : number.toLocaleString(number, {
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
        });
    };


    return (
        <>
            <Button variant="primary" className="backToFormButton" onClick={goToFormPage}>Back to Form</Button>
            <h2 style={{textAlign: 'center'}}>Hotels' Room Price/Review Data</h2>
            <p style={{textAlign: 'center', fontSize: '16px'}}>
                A lower Price/Review Score indicates that the place isn't expensive, yet, with a great review score
            </p>
            <Button variant="success" className="saveDataButton" onClick={saveData}>Save Data to Excel</Button>

            {successMsg && (
                <Alert variant="success" className="message">
                    <strong>Success!</strong> Saved data to Excel successfully at <strong>scraped_hotel_data</strong> folder.
                </Alert>
            )}
            {errorMsg && (
                <Alert variant="danger" className="errorMessage">
                    <strong>Error!</strong> Failed to save data.
                </Alert>
            )}

            <h3 style={{ marginBottom: '5px' }}>Booking Details</h3>
            {
                bookingDetails.length > 0 && (
                    <div className="booking-details">
                        <p className="detail-item"><strong>City</strong>: {bookingDetails[0].city}</p>
                        <p className="detail-item"><strong>Check In</strong>: {bookingDetails[0].check_in}</p>
                        <p className="detail-item"><strong>Check Out</strong>: {bookingDetails[0].check_out}</p>
                        <p className="detail-item"><strong>Adults</strong>: {bookingDetails[0].num_adults}</p>
                        <p className="detail-item"><strong>Children</strong>: {bookingDetails[0].num_children}</p>
                        <p className="detail-item"><strong>Rooms</strong>: {bookingDetails[0].num_rooms}</p>
                        <p className="detail-item"><strong>Currency</strong>: {bookingDetails[0].currency}</p>
                        <p className="detail-item"><strong>Only Hotel Properties</strong>: {bookingDetails[0].only_hotel.toString()}</p>
                    </div>
                )
            }

            <Table striped bordered hover className="hotelTable">
                <thead>
                    <tr>
                        <th>City</th>
                        <th>Hotel</th>
                        <th>Review</th>
                        <th>Price</th>
                        <th>Price/Review</th>
                        <th>Check In</th>
                        <th>Check Out</th>
                    </tr>
                </thead>
                    <tbody>
                        {data.map((hotel, index) => (
                            <tr key={index}>
                                <td>{hotel.city}</td>
                                <td>{hotel.hotel}</td>
                                <td>{formatNumber(hotel.review_score)}</td>
                                <td>{formatNumber(hotel.room_price)}</td>
                                <td>{formatNumber(hotel.price_per_review)}</td>
                                <td>{hotel.check_in}</td>
                                <td>{hotel.check_out}</td>
                            </tr>
                        ))}
                    </tbody>
            </Table>
        </>
    );
};

export default HotelTable;
