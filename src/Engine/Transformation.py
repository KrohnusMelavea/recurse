from .Vertex3f import Vertex3f
from .Vertex4f import Vertex4f

class Transformation: pass
class Transformation:
 translation: Vertex3f
 rotation: Vertex4f
 scale: Vertex3f
 
 def __init__(this, translation: Vertex3f, rotation: Vertex4f, scale: Vertex3f):
  this.translation = translation
  this.rotation = rotation
  this.scale = scale
 
 def from_dict(transformation: dict[str, dict[str, float]]) -> Transformation:
  return Transformation(
   translation=Vertex3f.from_dict(transformation["translation"]),
   rotation=Vertex4f.from_dict(transformation["rotation"]),
   scale=Vertex3f.from_dict(transformation["scale"])
  ) if transformation is not None else None