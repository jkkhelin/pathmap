import numpy as np

from app.detection import Detection
from app.util import normalize_camera_config

def test_compute_homographies_output_format():
    camera_config = {
        'A': {
            'video_points': [[0, 0], [1, 0], [1, 1], [0, 1]],
            'map_points': [[0, 0], [2, 0], [0.5, 1.5], [0.4, -0.2]],
            'video_width': 500,
            'video_height': 500
        },
        'B': {
            'video_points': [[0, 0], [1, 0], [1, 1], [0, 1]],
            'map_points': [[0, 0], [2, 0], [0.5, 1.5], [0.4, -0.2]],
            'video_width': 500,
            'video_height': 500
        }
    }
    normalized_config = normalize_camera_config(camera_config)

    Detection.compute_homographies(normalized_config)
    
    assert isinstance(Detection.homographies, dict)
    assert len(Detection.homographies) == 2
    assert isinstance(Detection.homographies['A'], np.ndarray)