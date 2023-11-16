import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

import axios from "axios";
import Cookies from "js-cookie";

import styles from "./components/styles/user.module.css";

import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Filler,
    Legend,
} from 'chart.js';
import { Line } from 'react-chartjs-2';
import { faker } from '@faker-js/faker';
import { SweetAlert } from "../components/SweetAlert";

ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Filler,
    Legend
);

const options = {
    responsive: true,
    plugins: {
        legend: {
            position: 'top',
        },
        title: {
            display: true,
            text: 'Rating History',
        },
    },
};

const labels = ['Today', 'Day 2', 'Day 3', 'Day 4', 'Day 5', 'Day 6',
    'Day 7', 'Day 8', 'Day 9', 'Day 10', 'Day 11', 'Day 12',
    'Day 13', 'Day 14', 'Day 15', 'Day 16', 'Day 17', 'Day 18',
    'Day 19', 'Day 20', 'Day 21', 'Day 22', 'Day 23', 'Day 24',
    'Day 25', 'Day 26', 'Day 27', 'Day 28', 'Day 29', 'Month ago'];

const dummyData = {
    labels,
    datasets: [
      {
        fill: true,
        label: 'Dataset 2',
        data: labels.map(() => faker.number.int({ min: 0, max: 1000 })),
        borderColor: 'rgb(53, 162, 235)',
        backgroundColor: 'rgba(53, 162, 235, 0.5)',
      },
    ],
  };

function UserDashboard() {

    const { username } = useParams();
    const API_URL = process.env.REACT_APP_API_URL;
    const authToken = Cookies.get("authToken");

    const [player, setPlayer] = useState(dummyData);

    useEffect(() => {
        document.title = `User Dashboard | ${username}`;

        const fetchData = async () => {
            try {
                const result = await axios.get(`${API_URL}/api/player/${username}/rating-history`,
                    {
                        headers: {
                            Authorization: `Bearer ${authToken}`
                        }
                    });

                let ratingData = [];
                for (let i = 0; i < 30; i++) {
                    ratingData.push(result.data[`day_${i+1}`]);
                }

                setPlayer({
                    labels: labels,
                    datasets: [
                        {
                            label: 'Rating',
                            data: ratingData,
                            fill: true,
                            backgroundColor: 'rgb(255, 99, 132)',
                            borderColor: 'rgba(255, 99, 132, 0.2)',
                        },
                    ],
                });
            } catch (error) {
                await SweetAlert({
                    title: "Oops..",
                    text: error.response,
                    icon: "error",
                    button: "Ok",
                });
            }
        };

        fetchData();
    }, [username, API_URL, authToken]);

    return (
        <div className={styles.user_dashboard}>
            <h1>User Dashboard</h1>
            <h2>{username}</h2>

            <div className={styles.rating_30days}>
                {player && <Line data={player} options={options} />}
            </div>
        </div>
    );
}

export default UserDashboard;