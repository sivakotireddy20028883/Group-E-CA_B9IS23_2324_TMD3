import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate, Link } from 'react-router-dom';
import Home from './components/Home';
import ReserveTable from './components/ReserveTable';
import ContactUs from './components/ContactUs';
import PlaceOrder from './components/PlaceOrder';
import AdminDashboard from './components/AdminDashboard';
import UserDashboard from './components/UserDashboard';
import ManageMenu from './components/ManageMenu';
import ManageOrders from './components/ManageOrders';
import Register from './components/Register';
import Login from './components/Login';
import Menu from './components/Menu';
import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import DashboardMenu from './components/DashboardMenu';

const App = () => {
    const [isLoggedIn, setIsLoggedIn] = useState(false);
    const [user, setUser] = useState(null);

    const handleLogin = (loggedInUser) => {
        setUser(loggedInUser);
        setIsLoggedIn(true);
    };

    const handleLogout = () => {
        localStorage.removeItem('token');
        setUser(null);
        setIsLoggedIn(false);
    };

    return (
        <Router>
            <div className="app-container">
                <Routes>
                    <Route path="/" element={<Home onLogin={handleLogin} />} />
                    <Route path="/api/menu" element={<Menu />} />
                    <Route path="/api/reservation" element={<ReserveTable />} />
                    <Route path="/api/contact" element={<ContactUs />} />
                    <Route path="/api/orders" element={<PlaceOrder />} />
                    <Route path="/api/register" element={<Register />} />
                    <Route path="/api/login" element={<Login onLogin={handleLogin} />} />
                    
                    {user && user.role === 'admin' && (
                        <>
                            <Route path="/api/admin/dashboard" element={<AdminDashboard username={user.username} onLogout={handleLogout} />} />
                            <Route path="/api/admin/menu" element={<ManageMenu username={user.username} onLogout={handleLogout}/>} />
                            <Route path="/api/admin/reservations" element={<ManageReservations username={user.username} onLogout={handleLogout}/>} />
                            <Route path="/api/admin/orders" element={<ManageOrders username={user.username} onLogout={handleLogout}/>} />
                            <Route path="/api/admin" element={<Navigate to="/api/admin/dashboard" username={user.username} onLogout={handleLogout}/>} />
                        </>
                    )}

                    {user && user.role === 'user' && (
                        <>
                            <Route path="/api/user/dashboard" element={<UserDashboard username={user.username} onLogout={handleLogout} />} />
                            <Route path="/api/user/menu" element={<DashboardMenu username={user.username} onLogout={handleLogout}/>} />
                            <Route path="/api/reservation" element={<ReserveTable username={user.username} onLogout={handleLogout}/>} />
                            <Route path="/api/orders" element={<PlaceOrder username={user.username} onLogout={handleLogout}/>} />
                            <Route path="/user" element={<Navigate to="/api/user/dashboard" username={user.username} onLogout={handleLogout}/>} />
                        </>
                    )}

                    {!isLoggedIn && (
                        <>
                            <Route path="/api/login" element={<Login onLogin={handleLogin} />} />
                            <Route path="/api/register" element={<Register />} />
                            <Route path="*" element={<Navigate to="/" />} />
                        </>
                    )}
                </Routes>
            </div>
        </Router>
    );
};

export default App;
