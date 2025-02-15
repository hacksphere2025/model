import "bootstrap/dist/css/bootstrap.min.css";
import "font-awesome/css/font-awesome.css";
// import './App.css';
import Index from './components/Index1';
import {io} from 'socket.io-client';

const socket = io("http://localhost:4000");

function App() {

  return (
    <Index socket={socket}/>

  );
}

export default App;