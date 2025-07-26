from uuid import UUID
from .Vertex3f import Vertex3f

class Model: pass
class Model:
 id: UUID
 vertices: list[Vertex3f]
 indices: list[list[int]]
 
 def __init__(this, id: UUID, vertices: list[Vertex3f], indices: list[list[int]]):
  this.vertices = vertices
  this.indices = indices
  
 def from_dict(model: dict[str, str | list[dict[str, float], list[int]]]) -> Model:
  return Model(
   id=UUID(hex=model["id"]),
   vertices=Vertex3f.from_dicts(model["vertices"]),
   indices=model["indices"]
  )