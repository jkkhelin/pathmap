from app.util import normalize_camera_config

def test_normalize_camera_config_normalizes_video_points():
    camera_config = {
        'A': {
            'video_points': [[10, 10], [15, 20], [1.4, 1], [12, 41]],
            'map_points': [[0, 0], [2, 0], [0.5, 1.5], [0.4, 0.2]],
            'video_width': 500,
            'video_height': 500
        },
        'B': {
            'video_points': [[0, 0], [1, 0], [1, 1], [0, 1]],
            'map_points': [[0, 0], [2, 0], [0.5, 1.5], [0.4, 0.2]],
            'video_width': 500,
            'video_height': 500
        }
    }

    normalized_config = normalize_camera_config(camera_config)

    assert normalized_config['A']['video_points'][3][1] == 41 / 500