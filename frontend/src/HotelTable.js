import React, { useState, useEffect } from 'react';
import { Table, Button, Alert } from 'react-bootstrap';
import axios from 'axios';
import './HotelTable.css';

const HotelTable = () => {
    const [data, setData] = useState([]);
    const [successMsg, setSuccessMsg] = useState(false);
    const [errorMsg, setErrorMsg] = useState(false);

    useEffect(() => {
        fetchData();
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
        axios.post('/', {})
        .then(() => {
            window.location.href = '/';
        })
        .catch(error => {
            console.error('Error redirecting to form page:', error);
        });
    };


    return (
        <>
            <Button variant="primary" className="backToFormButton" onClick={goToFormPage}>Back to Form</Button>
            <h2 style={{textAlign: 'center'}}>Hotels' Room Price/Review Data</h2>
            <p style={{textAlign: 'center'}}>A lower Price/Review Score indicates that the place isn't expensive, yet, with a great review score</p>
            <Button variant="success" className="saveDataButton" onClick={saveData}>Save Data to Excel</Button>

            {successMsg && (
                <Alert variant="success" className="message">
                    <strong>Success!</strong> Saved data to Excel successfully at 'scraped_hotel_data' folder.
                </Alert>
            )}
            {errorMsg && (
                <Alert variant="danger" className="message">
                    <strong>Error!</strong> Failed to save data.
                </Alert>
            )}

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
                            <td>{hotel.review_score}</td>
                            <td>{hotel.room_price}</td>
                            <td>{hotel.price_per_review}</td>
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
