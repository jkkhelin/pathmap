"""This module provides utility functions for internal use."""

def normalize_camera_config(camera_config):
    """Scale video point coordinates to 0...1 from raw cameras.json data."""
    for key, value in camera_config.items():
        value['video_points'] = [[x/value['video_width'],
                                  y/value['video_height']]
                                  for x, y in value['video_points']]
    return camera_config