from .Model import Model
from .Entity import Entity
from .Texture import Texture
from .Camera import Camera
from .Shader import Shader

class Renderer:
 models: list[Model]
 entities: list[Entity]
 textures: list[Texture]
 camera: Camera
 shaders: list[Shader]
 
 def __init__(this, models: list[Model], entities: list[Entity], textures: list[Texture], camera: Camera, shaders: list[Shader]):
  this.models = models
  this.entities = entities
  this.textures = textures
  this.camera = camera
  this.shaders = shaders