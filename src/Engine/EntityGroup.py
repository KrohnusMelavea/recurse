from .Entity import Entity
from uuid import UUID

class EntityGroup: pass
class EntityGroup:
 model_id: UUID
 texture_id: UUID
 
 def __init__(this, model_id: UUID, texture_id: UUID):
  this.model_id = model_id
  this.texture_id = texture_id
  
 def __eq__(this, other: EntityGroup) -> bool:
  return this.model_id == other.model_id and this.texture_id == other.texture_id
 
 def __hash__(this) -> int:
  return hash((this.model_id, this.texture_id))
  
 def __repr__(this) -> str:
  return f"EntityGroup(model_id={this.model_id},texture_id={this.texture_id})"