from uuid import UUID

class ShaderPack: pass
class ShaderPack:
 id: UUID
 shader_ids: list[UUID]
 
 def __init__(this, id: UUID, shader_ids: list[UUID]):
  this.id = id
  this.shader_ids = shader_ids
 
 def from_dict(shader_pack: dict[str, str | list[str]]) -> ShaderPack:
  return ShaderPack(
   id=UUID(hex=shader_pack["id"]),
   shader_ids=[UUID(hex=shader_id) for shader_id in shader_pack["shader_ids"]]
  )
 
 def from_dicts(shader_packs: list[dict[str, str | list[str]]]) -> list[ShaderPack]:
  return [ShaderPack.from_dict(shader_pack) for shader_pack in shader_packs]