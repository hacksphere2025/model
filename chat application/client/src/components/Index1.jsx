import { useState, useEffect } from 'react';
import PropTypes from 'prop-types';
import Login from './Login';
import Chat from './Chat';

const Index = ({ socket }) => {
  const [newUser, setNewUser] = useState("");
  const [user, setUser] = useState({});
  const [users, setUsers] = useState([]);
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState([]);

  useEffect(() => {
    socket.on("users", (users) => {
      const messagesArr = [];
      for (const { userId, username } of users) {
        const newMessage = { type: "UserStatus", userId, username };
        messagesArr.push(newMessage);
      }
      setMessages([...messages, ...messagesArr]);
      setUsers(users);
    });

    socket.on("session", ({ userId, username }) => {
      setUser({ userId, username });
    });

    socket.on("user connected", ({ userId, username }) => {
      const newMessage = { type: "UserStatus", userId, username };
      setMessages([...messages, newMessage]);
    });
  }, [socket, messages]);

  function logNewUser() {
    setUser({ username: newUser });
    socket.auth = { username: newUser };
    socket.connect();
  }
  function sendMessage() {
    socket.emit("new message", message);
    const newMessage = { type: "message", 
      userId: user.userId, 
      username: user.username,
      message,
    };
    setMessages([...messages, newMessage])
    setMessage("");
  }
  return (
    <main className="content">
      <div className="container mt-3">
        {user.userId && (
          <Chat user={user} message={message} messages={messages} sendMessage={sendMessage}></Chat>
        )}
        {!user.userId && (
          <Login newUser={newUser} setNewUser={setNewUser} logNewUser={logNewUser}></Login>
        )}
      </div>
    </main>
  );
};

Index.propTypes = {
  socket: PropTypes.object.isRequired,
};

export default Index;