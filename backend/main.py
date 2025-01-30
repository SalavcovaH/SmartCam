import cv2
import os
import asyncio
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import base64

app = FastAPI()

# Allow CORS for all origins (adjust for security in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allows all origins, or specify specific origins like ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

# Testing message
@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI"}

# Test function for saving image - not working
@app.get("/save-image")
async def save_image():
    print("clicked")
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open webcam")
        return {"message": "Error"}
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

    except Exception as e:
        print(f"WebSocket Error: {e}")
    finally:
        cap.release()
        await websocket.close()

