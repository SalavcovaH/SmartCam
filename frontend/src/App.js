import React, { useEffect, useRef, useState } from 'react';
import './App.css';

/* Testing app to show webcam stream, button in development*/
const WebcamStream = () => {
  const canvasRef = useRef(null);
  const [message, setMessage] = useState('');

  useEffect(() => {
    const ws = new WebSocket("ws://localhost:8000/ws");

    ws.onmessage = (event) => {
      // Each message is a base64 encoded image
      const img = new Image();
      img.src = `data:image/jpeg;base64,${event.data}`;
      
      img.onload = () => {
        const canvas = canvasRef.current;
        const ctx = canvas.getContext("2d");
        ctx.drawImage(img, 0, 0);
      };
    };

    return () => {
      if (ws) ws.close();
    };
  }, []);

  // Function to fetch message from backend on button click
  const captureImage = async () => {
    try {
      const response = await fetch('http://localhost:8000/save-image');
      const data = await response.json();
      
      // Set the response message in state
      setMessage(data.message);
    } catch (error) {
      console.error('Error fetching message:', error);
    }
  };

  return (
    <div className="App">
      <div className="left-bar">
        <button onClick={captureImage}>Video 1</button>
        <button>Video 2</button>
        <button>Video 3</button>
        {/* Display the fetched message */}
        {message && (
          <div>
            <h1>Backend says:</h1>
            <p>{message}</p>
          </div>
        )}
      </div>

      <div className="right-stream">
        <h1>Welcome to SmartCam!!!</h1>
        <canvas ref={canvasRef} width={640} height={480}></canvas>
      </div>
    </div>
  );
};

export default WebcamStream;
