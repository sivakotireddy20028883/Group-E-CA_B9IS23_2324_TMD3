import React, { useState } from 'react';
import axios from 'axios';

const MenuItemForm = ({ onSubmit, item }) => {
    const [name, setName] = useState(item ? item.name : '');
    const [description, setDescription] = useState(item ? item.description : '');
    const [price, setPrice] = useState(item ? item.price : '');
    const [quantity, setQuantity] = useState(item ? item.quantity : 1);
    const [availability, setAvailability] = useState(item ? item.availability : true);

    const handleSubmit = async (event) => {
        event.preventDefault();
        const menuItemData = {
            name,
            description,
            price,
            quantity,
            availability
        };
        try {
            await onSubmit(menuItemData);
        } catch (error) {
            console.error('Error submitting menu item:', error);
        }
    };

    return (
        <form onSubmit={handleSubmit}>
            <div>
                <label>Name</label>
                <input type="text" value={name} onChange={(e) => setName(e.target.value)} required />
            </div>
            <div>
                <label>Description</label>
                <input type="text" value={description} onChange={(e) => setDescription(e.target.value)} />
            </div>
            <div>
                <label>Price</label>
                <input type="number" step="0.01" value={price} onChange={(e) => setPrice(e.target.value)} required />
            </div>
            <div>
                <label>Quantity</label>
                <input type="number" value={quantity} onChange={(e) => setQuantity(e.target.value)} required />
            </div>
            <div>
                <label>Availability</label>
                <input type="checkbox" checked={availability} onChange={(e) => setAvailability(e.target.checked)} />
            </div>
            <button type="submit">Submit</button>
        </form>
    );
};

export default MenuItemForm;
