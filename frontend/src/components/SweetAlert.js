import Swal from 'sweetalert2';
import withReactContent from 'sweetalert2-react-content';

const MySwal = withReactContent(Swal)

const SweetAlert = async ({title, children, icon}) => {
    await MySwal.fire({
        title: title,
        html: children,
        icon: icon? icon : <></>
    }).then(() => {
            return
        }
        );
    };
    
export { SweetAlert };