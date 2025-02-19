import PropTypes from 'prop-types';

const ChatInput = ({message,sendMessage})=>{
    return (
        <div className="mt-auto align-items-end border-top border-info py-3 px-4 w-100 d-lg-block">
        <div className="input-group flex-fill">
          <input type="text" className="form-control" name="message" value={message} placeholder="Type your message..." onChange={(e) => sendMessage(e.target.value)} />
          <button className="btn btn-info">send</button>
        </div>
      </div>)
};

ChatInput.propTypes = {
  message: PropTypes.string.isRequired,
  setMessage: PropTypes.func.isRequired,
};

export default ChatInput;