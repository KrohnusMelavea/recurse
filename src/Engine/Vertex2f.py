class Vertex2f: pass
class Vertex2f:
 x: float
 y: float
 
 def __init__(this, x: float, y: float):
  this.x = x
  this.y = y
  
 def serialise(this) -> list[float]:
  return [this.x, this.y]

 def deserialise(vertex: list[float]) -> Vertex2f:
  return Vertex2f(
   x=vertex[0],
   y=vertex[1]
  )
 
 def from_dict(vertex: dict[str, float]) -> Vertex2f:
  return Vertex2f(
   x=vertex["x"],
   y=vertex["y"]
  ) if vertex is not None else None
  
 def from_dicts(vertices: list[dict[str, float]]) -> list[Vertex2f]:
  return [Vertex2f.from_dict(vertex) for vertex in vertices] if vertices is not None else None