import PropTypes from 'prop-types';
import ChatHeader from './ChatHeader';
import ChatInput from './ChatInput';
import ChatContainer from './ChatContainer';

const Chat = ({ user ,message, messages,setMessage }) => {
  return (
    <ChatContainer>
     <ChatHeader user={user}></ChatHeader>     
     <div className='position-relative chat-height overflow-auto'>
        <div className='d-flex flex-column p-4'>
            {messages.map((message,index)=>{
                return message.type === "UserStatus" ?(
                <div key={index} className='text-center'>
                    <span className='badge bg-info'>{message.userId === user.userId ?"You have Joined!":`${message.username} has Joined!` }</span>
                </div>):null;
            })}
        </div>
    </div> 

     <ChatInput message={message} setMessage={setMessage}></ChatInput>
     </ChatContainer>
  );
};

Chat.propTypes = {
  user: PropTypes.string.isRequired,
  message: PropTypes.string.isRequired,
  messages:PropTypes.array.isRequired,
  setMessage: PropTypes.func.isRequired,
};

export default Chat;