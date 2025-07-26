from .Transformation import Transformation

class Camera: pass
class Camera:
 fov: float
 transformation: Transformation
 
 def __init__(this, fov: float, transformation: Transformation):
  this.fov = fov
  this.transformation = transformation
 
 def from_dict(camera: dict[str, dict[str, dict[str, float]] | float]) -> Camera:
  return Camera(
   fov=camera["fov"],
   transformation=Transformation.from_dict(camera["transformation"])
  ) if camera is not None else None