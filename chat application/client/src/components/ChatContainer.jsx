import PropTypes from 'prop-types';

const ChatContainer = (props)=>{
    return (
        
            <div className="card border-2 border-info w-100 h-100">
              <div className="row vh-80">
                <div className="d-flex flex-column col-12 h-100">
                    {props.children}
                </div>
              </div>
            </div>
    );
};

ChatContainer.propTypes = {
    children: PropTypes.node
};

export default ChatContainer;