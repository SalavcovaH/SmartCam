import React, { useState } from 'react';

const CameraSettings = () => {
    // Define state for each camera parameter
    const [brightness, setBrightness] = useState(128);
    const [contrast, setContrast] = useState(5);
    const [saturation, setSaturation] = useState(100);
    const [sharpness, setSharpness] = useState(20);
    const [framerate, setFramerate] = useState(30);

    // Handler to submit data to the backend API
    const handleSubmit = async () => {
        const cameraParams = {
            format: "MJPG",  // You can dynamically set this based on user input if needed
            resolution: "1920x1080",  // You can dynamically set this too
            saturation,
            sharpness,
            framerate,
            contrast,
            brightness
        };

        // Send the parameters to your API
        const response = await fetch('http://localhost:8000/set-camera-parameters', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(cameraParams),
        });

        const result = await response.json();
        console.log(result);
    };

    return (
        <div style={{ padding: '20px' }}>
            <h2>Camera Settings</h2>

            <div>
                <label>Brightness: {brightness}</label>
                <input
                    type="range"
                    min="0"
                    max="255"
                    value={brightness}
                    onChange={(e) => setBrightness(e.target.value)}
                    style={{ width: '100%' }}
                />
            </div>

            <div>
                <label>Contrast: {contrast}</label>
                <input
                    type="range"
                    min="0"
                    max="10"
                    value={contrast}
                    onChange={(e) => setContrast(e.target.value)}
                    style={{ width: '100%' }}
                />
            </div>

            <div>
                <label>Saturation: {saturation}</label>
                <input
                    type="range"
                    min="0"
                    max="200"
                    value={saturation}
                    onChange={(e) => setSaturation(e.target.value)}
                    style={{ width: '100%' }}
                />
            </div>

            <div>
                <label>Sharpness: {sharpness}</label>
                <input
                    type="range"
                    min="0"
                    max="50"
                    value={sharpness}
                    onChange={(e) => setSharpness(e.target.value)}
                    style={{ width: '100%' }}
                />
            </div>

            <div>
                <label>Framerate: {framerate}</label>
                <input
                    type="range"
                    min="10"
                    max="30"
                    value={framerate}
                    onChange={(e) => setFramerate(e.target.value)}
                    style={{ width: '100%' }}
                />
            </div>

            <button onClick={handleSubmit}>Apply Settings</button>
        </div>
    );
};

export default CameraSettings;
