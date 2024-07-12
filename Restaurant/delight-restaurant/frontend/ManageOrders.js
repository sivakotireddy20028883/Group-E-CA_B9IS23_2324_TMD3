import React, { useState, useEffect } from 'react';
import axios from 'axios';
import AdminDashboard from './AdminDashboard';
import './ManageOrders.css';

const ManageOrders = ({ username, onLogout }) => {
  const [orders, setOrders] = useState([]);
  const [sortOrder, setSortOrder] = useState('desc');

  useEffect(() => {
    fetchOrders();
  }, [sortOrder]);

  const fetchOrders = () => {
    axios.get(`http://localhost:5000/api/admin/orders?sort_order=${sortOrder}`)
      .then(response => {
        setOrders(response.data);
      })
      .catch(error => {
        console.error('Error fetching orders:', error);
      });
  };

  return (
    <div className="container">
      <AdminDashboard username = {username} onLogout={onLogout} />
      <h2>Manage Orders</h2>
      <div className="sort-container">
        <label>Sort by Date: </label>
        <select onChange={(e) => setSortOrder(e.target.value)} value={sortOrder}>
          <option value="desc">Descending</option>
          <option value="asc">Ascending</option>
        </select>
      </div>
      <div>
        {orders.map(order => (
          <div key={order.id} className="order">
            <div className="order-header">
              <h2>Order ID: {order.id}</h2>
              <p>Order Date: {order.order_date}</p>
            </div>
            <div className="order-details">
              <p>User ID: {order.user_id}</p>
              <p>Total Amount: ${order.total_amount}</p>
            </div>
            <div className="order-items">
              <h3>Items</h3>
              <div className="order-item-container">
                {order.items.map(item => (
                  <div key={item.menu_item_id} className="order-item">
                    <span>Item Id: {item.menu_item_id}</span><br></br>
                    <span>Quantity: {item.quantity}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ManageOrders;
