class Vertex4f: pass
class Vertex4f:
 x: float
 y: float
 z: float
 w: float
 
 def __init__(this, x: float, y: float, z: float, w: float):
  this.x = x
  this.y = y
  this.z = z
  this.w = w
  
 def serialise(this) -> list[float]:
  return [this.x, this.y, this.z, this.w]

 def deserialise(vertex: list[float]) -> Vertex4f:
  return Vertex4f(
   x=vertex[0],
   y=vertex[1],
   z=vertex[2],
   w=vertex[3]
  )
  
 def from_dict(vertex: dict[str, float]) -> Vertex4f:
  return Vertex4f(
   x=vertex["x"],
   y=vertex["y"],
   z=vertex["z"],
   w=vertex["w"]
  ) if vertex is not None else None
  
 def from_dicts(vertices: list[dict[str, float]]) -> list[Vertex4f]:
  return [Vertex4f.from_dict(vertex) for vertex in vertices] if vertices is not None else None