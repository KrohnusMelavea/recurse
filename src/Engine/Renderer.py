from .Model import Model
from .Entity import Entity
from .EntityGroup import EntityGroup
from .Texture import Texture
from .Camera import Camera
from .Shader import Shader
from .ShaderPack import ShaderPack
from uuid import UUID
from OpenGL.GL import (
 glGenVertexArrays,
 glBindVertexArray,
 glEnableClientState,
 GL_VERTEX_ARRAY,
 glUseProgram,
 glLinkProgram,
 glValidateProgram
)

class Renderer:
 models: list[Model]
 entities: list[Entity]
 textures: list[Texture]
 camera: Camera
 shaders: list[Shader]
 shader_packs: list[ShaderPack]
 
 def __init__(this, models: list[Model], entities: list[Entity], textures: list[Texture], camera: Camera, shaders: list[Shader], shader_packs: list[ShaderPack]):
  this.models = models
  this.entities = entities
  this.textures = textures
  this.camera = camera
  this.shaders = shaders
  this.shader_packs = shader_packs
  
  this.vao = glGenVertexArrays(1)
  glBindVertexArray(this.vao)
  glEnableClientState(GL_VERTEX_ARRAY)
  
  this.fetch_shaders()
  this.compile_shaders()
  shader_pack = this.get_shader_pack_by_id(UUID(hex="bd83d9aa-7fee-4dd7-967b-736deead8da4"))
  shader_pack_binary_handles = this.get_shader_pack_binary_handles(shader_pack)
  shader_pack.compile(shader_pack_binary_handles)
  
  glLinkProgram(shader_pack.shader_program)
  glUseProgram(shader_pack.shader_program)
  
 def draw(this):
  entity_groups = this.group_entities()
 
 def group_entities(this) -> dict[EntityGroup, list[UUID]]:
  entity_groups: dict[EntityGroup, list[UUID]] = dict()
  for entity in this.entities:
   entity_group = EntityGroup(entity.model_id, entity.texture_id)
   if entity_group in entity_groups.keys():
    entity_groups[entity_group].append(entity.id)
   else:
    entity_groups[entity_group] = [entity.id]
    
  return entity_groups
  
 def fetch_shaders(this) -> int:
  return sum(shader.fetch() for shader in this.shaders)
 
 def compile_shaders(this) -> int:
  return sum(shader.compile() for shader in this.shaders)
 
 def get_shader_pack_by_id(this, id: UUID) -> ShaderPack:
  return next(shader_pack for shader_pack in this.shader_packs if shader_pack.id == id)
 
 def get_shader_pack_binary_handles(this, shader_pack: ShaderPack) -> list[int]:
  return [shader.binary_handle for shader in this.shaders if shader.id in shader_pack.shader_ids]
