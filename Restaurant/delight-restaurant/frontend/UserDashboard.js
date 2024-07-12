import React from 'react';
import { Link } from 'react-router-dom';
import './UserDashboard.css';

const UserDashboard = ({ username, onLogout }) => {
    const handleLogout = () => {
        if (typeof onLogout === 'function') {
            onLogout();
        }
    };

    return (
        <div className="user-dashboard">
            <h1>Welcome to Your Dashboard, {username}!</h1>
            <nav>
                <ul>
                    <li><Link to="/api/user/menu">View Menu</Link></li>
                    <li><Link to="/api/reservation">Book/Reserve a Table</Link></li>
                    <li><Link to="/api/orders">Place Order</Link></li>

                    <li><button onClick={handleLogout}>Logout</button></li>
                </ul>
            </nav>
        </div>
    );
};

export default UserDashboard;
