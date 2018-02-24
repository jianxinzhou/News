import React from 'react';
import PropTypes from 'prop-types';
import Auth from '../Auth/Auth';
import { Link } from 'react-router';
import './Base.css';

// 此处定义的是函数，在react中可以使用class定义conponent，也可以使用函数定义conponent
const Base = ({children}) => (
    <div>
        <nav className="nav-bar indigo lighten-1">
            <div className="nav-wrapper">
                 <a href="/" className="brand-logo">&nbsp;&nbsp;Tap News</a>
                 <ul id="nav-mobile" className="right">
                    {Auth.isUserAuthenticated()?
                        (<div>
                            <li>{Auth.getEmail()}</li>
                            <li><Link to="/logout">Log out</Link></li>
                        </div>)
                        :
                        (<div>
                            <li><Link to="/login">Log in</Link></li>
                            <li><Link to="/signup">Sign up</Link></li>
                        </div>)
                    }
                </ul>
            </div>
        </nav>
        <br/>
        { children }
    </div>
);

Base.PropTypes = {
    children: PropTypes.object.isRequired
};

export default Base;
