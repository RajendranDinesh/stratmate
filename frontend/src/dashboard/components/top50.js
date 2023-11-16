import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Cookies from 'js-cookie';

import styles from './styles/top50.module.css';

import Down from './assets/down.png';
import Up from './assets/up.png';
import Pawn from './assets/pawn.png';
import rating from './assets/rating.png';

function Top50() {
    const API_URL = process.env.REACT_APP_API_URL;
    const authToken = Cookies.get('authToken');
    const [players, setPlayers] = useState([]);

    useEffect(() => {
        const fetchData = async () => {
        const result = await axios.get(`${API_URL}/api/top-players`, 
            { headers: { Authorization: `Bearer ${authToken}` } });
        setPlayers(result.data);
        };

        fetchData();
    }, [API_URL, authToken]);

    const handleRedirect = (username) => {
        window.location.href = `/user/${username}`;
    }

    return (
        <div className={styles.top_container}>
            <h2>Top 50 Players</h2>

            <div className={styles.player_container}>
                {players.map((player, index) => (
                    <div key={index} className={styles.player_card} onClick={() => handleRedirect(player[0])}>
                        <div className={styles.player_rank}>
                            <img src={Pawn} alt={`${player[0]}_pawn`}/>
                            <p>{player[0]}</p>
                        </div>
                        <div className={styles.player_name}>
                            <img src={rating} alt={`${player[1]}_rating`}/>
                            <p>{player[1]}</p>
                        </div>
                        <div className={styles.player_points}>
                            {
                                player[2] > 0 ?
                                <img src={Up} alt={`${player[2]}_up`}/> : <img src={Down} alt={`${player[2]}_down`}/>
                            }
                            <p>{player[2]}</p>
                        </div>
                    </div>
                ))}
            </div>

        </div>
    );
}

export default Top50;