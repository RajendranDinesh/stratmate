import React, { useState } from 'react';
import axios from 'axios';

import styles from './styles/user.module.css';
import Cookies from 'js-cookie';

import { SweetAlert } from '../../components/SweetAlert';
import Spinner from './spinner';

const debounce = (func, delay) => {
    let debounceTimer;
    return function(...args) {
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(() => func.apply(this, args), delay);
    };
;}

function User(){
    const API_URL = process.env.REACT_APP_API_URL;
    const authToken = Cookies.get('authToken');
    const [users, setUsers] = useState(null);

    const [loading, setLoading] = useState(false);

    const getUser = async (e) => {
        await axios.get('https://lichess.org/api/player/autocomplete', {
            params: {
                term: e.target.value
            }
        }).then((response) => {
            setUsers(response.data);
        }).catch((error) => {
            console.log(error);
        });
    }

    const debounceGetUser = debounce(getUser, 500);

    const handleChange = (e) => {
        if (e.target.value.length >= 3) {
            debounceGetUser(e);
        } else {
            setUsers(null);
        }
    }

    const handleClick = (e) => {
        const user = e.target.innerHTML;
        window.location.href = `/user/${user}`;
    }

    const handleRatingDownload = async () => {
        setLoading(true);
        try {
            const response = await axios.get(`${API_URL}/api/players/rating-history-csv`,
                {
                    responseType: 'blob',
                    headers: {
                        Authorization: `Bearer ${authToken}`,
                        'Content-Type': 'application/json',
                        'Accept': 'application/json'
                    }
                });

            const url = window.URL.createObjectURL(new Blob([response.data]));
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', 'rating_history.csv');
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            setLoading(false);
        } catch (error) {
            await SweetAlert({
                title: "Oops..",
                icon: "warning",
                children: 'Please try again later.'
            });
            setLoading(false);
        }
    }

    const handleLogout = async () => {
        Cookies.remove('authToken');
        window.location.href = '/';
    }

    return (
        <div className={styles.user_rating}>
            <div className={styles.user_container}>

                <label htmlFor="user" className={styles.user_label}>Search for an User</label>
                <input id='user' className={styles.user_input} type="text" onChange={handleChange} />

                <div style={{width:'80%'}}>
                    {
                        users ? users.length === 0 ?  <p>No user found</p> : <p>Choose one user to view rating history</p> : <></>
                    }
                { users && users.length > 0 && <div className={styles.options}>
                    {users.map((user, index) => {
                        return (
                            <div className={styles.option} key={index} onClick={handleClick}>{user}</div>
                        )
                    })}
                </div> }
                </div>
            </div>
        
            <div className={styles.rating_download_container}>
                <h4>Download Ratings</h4>
                <p>(Data covers only past 30 day's ratings of Top 50 Players)</p>

                <div className={ loading ? styles.rating_download_disabled : styles.rating_download } onClick={handleRatingDownload}>
                    {
                        loading ?  <Spinner /> : <p>Download</p>
                    }
                </div>

            </div>

            <div className={styles.logout} onClick={handleLogout}>
                <span>Logout</span>
            </div>
        </div>
    );

}

export default User;