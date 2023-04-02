import Spinner from 'react-bootstrap/Spinner';

const Loading = () => {
  return (
    <div className="Loading">
      <div style={{ fontSize: "2em"}}>
        <p> Loading... </p>
      </div>
      <Spinner animation="border"
               role="status">
        <span style={{ visibility: "hidden" }}>Loading...</span>
      </Spinner>
    </div>
  );
}

export default Loading;