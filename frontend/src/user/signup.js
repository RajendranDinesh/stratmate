import SignUpRightContainer from "./components/signUpRightContainer";
import LeftContainer from "./components/leftContainer";

import styles from "./components/styles/login.module.css";

function SignUp() {
    return(
        <div className={styles.login_container}>
            <LeftContainer />
            <SignUpRightContainer />
        </div>
    )
}

export default SignUp;