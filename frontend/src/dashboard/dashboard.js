import Top50 from "./components/top50";
import User from "./components/user";
import styles from './components/styles/dashboard.module.css';

function Dashboard() {
    return(
        <div className={styles.dashboard} >
            <Top50 />
            <User />
        </div>
    );
}

export default Dashboard;