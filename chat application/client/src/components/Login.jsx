import PropTypes from 'prop-types';

const Login = ({ newUser, setNewUser, logNewUser }) => {
  return (
    <div className="card w-100 text-center border-white">
      <div className="row">
        <div className="col-12">
          <h5>Enter the userName : </h5>
        </div>
        <div className="d-flex justify-content-center py-1">
          <div className="col-4">
            <input
              type="text"
              name="username"
              value={newUser}
              className="form-control mb-4"
              placeholder="username"
              autoComplete="off"
              onChange={(e) => setNewUser(e.target.value)}
              onKeyPress={(e) => (e.code === "Enter" ? logNewUser() : null)}
            />
            <button className="btn btn-success w-100" onClick={logNewUser}>
              Join!
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

Login.propTypes = {
  newUser: PropTypes.string.isRequired,
  setNewUser: PropTypes.func.isRequired,
  logNewUser: PropTypes.func.isRequired,
};

export default Login;