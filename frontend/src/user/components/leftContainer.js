import styles from './styles/login.module.css';
import StratImage from './assets/login.jpeg';

function LeftContainer() {
    return(
        <div className={styles.left_container}>
            <img src={StratImage} alt='strat'/>
        </div>
    )
}

export default LeftContainer;