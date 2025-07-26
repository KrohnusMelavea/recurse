from uuid import UUID

class Texture: pass
class Texture:
 id: UUID
 path: str

 def __init__(this, id: UUID, path: str):
  this.id = id
  this.path = path
 
 def from_dict(texture: dict[str, UUID|str]) -> Texture:
  return Texture(
   id=UUID(hex=texture["id"]),
   path=texture["path"]
  )