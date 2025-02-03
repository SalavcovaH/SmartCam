from fastapi import FastAPI, WebSocket
from camera_manager import CameraManager, CameraParams
from websocket_manager import WebSocketManager

app = FastAPI()

# Initialize the Camera Manager and WebSocket Manager
camera_manager = CameraManager()
websocket_manager = WebSocketManager(camera_manager)


@app.post("/set-camera-parameters")
async def set_camera_parameters(camera_params: CameraParams):
    """ Update the camera parameters. This will reset the camera stream. """
    camera_manager.set_params(camera_params)
    return {"message": "Camera parameters set successfully", "data": camera_params}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """ WebSocket endpoint to start streaming the webcam frames. """
    await websocket_manager.start_stream(websocket)


@app.post("/start-video-stream")
async def start_video_stream():
    """ Start the video stream """
    camera_manager.restart_stream()
    return {"message": "Video stream started"}


@app.post("/stop-video-stream")
async def stop_video_stream():
    """ Stop the video stream """
    await websocket_manager.stop_stream()
    return {"message": "Video stream stopped"}


"""
import cv2
import os
import asyncio
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import base64
from pydantic import BaseModel, conint, confloat
from enum import Enum
from typing import Literal

# Define Enum for camera formats
class CameraFormat(str, Enum):
    MJPG = "MJPG"

# Define Enum for camera resolution
class CameraResolution(str, Enum):
    FHD = "1920x1080"
    HD = "1280x720"
    VGA = "640x480"

# Camera parameter model
class CameraParams(BaseModel):
    format: CameraFormat
    resolution: CameraResolution
    saturation: conint(ge=0, le=200)
    sharpness: conint(ge=0, le=50)
    framerate: Literal[10,15,20,30]
    contrast: conint(ge=0, le=10)
    brightness: conint(ge=30, le=255)


app = FastAPI()

save = False
changed_param = False
parametres = CameraParams(
    format="MJPG", 
    resolution="1280x720",
    saturation=100,
    sharpness=25,
    framerate=30,
    contrast=5,
    brightness=200
)

output_dir = "app/output"
name = "test1"

# Allow CORS for all origins (adjust for security in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allows all origins, or specify specific origins like ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

def set_parameters(cap, cam_parametres):
    # Set camera parameters (e.g., frame width, frame height, etc.)
    if cap is not None:
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, int(cam_parametres.resolution.split("x")[0]))
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, int(cam_parametres.resolution.split("x")[1]))
        cap.set(cv2.CAP_PROP_SATURATION, cam_parametres.saturation)
        cap.set(cv2.CAP_PROP_SHARPNESS, cam_parametres.sharpness)
        cap.set(cv2.CAP_PROP_FPS, cam_parametres.framerate)
        cap.set(cv2.CAP_PROP_BRIGHTNESS, cam_parametres.brightness)
        cap.set(cv2.CAP_PROP_CONTRAST, cam_parametres.contrast)
        print("Camera parameters set.")


# Route to set camera parameters
@app.post("/set-camera-parameters")
async def set_camera_parameters(camera_params: CameraParams):
    # You can use camera_params to configure the actual camera hardware here.
    # For now, let's just simulate setting the parameters by printing them.
    print(f"Setting camera parameters: {camera_params}")
    global changed_param
    global parametres
    parametres = camera_params
    changed_param = True
    
    # Return a success message (you can add more logic here to apply the settings)
    return {"message": "Camera parameters set successfully", "data": camera_params}


# Testing message
@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI"}

# Test function for saving image - not working
@app.get("/save-image")
async def save_image():
    print("clicked")
    global save
    save = True
    return {"message": "Clicked"}

# Opens websocket for streaming webcam image
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open webcam")
        await websocket.close()
        return
    
    # Set MJPG format and default
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
    set_parameters(cap, parametres)
    print("setting default")

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error: Could not read frame from webcam")
                break


            # Convert frame to JPEG
            _, buffer = cv2.imencode(".jpg", frame)
            jpg_as_text = base64.b64encode(buffer).decode("utf-8")
            
            # Send base64 encoded frame over WebSocket
            await websocket.send_text(jpg_as_text)

            # Allow FastAPI to handle other requests (e.g., GET /message)
            await asyncio.sleep(0.01)  # Small sleep to yield control and allow other tasks
            
            # Save image
            global save
            if save:
                os.makedirs(output_dir, exist_ok=True)
                cv2.imwrite(f"{output_dir}/{name}.jpg", frame)
                save = False
                print("Image saved!")

            global changed_param
            if changed_param:
                set_camera_parameters(cap, parametres)
                changed_param = False
                print("Changed parametres")


    except Exception as e:
        print(f"WebSocket Error: {e}")
    finally:
        cap.release()
        await websocket.close()
"""
