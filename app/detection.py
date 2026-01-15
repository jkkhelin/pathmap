"""This module provides the Detection class that is used to
represent a single data point (eg. pixel location) in the
object movement path provided by Frigate. It also includes
utilities for translating it into a point on the map using
precomputed homographies."""

import app.homography as hg

class Detection:
    """Represents a single detection point.
    
    Class Attributes:
        homographies: a cache of per-camera homography transformations.
    """
    homographies = {}

    @classmethod
    def compute_homographies(cls, camera_config: dict):
        """Compute and cache homographies for all configured cameras.
        
        Builds a dictionary that maps each camera name to a
        homography computed from corresponding control points
        in video and map coordinates.
        
        Args:
            camera_config (dict):
                Deserialized and normalized data from config/cameras.json.
        """
        Detection.homographies = {camera: hg.estimate_homography(
            data['video_points'], data['map_points'])
            for camera, data in camera_config.items()}

    def __init__(self, camera, video_point):
        """Initialize a detection.
        
        Args:
            camera (str): The camera name that produced this detection.
            video_point: The point in the video feed associated with
                this detection.
        """
        self.camera = camera
        self.video_point = video_point

    def map_point(self) -> tuple:
        """Map the detection's video point into the world/map
        coordinate system.
        
        Returns:
            tuple[float, float]: the point in world/map coordinates.
        """
        return hg.apply_homography(Detection.homographies[self.camera],
                                *self.video_point)