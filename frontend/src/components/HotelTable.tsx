import React, {useState, useEffect} from 'react';
import { Table, Button, Alert } from 'react-bootstrap';
import axios, { AxiosResponse, AxiosRequestConfig } from 'axios';
import './HotelTable.css';

interface HotelData {
    city: string;
    hotel: string;
    review_score: number;
    room_price: number;
    price_per_review: number;
    check_in: string;
    check_out: string;
    accommodation_name: string;
}

interface BookingDetail {
    city: string;
    check_in: string;
    check_out: string;
    num_adults: number;
    num_children: number;
    num_rooms: number;
    currency: string;
    only_hotel: boolean;
}

const HotelTable: React.FC = () => {
    const [data, setData] = useState<HotelData[]>([]);
    const [bookingDetails, setBookingDetails] = useState<BookingDetail[]>([]);
    const [successMsg, setSuccessMsg] = useState<boolean>(false);
    const [errorMsg, setErrorMsg] = useState<boolean>(false);

    useEffect(() => {
        fetchData();
        fetchBookingDetails();
    }, []);

    const fetchData = async () => {
        try {
            const response = await axios.get<{ hotel_data: HotelData[] }>('http://localhost:8000/get_hotel_data_from_db/');
            const responseData: HotelData[] = response.data.hotel_data;
            setData(responseData);
        } catch (error) {
            console.error('Error fetching data:', error);
        }
    };

    const fetchBookingDetails = async () => {
        try {
            const response: AxiosResponse<{ booking_data: BookingDetail[] }> = await axios.get('http://localhost:8000/get_booking_details_from_db/');
            const responseData: BookingDetail[] = response.data.booking_data;
            
            // Sort booking details to get the most recent one first
            // Assuming the backend returns records with an 'id' field
            const sortedData = [...responseData].sort((a, b) => {
                // If there's an ID field, sort by ID in descending order
                if ('id' in a && 'id' in b) {
                    return (b.id as number) - (a.id as number);
                }
                // Fallback to sorting by date if no ID
                return new Date(b.check_in).getTime() - new Date(a.check_in).getTime();
            });
            
            setBookingDetails(sortedData);
        } catch (error) {
            console.error('Error fetching booking details:', error);
        }
    };

    const saveData = async () => {
        try {
            const saveDataUrl = 'http://localhost:8000/save/';
            const data = {};
            const config: AxiosRequestConfig = { responseType: 'json' };

            const response: AxiosResponse<{ filename: string; file_content: string }> = await axios.post(
                saveDataUrl,
                data,
                config
            );

            const { filename, file_content } = response.data;
            const binaryString: string = atob(file_content);

            const bytes = new Uint8Array(binaryString.length);
            for (let i = 0; i < binaryString.length; i++) {
                bytes[i] = binaryString.charCodeAt(i);
            }

            const blob = new Blob([bytes], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' });
            const url: string = URL.createObjectURL(blob);

            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', filename);
            document.body.appendChild(link);
            link.click();
            link.remove();

            URL.revokeObjectURL(url);

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

    const formatNumber = (value: number | string): string => {
        const number: number = typeof value === 'string' ? parseFloat(value) : value;
        return isNaN(number)
            ? value.toString()
            : number.toLocaleString(undefined, {
                  minimumFractionDigits: 2,
                  maximumFractionDigits: 2,
              });
    };

    return (
        <>
            <title>Find the Best Place to Stay with Price/Review - Table</title>
            <Button variant="primary" className="backToFormButton" onClick={goToFormPage}>
                Back to Form
            </Button>
            <h2 style={{ textAlign: 'center' }}>Hotels&apos; Room Price/Review Data</h2>
            <p style={{ textAlign: 'center', fontSize: '16px' }}>
                A lower Price/Review Score indicates that the place isn&apos;t expensive, yet, with a great review score
            </p>
            <Button variant="success" className="saveDataButton" onClick={saveData}>
                Save Data to Excel
            </Button>

            {successMsg && (
                <Alert variant="success" className="message">
                    <strong>Success!</strong> Saved data to Excel successfully.
                </Alert>
            )}
            {errorMsg && (
                <Alert variant="danger" className="errorMessage">
                    <strong>Error!</strong> Failed to save data.
                </Alert>
            )}

            <h3 style={{ marginBottom: '5px' }}>Booking Details</h3>
            {bookingDetails.length > 0 && (
                <div className="booking-details">
                    <p className="detail-item">
                        <strong>City</strong>: {bookingDetails[0].city}
                    </p>
                    <p className="detail-item">
                        <strong>Check In</strong>: {bookingDetails[0].check_in}
                    </p>
                    <p className="detail-item">
                        <strong>Check Out</strong>: {bookingDetails[0].check_out}
                    </p>
                    <p className="detail-item">
                        <strong>Adults</strong>: {bookingDetails[0].num_adults}
                    </p>
                    <p className="detail-item">
                        <strong>Children</strong>: {bookingDetails[0].num_children}
                    </p>
                    <p className="detail-item">
                        <strong>Rooms</strong>: {bookingDetails[0].num_rooms}
                    </p>
                    <p className="detail-item">
                        <strong>Currency</strong>: {bookingDetails[0].currency}
                    </p>
                    <p className="detail-item">
                        <strong>Only Hotel Properties</strong>: {bookingDetails[0].only_hotel ? "Yes" : "No"}
                    </p>
                </div>
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
                        <th>Accommodation Type</th>
                    </tr>
                </thead>
                <tbody>
                    {data && data.map((hotel, index) => (
                        <tr key={index}>
                            <td>{hotel.city}</td>
                            <td>{hotel.hotel}</td>
                            <td>{formatNumber(hotel.review_score)}</td>
                            <td>{formatNumber(hotel.room_price)}</td>
                            <td>{formatNumber(hotel.price_per_review)}</td>
                            <td>{hotel.check_in}</td>
                            <td>{hotel.check_out}</td>
                            <td>{hotel.accommodation_name}</td>
                        </tr>
                    ))}
                </tbody>
            </Table>
        </>
    );
};

export default HotelTable;
