import React, { useState } from 'react';
import axios from 'axios';
import './ContactUs.css';

const ContactUs = () => {

    return (
        <div className="contact-container">
            <h2>Contact Us</h2>
            <div className="contact-details">
                <p>Address: 123 Delight Street, Food City</p>
                <p>Phone: (123) 456-7890</p>
                <p>Email: info@delightrestaurant.com</p>
            </div>
        </div>
    );
};

export default ContactUs;
