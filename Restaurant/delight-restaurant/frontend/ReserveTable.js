import React, { useState } from 'react';
import axios from 'axios';
import './ReserveTable.css';
import UserDashboard from './UserDashboard';

const ReserveTable = ({username, onLogout}) => {
    const [name, setName] = useState('');
    const [date, setDate] = useState('');
    const [time, setTime] = useState('');
    const [numberOfGuests, setNumberOfGuests] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            await axios.post('http://localhost:5000/api/reservation', {
                name,
                date,
                time,
                numberOfGuests
            });
            alert('Table reserved successfully!');
            // Clear form inputs after successful submission
            setName('');
            setDate('');
            setTime('');
            setNumberOfGuests('');
        } catch (error) {
            console.error('Error reserving table', error);
            alert('Failed to reserve table');
        }
    };

    return (
        <div className="reserve-table">
            <UserDashboard username = {username} onLogout={onLogout}/>
            <div className="reserve-table-container">
                <h1>Book a Table</h1>
                <form className="reserve-table-form" onSubmit={handleSubmit}>
                    <label>Name</label>
                    <input
                        type="text"
                        value={name}
                        onChange={(e) => setName(e.target.value)}
                        required
                    />
                    <label>Date</label>
                    <input
                        type="date"
                        value={date}
                        onChange={(e) => setDate(e.target.value)}
                        required
                    />
                    <label>Time</label>
                    <input
                        type="time"
                        value={time}
                        onChange={(e) => setTime(e.target.value)}
                        required
                    />
                    <label>Number of Guests</label>
                    <input
                        type="number"
                        value={numberOfGuests}
                        onChange={(e) => setNumberOfGuests(e.target.value)}
                        required
                    />
                    <button type="submit">Reserve</button>
                </form>
            </div>
        </div>
    );
};

export default ReserveTable;
