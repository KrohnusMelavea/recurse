from .util import read_file
from OpenGL.GL import (
 shaders,
 GL_VERTEX_SHADER,
 GL_FRAGMENT_SHADER,
)
from enum import Enum
from uuid import UUID

class Shader: pass
class Shader:
 ShaderType = Enum(
  'Type',
  [
   ('Invalid', 0),
   ('Vertex', GL_VERTEX_SHADER),
   ('Fragment', GL_FRAGMENT_SHADER)
  ]
 )

 id: str
 path: str
 type: ShaderType
 source: str
 binary_handle: int
 
 def __init__(this, id: UUID, path: str):
  this.id = id
  this.path = path
  this.type = Shader.get_shader_type_from_path(path)
  this.source = ""
  this.binary_handle = None
 
 def fetch(this) -> bool:
  source = read_file(this.path)
  if source != this.source:
   this.source = source
   return True
  else:
   return False
 
 def compile(this) -> bool:
  try:
   this.binary_handle = shaders.compileShader(
    this.source,
    this.type.value
   )
   return True
  except RuntimeError as exception:
   print(exception)
   return False
  
 def get_shader_type_from_path(path: str) -> ShaderType:
  if path.endswith(".frg"):
   return Shader.ShaderType.Fragment
  elif path.endswith(".vrt"):
   return Shader.ShaderType.Vertex
  else:
   return Shader.ShaderType.Invalid
 
 def from_dict(shader: list[dict[str, str]]) -> Shader:
  return Shader(
   id=UUID(hex=shader["id"]),
   path=shader["path"]
  )