from .Model import Model
from .Entity import Entity
from .EntityGroup import EntityGroup
from .Texture import Texture
from .Camera import Camera
from .Shader import Shader
from .ShaderPack import ShaderPack
from OpenGL.arrays.vbo import VBO
from OpenGL.GL import (
 glGenVertexArrays,
 glBindVertexArray,
 glEnableClientState,
 GL_VERTEX_ARRAY,
 glUseProgram,
 glLinkProgram,
 glEnable,
 glCullFace,
 glFrontFace,
 glGetUniformBlockIndex,
 glGenBuffers,
 GL_DEPTH_TEST,
 GL_CULL_FACE,
 GL_FRONT,
 GL_CCW,
 glBindBufferBase,
 GL_UNIFORM_BUFFER,
 glEnableVertexAttribArray,
 glVertexAttribPointer,
 GL_FLOAT,
 GL_FALSE,
 glDrawElementsInstanced,
 glDrawArraysInstanced,
 GL_TRIANGLES,
 GL_UNSIGNED_INT,
 glClear,
 GL_COLOR_BUFFER_BIT,
 GL_DEPTH_BUFFER_BIT
)
from uuid import UUID
from numpy import array, float32
import ctypes

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
  
  for model in this.models:
   if model.type == Model.ModelType.InvalidEnum:
    continue
   model.generate_buffers()
  
  this.vao = glGenVertexArrays(1)
  glBindVertexArray(this.vao)
  glEnableClientState(GL_VERTEX_ARRAY)
  
  glEnable(GL_DEPTH_TEST)
  glEnable(GL_CULL_FACE)
  glCullFace(GL_FRONT)
  glFrontFace(GL_CCW)
  
  this.fetch_shaders()
  this.compile_shaders()
  shader_pack = this.get_shader_pack_by_id(UUID(hex="bd83d9aa-7fee-4dd7-967b-736deead8da4"))
  shader_pack_binary_handles = this.get_shader_pack_binary_handles(shader_pack)
  shader_pack.compile(shader_pack_binary_handles)
  
  this.camera_uniform_index = glGetUniformBlockIndex(shader_pack.shader_program, "UBO")
  this.camera_uniform_buffer = glGenBuffers(1)
  glBindBufferBase(GL_UNIFORM_BUFFER, this.camera_uniform_index, this.camera_uniform_buffer)
  
  glLinkProgram(shader_pack.shader_program)
  glUseProgram(shader_pack.shader_program)
  
 def draw(this):
  glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
  
  glEnableVertexAttribArray(0)
  glEnableVertexAttribArray(1)
  glEnableVertexAttribArray(2)
  glEnableVertexAttribArray(3)
  glEnableVertexAttribArray(4)
  
  entity_groups = this.group_entities()
  print(entity_groups)
  for entity_group, entity_ids in entity_groups.items():
   this.draw_entity_group(entity_group, entity_ids)
   
 def draw_entity_group(this, entity_group: EntityGroup, entity_ids: list[UUID]):
  model = this.get_model_by_id(entity_group.model_id)
  entity_instance_data = array(
   object=this.get_entities_instance_data_by_ids(entity_ids), 
   dtype=float32
  )
  entity_instance_data_vertex_buffer_object = VBO(
   data=entity_instance_data,
   usage="GL_STATIC_DRAW",
   target="GL_ARRAY_BUFFER",
   size=entity_instance_data.nbytes
  )
  
  model.bind_buffers()
  entity_instance_data_vertex_buffer_object.bind()
  
  glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 20, ctypes.c_void_p(0))
  glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 20, ctypes.c_void_p(12))
  glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, 40, ctypes.c_void_p(0))
  glVertexAttribPointer(3, 4, GL_FLOAT, GL_FALSE, 40, ctypes.c_void_p(12))
  glVertexAttribPointer(4, 3, GL_FLOAT, GL_FALSE, 40, ctypes.c_void_p(28))
  
  if model.type != Model.ModelType.IndexCompressedTextured:
   glDrawElementsInstanced(GL_TRIANGLES, (12+8)*3 + 12+16+12, GL_UNSIGNED_INT, model.index_buffer_object, len(entity_ids))
  elif model.type == Model.ModelType.IndexCompressedTextured:
   glDrawArraysInstanced(GL_TRIANGLES, 0, (12+8)*3 + 12+16+12, len(entity_ids))
 
  model.unbind_buffers()
  entity_instance_data_vertex_buffer_object.unbind()
 
 def group_entities(this) -> dict[EntityGroup, list[UUID]]:
  entity_groups: dict[EntityGroup, list[UUID]] = dict()
  for entity in this.entities:
   entity_group = EntityGroup(entity.model_id, entity.texture_id)
   if entity_group in entity_groups.keys():
    entity_groups[entity_group].append(entity.id)
   else:
    entity_groups[entity_group] = [entity.id]
    
  return entity_groups
 
 def get_model_by_id(this, id: UUID) -> Model:
  return next(model for model in this.models if model.id == id)
 
 def get_entities_by_entity_ids(this, ids: list[UUID]) -> list[Entity]:
  return [this.get_entity_by_entity_id(id) for id in ids]
 
 def get_entities_instance_data_by_ids(this, ids: list[UUID]) -> list[list[float]]:
  return [this.get_entity_by_entity_id(id).transformation.serialise() for id in ids]
 
 def get_entities_instance_data(this, entities: list[Entity]) -> list[list[float]]:
  return [entity.transformation.serialise() for entity in entities]
 
 def get_entity_by_entity_id(this, id: UUID) -> Entity:
  return next(entity for entity in this.entities if entity.id == id)
  
 def fetch_shaders(this) -> int:
  return sum(shader.fetch() for shader in this.shaders)
 
 def compile_shaders(this) -> int:
  return sum(shader.compile() for shader in this.shaders)
 
 def get_shader_pack_by_id(this, id: UUID) -> ShaderPack:
  return next(shader_pack for shader_pack in this.shader_packs if shader_pack.id == id)
 
 def get_shader_pack_binary_handles(this, shader_pack: ShaderPack) -> list[int]:
  return [shader.binary_handle for shader in this.shaders if shader.id in shader_pack.shader_ids]
