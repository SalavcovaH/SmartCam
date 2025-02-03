import cv2
from pydantic import BaseModel
from enum import Enum
from typing import Optional


# Define Enum for camera formats
class CameraFormat(str, Enum):
    MJPG = "MJPG"


# Define Enum for camera resolution
class CameraResolution(str, Enum):
    FHD = "1920x1080"
    HD = "1280x720"
    VGA = "640x480"


class CameraParams(BaseModel):
    format: CameraFormat
    resolution: CameraResolution
    saturation: int
    sharpness: int
    framerate: int
    contrast: int
    brightness: int


class CameraManager:
    def __init__(self):
        self.cap: Optional[cv2.VideoCapture] = None
        self.params = CameraParams(
            format="MJPG",
            resolution="1280x720",
            saturation=100,
            sharpness=25,
            framerate=30,
            contrast=5,
            brightness=200
        )
    
    def set_params(self, params: CameraParams):
        """ Update the camera parameters and restart the stream if needed. """
        self.params = params
        if self.cap is not None:
            self.restart_stream()

    def restart_stream(self):
        """ Restart the camera stream with the updated parameters. """
        if self.cap:
            self.cap.release()

        # Reinitialize the video capture with the new parameters
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            print("Error: Could not open webcam")
            return

        self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
        self.set_capture_params()

    def set_capture_params(self):
        """ Apply the camera parameters to the capture object. """
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, int(self.params.resolution.split("x")[0]))
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, int(self.params.resolution.split("x")[1]))
        self.cap.set(cv2.CAP_PROP_SATURATION, self.params.saturation)
        self.cap.set(cv2.CAP_PROP_SHARPNESS, self.params.sharpness)
        self.cap.set(cv2.CAP_PROP_FPS, self.params.framerate)
        self.cap.set(cv2.CAP_PROP_BRIGHTNESS, self.params.brightness)
        self.cap.set(cv2.CAP_PROP_CONTRAST, self.params.contrast)

    def get_frame(self):
        """ Capture a single frame from the camera and return it as base64. """
        if self.cap is None:
            return None

        ret, frame = self.cap.read()
        if not ret:
            print("Error: Could not read frame from webcam")
            return None

        _, buffer = cv2.imencode(".jpg", frame)
        return buffer.tobytes()

    def release(self):
        """ Release the camera capture object. """
        if self.cap:
            self.cap.release()
