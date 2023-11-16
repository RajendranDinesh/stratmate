import React, { useState } from 'react';

import Cookies from 'js-cookie';
import axios from 'axios';

import { SweetAlert } from '../../components/SweetAlert';
import styles from './styles/login.module.css';

function RightContainer() {
    const API_URL = process.env.REACT_APP_API_URL;

    const [data, setData] = useState({
        email: "",
        password: "",
    });

    const handleDataChange = (e) => {
        setData({
            ...data,
            [e.target.name]: e.target.value
        });
    };

    const handleLoginSubmit = async (e) => {
        e.preventDefault();
        try {
          const response = await axios.post(`${API_URL}/api/login`, 
          JSON.stringify(data), {
            headers: {
              'Content-Type': 'application/json'
            }
          });

          if (response.status === 200) {
            window.location = '/';
            Cookies.set('authToken', response.data.token);
          }
        } catch (error) {
            
          if (error.response && error.response.status >= 400 && error.response.status < 500) {
                await SweetAlert({
                title: error.response.data.detail ? 'OOps..' : "It's not you, it's us.",
                children: error.response.data.detail ? error.response.data.detail : 'Please try again later.',
                icon: "warning"
                });            
          }
          else {
            await SweetAlert({
                title: "It's not you, it's us.",
                children: 'Please try again later.',
                icon: "warning"
              });
          }
        }
    };

    return(
        <div className={styles.right_container}>
            <div className={styles.login_form_container}>
                <form className={styles.login_form}>
                    <div>
                        <span>Username</span>
                        <input value={data.email} name='email' onChange={handleDataChange} placeholder='Username' autoComplete='off' type='text' required/>
                    </div>

                    <div>
                        <span>Password</span>
                        <input value={data.password} name='password' onChange={handleDataChange} placeholder='Password' autoComplete='off' type='password' required/>
                    </div>

                    <div>
                        <button onClick={handleLoginSubmit}>
                           <span>Login</span>
                        </button>
                    </div>
                </form>
            </div>
        </div>
    )
}

export default RightContainer;