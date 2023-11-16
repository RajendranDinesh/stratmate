import RightContainer from "./components/rightContainer";
import LeftContainer from "./components/leftContainer";

import styles from "./components/styles/login.module.css";

function Login() {
    return(
        <div className={styles.login_container}>
            <LeftContainer />
            <RightContainer />
        </div>
    )
}

export default Login;