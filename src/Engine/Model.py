from .Vertex2f import Vertex2f
from .Vertex3f import Vertex3f
from OpenGL.arrays.vbo import VBO
from uuid import UUID
from numpy import ndarray, array, float32, uint32
from enum import Enum

class Model: pass
class Model:
 ModelType = Enum(
  "ModelType",
  [
   ("InvalidEnum", 0),
   ("Indexed", 1),
   ("NonIndexed", 2),
   ("IndexCompressed", 3),
   ("IndexedTextured", 4),
   ("NonIndexedTextured", 5),
   ("IndexCompressedTextured", 6)
  ]
 )
 
 id: UUID
 type: ModelType
 vertices: list[Vertex3f]
 indices: list[list[int]]
 texture_coordinates = list[Vertex2f]
 
 vertex_buffer: ndarray
 index_buffer: ndarray
 
 vertex_buffer_object: VBO
 index_buffer_object: VBO
 
 def __init__(this, id: UUID, type: ModelType, vertices: list[Vertex3f], indices: list[list[int]], texture_coordinates: list[Vertex2f]):
  this.id = id
  this.type = type
  this.vertices = vertices
  this.indices = indices
  this.texture_coordinates = texture_coordinates
  
 def bind_buffers(this):
  this.bind_vertex_buffer()
  this.bind_index_buffer()
  
 def unbind_buffers(this):
  this.unbind_vertex_buffer()
  this.unbind_index_buffer()
 
 def bind_vertex_buffer(this):
  this.vertex_buffer_object.bind()
  
 def bind_index_buffer(this):
  if this.should_bind_index_buffer():
   this.index_buffer_object.bind()
   
 def unbind_vertex_buffer(this):
  this.vertex_buffer_object.unbind()
 
 def unbind_index_buffer(this):
  if this.should_bind_index_buffer():
   this.index_buffer_object.unbind()
 
 def should_bind_index_buffer(this) -> bool:
  return this.type == Model.ModelType.Indexed or this.type == Model.ModelType.IndexedTextured
 
 def generate_buffers(this):
  this.generate_cpu_buffers()
  this.generate_gpu_buffers()
 
 def generate_vertex_buffers(this):
  this.generate_cpu_vertex_buffer()
  this.generate_gpu_vertex_buffer()
  
 def generate_index_buffers(this):
  this.generate_cpu_index_buffer()
  this.generate_gpu_index_buffer()
 
 def generate_cpu_buffers(this):
  this.generate_cpu_vertex_buffer()
  this.generate_cpu_index_buffer()
  
 def generate_cpu_vertex_buffer(this):
  print(this.type)
  match this.type:
   case Model.ModelType.Indexed:
    this.vertex_buffer = array(this.flatten_vertices(), dtype=float32)
   case Model.ModelType.NonIndexed:
    this.vertex_buffer = array(this.flatten_vertices(), dtype=float32)
   case Model.ModelType.IndexCompressed:
    this.vertex_buffer = array(this.flatten_compressed_vertices(), dtype=float32)
   case Model.ModelType.IndexedTextured:
    this.vertex_buffer = array(this.flatten_vertices_and_texture_coordinates(), dtype=float32)
   case Model.ModelType.NonIndexedTextured:
    this.vertex_buffer = array(this.flatten_vertices(), dtype=float32)
   case Model.ModelType.IndexCompressedTextured:
    this.vertex_buffer = array(this.flatten_compressed_vertices_and_texture_coordinates(), dtype=float32)
   
 def flatten_vertices(this) -> list[float]:
  return [
   entry 
   for vertex in this.vertices 
   for entry in vertex.serialise()
  ]
 
 def flatten_compressed_vertices(this) -> list[float]:
  return [
   entry
   for indices in this.indices
   for index in indices
   for entry in this.vertices[index].serialise()
  ]
 
 def flatten_vertices_and_texture_coordinates(this) -> list[float]:
  return [
   entry
   for vertex, texture_coordinates in zip(this.vertices, this.texture_coordinates)
   for entry in vertex.serialise() + texture_coordinates.serialise()
  ]
 
 def flatten_compressed_vertices_and_texture_coordinates(this) -> list[float]:
  return [
   entry
   for indices in this.indices
   for index in indices
   for entry in this.vertices[index].serialise() + this.texture_coordinates[index].serialise()
  ]
 
 def generate_cpu_index_buffer(this):
  match this.type:
   case Model.ModelType.Indexed:
    this.index_buffer = array(this.flatten_indices(), dtype=uint32)
   case Model.ModelType.IndexedTextured:
    this.index_buffer = array(this.flatten_indices(), dtype=uint32)
   case Model.ModelType.IndexCompressedTextured:
    this.index_buffer = array(this.flatten_indices(), dtype=uint32)
    
 def flatten_indices(this) -> list[int]:
  return [
   index
   for indices in this.indices
   for index in indices
  ]
 
 def generate_gpu_buffers(this):
  this.generate_gpu_vertex_buffer()
  if this.indices is not None:
   this.generate_gpu_index_buffer()
 
 def generate_gpu_vertex_buffer(this):
  this.vertex_buffer_object = VBO(
   data=this.vertex_buffer,
   usage="GL_STATIC_DRAW",
   target="GL_ARRAY_BUFFER",
   size=this.vertex_buffer.nbytes
  )
 
 def generate_gpu_index_buffer(this):
  this.index_buffer_object = VBO(
   data=this.index_buffer,
   usage="GL_STATIC_DRAW",
   target="GL_ELEMENT_ARRAY_BUFFER",
   size=this.index_buffer.nbytes
  )
  
 def string_to_type_enum(enum: str) -> ModelType:
  match enum:
   case "Indexed":
    return Model.ModelType.Indexed
   case "NonIndexed":
    return Model.ModelType.NonIndexed
   case "IndexedTextured":
    return Model.ModelType.IndexedTextured
   case "NonIndexedTextures":
    return Model.ModelType.NonIndexedTextured
   case "IndexCompressedTextured":
    return Model.ModelType.IndexCompressedTextured
  return Model.ModelType.InvalidEnum
  
 def from_dict(model: dict[str, str | list[dict[str, float], list[int]]]) -> Model:
  return Model(
   id=UUID(hex=model["id"]),
   type=Model.string_to_type_enum(model["type"]),
   vertices=Vertex3f.from_dicts(model["vertices"]),
   indices=model["indices"],
   texture_coordinates=Vertex2f.from_dicts(model["texture_coordinates"])
  )