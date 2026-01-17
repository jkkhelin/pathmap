# Pathmap

Pathmap is an application for drawing paths of NVR-camera-tracked objects on a map. It uses Frigate for object detection, maps camera detections to world/map locations, and provides a heatmap visualization of recent detected movement.

![example heatmap](https://raw.githubusercontent.com/jkkhelin/pathmap/main/static/example_heatmap.png)

## Quickstart

```bash
git clone https://github.com/jkkhelin/pathmap.git
cd pathmap
```

### Config

Add map.png and cameras.json files in the config directory. The map.png is the base image on which the tracked object paths will be drawn. The cameras.json includes camera configuration required to map points from the camera's video view onto the map. A minimum of 4 pairs of points that correspond to the same physical locations in the video and map pixel spaces are required for each camera. An example configuration is available in config/cameras.example.json.

### Run

```bash
python3 -m pip install -r requirements.txt
FRIGATE_URL=YOUR_URL fastapi run app/main.py --port 8000
```

### Docker

```bash
docker build -t pathmap .
docker run -d -p 8000:8000 -e FRIGATE_URL=YOUR_URL -v $(pwd)/config:/app/config:ro,Z pathmap
```

## Try it

View person movement from the past 24 hours on your map at http://localhost:8000/heatmap-24h.

## License

Pathmap has an MIT license, found in the LICENSE file.