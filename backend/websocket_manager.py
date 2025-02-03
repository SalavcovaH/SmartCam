import base64
from fastapi import WebSocket
from camera_manager import CameraManager
import asyncio


class WebSocketManager:
    def __init__(self, camera_manager: CameraManager):
        self.camera_manager = camera_manager
        self.websocket: WebSocket = None

    async def start_stream(self, websocket: WebSocket):
        """ Start streaming frames to the WebSocket client. """
        self.websocket = websocket
        await websocket.accept()

        try:
            while True:
                frame_data = self.camera_manager.get_frame()
                if frame_data:
                    await self.websocket.send_text(base64.b64encode(frame_data).decode('utf-8'))
                await asyncio.sleep(0.01)  # Allow other tasks to run
        except Exception as e:
            print(f"WebSocket error: {e}")
        finally:
            await self.stop_stream()

    async def stop_stream(self):
        """ Close the WebSocket connection and release the camera capture. """
        if self.websocket:
            await self.websocket.close()
        self.camera_manager.release()
