class Vertex3f: pass
class Vertex3f:
 x: float
 y: float
 z: float
 
 def __init__(this, x: float, y: float, z: float):
  this.x = x
  this.y = y
  this.z = z
  
 def from_dict(vertex: dict[str, float]) -> Vertex3f:
  return Vertex3f(
   x=vertex["x"],
   y=vertex["y"],
   z=vertex["z"]
  ) if vertex is not None else None
  
 def from_dicts(vertices: list[dict[str, float]]) -> list[Vertex3f]:
  return [Vertex3f.from_dict(vertex) for vertex in vertices] if vertices is not None else None