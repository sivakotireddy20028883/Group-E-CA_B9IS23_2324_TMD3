import React from 'react';
import { Link } from 'react-router-dom';
import './AdminDashboard.css';

const AdminDashboard = ({ username, onLogout }) => {
    const handleLogout = () => {
        if (typeof onLogout === 'function') {
            onLogout(); // Ensure onLogout is properly passed and invoked
        }
    };

    return (
        <div className="admin-dashboard">
            <h1>Welcome to Your Dashboard, {username}!</h1>
            <nav>
                <ul>
                    <li><Link to="/api/admin/menu">Manage Menu</Link></li>
                    <li><Link to="/api/admin/reservations">Manage Reservations</Link></li>
                    <li><Link to="/api/admin/orders">Manage Orders</Link></li>
                    <li><button onClick={handleLogout}>Logout</button></li>
                </ul>
            </nav>
        </div>
    );
};

export default AdminDashboard;
