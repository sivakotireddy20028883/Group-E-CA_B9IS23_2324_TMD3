import React from 'react';
import DashboardHeader from './DashboardHeader';
import Menu from './Menu';
import DashboardMenu from './DashboardMenu';

const MenuPage = ({ username, role, onLogout }) => {
    return (
        <div>
            <DashboardMenu />
        </div>
    );
};

export default MenuPage;
