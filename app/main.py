"""This is the main module for the pathmap application.
It loads configuration and defines the ASGI app for the uvicorn
server. There is currently a single path operation, /heatmap-24h."""

import os, json

from fastapi import FastAPI
from fastapi.responses import FileResponse

from app.detection_class import Detection
from app.util import normalize_camera_config
from app.frigate_client import fetch_events, extract_detections
from app.heatmap import overlay_heatmap

FRIGATE_URL = os.getenv('FRIGATE_URL')

with open('config/cameras.json') as f:
    camera_config = json.load(f)
normalized = normalize_camera_config(camera_config)
Detection.compute_homographies(normalized)

app = FastAPI()

@app.get('/heatmap-24h')
def get_24h_heatmap():
    """The path operation for creating and returning a visual
    heatmap of camera events from the previous 24 hours.
    """
    events = fetch_events(FRIGATE_URL)
    detections = extract_detections(events)
    map_points = [d.map_point() for d in detections]
    overlay_heatmap(image_path='config/map.png',
                    points=map_points,
                    out_path='map_output/heatmap-24h.png',
                    sigma_px=10,
                    alpha_max=0.8,
                    cmap_name='jet',
                    gamma=0.35)
    return FileResponse('map_output/heatmap-24h.png')