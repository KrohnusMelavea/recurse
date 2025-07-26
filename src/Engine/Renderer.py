from .Model import Model
from .Entity import Entity
from .Texture import Texture
from .Camera import Camera
from .Shader import Shader
from .ShaderPack import ShaderPack

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