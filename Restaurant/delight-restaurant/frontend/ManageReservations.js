import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './ManageReservations.css';
import AdminDashboard from './AdminDashboard'; // Import your AdminDashboard component

const ManageReservations = ({ username, onLogout }) => {
    const [reservations, setReservations] = useState([]);
    const [newReservation, setNewReservation] = useState({ name: '', date: '', time: '', people: '' });
    const [editingReservation, setEditingReservation] = useState(null);
    const [sortBy, setSortBy] = useState('date');
    const [sortOrder, setSortOrder] = useState('asc');
    const [error, setError] = useState('');

    useEffect(() => {
        fetchReservations();
    }, [sortBy, sortOrder]);

    const fetchReservations = async () => {
        try {
            const response = await axios.get('http://localhost:5000/api/admin/reservations', {
                params: {
                    sort_by: sortBy,
                    order: sortOrder
                }
            });
            setReservations(response.data);
        } catch (error) {
            console.error('Error fetching reservations', error);
            setError('Failed to fetch reservations.');
        }
    };

    const handleUpdateReservation = async (id) => {
        try {
            const response = await axios.put(`http://localhost:5000/api/admin/reservations/${id}`, editingReservation);
            setReservations(reservations.map(res => (res.id === id ? response.data : res)));
            setEditingReservation(null);
        } catch (error) {
            console.error('Error updating reservation', error);
            setError('Failed to update reservation.');
        }
    };

    const handleDeleteReservation = async (id) => {
        try {
            await axios.delete(`http://localhost:5000/api/admin/reservations/${id}`);
            setReservations(reservations.filter(res => res.id !== id));
        } catch (error) {
            console.error('Error deleting reservation', error);
            setError('Failed to delete reservation.');
        }
    };

    const handleInputChange = (event) => {
        const { name, value } = event.target;
        setNewReservation({ ...newReservation, [name]: value });
    };

    const handleEditInputChange = (event) => {
        const { name, value } = event.target;
        setEditingReservation({ ...editingReservation, [name]: value });
    };

    const toggleEditing = (id) => {
        const reservationToEdit = reservations.find(res => res.id === id);
        setEditingReservation(reservationToEdit);
    };

    const handleCancelEdit = () => {
        setEditingReservation(null);
    };

    const handleSort = (sortField) => {
        if (sortBy === sortField) {
            setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc');
        } else {
            setSortBy(sortField);
            setSortOrder('asc');
        }
    };

    return (
        <div className="reservation-manager">
            <AdminDashboard username = {username} onLogout={onLogout} /> {/* Assuming AdminDashboard exists */}
            <h1>Manage Reservations</h1>
            <div className="reservation-list">
                <div className="sort-options">
                    <button onClick={() => handleSort('date')}>
                        Sort by Date {sortBy === 'date' && (sortOrder === 'asc' ? '↑' : '↓')}
                    </button>
                    <button onClick={() => handleSort('booking_date')}>
                        Sort by Booking Time {sortBy === 'booking_date' && (sortOrder === 'asc' ? '↑' : '↓')}
                    </button>
                </div>
                {reservations.map(res => (
                    <div key={res.id} className="reservation-item">
                        {editingReservation && editingReservation.id === res.id ? (
                            <div>
                                <input type="text" name="name" value={editingReservation.name} onChange={handleEditChange} />
                                <input type="date" name="date" value={editingReservation.date} onChange={handleEditChange} />
                                <input type="time" name="time" value={editingReservation.time} onChange={handleEditChange} />
                                <input type="number" name="people" value={editingReservation.people} onChange={handleEditChange} />
                                <button onClick={() => handleUpdateReservation(res.id)}>Save</button>
                                <button onClick={() => setEditingReservation(null)}>Cancel</button>
                            </div>
                        ) : (
                            <div>
                                <p>Name: {res.name}</p>
                                <p>Date: {res.date}</p>
                                <p>Time: {res.time}</p>
                                <p>People: {res.people}</p>
                            </div>
                        )}
                    </div>
                ))}
            </div>
            {error && <p className="error">{error}</p>}
        </div>
    );
};

export default ManageReservations;
