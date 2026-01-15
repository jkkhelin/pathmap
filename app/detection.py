import app.homography as hg

class Detection:
    homographies = {}

    @classmethod
    def compute_homographies(cls, camera_config: dict):
        Detection.homographies = {camera: hg.estimate_homography(
            data['video_points'], data['map_points'])
            for camera, data in camera_config.items()}

    def __init__(self, camera, video_point):
        self.camera = camera
        self.video_point = video_point

    def map_point(self) -> tuple:
        return hg.apply_homography(Detection.homographies[self.camera],
                                *self.video_point)