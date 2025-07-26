from uuid import UUID
from .util import parse_nullable_guid
from .Transformation import Transformation

class Entity: pass
class Entity:
 id: UUID
 model_id: UUID
 texture_id: UUID
 transformation: Transformation
 
 def __init__(this, id: UUID, model_id: UUID, texture_id: UUID, transformation: Transformation):
  this.id = id
  this.model_id = model_id
  this.texture_id = texture_id
  this.transformation = transformation
 
 def from_dict(entity: dict[str, str|dict[str, float]]) -> Entity:
  return Entity(
   id=UUID(hex=entity["id"]),
   model_id=parse_nullable_guid(entity["model_id"]),
   texture_id=parse_nullable_guid(entity["texture_id"]),
   transformation=Transformation.from_dict(entity["transformation"])
  )