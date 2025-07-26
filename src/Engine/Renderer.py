from .Model import Model
from .Entity import Entity
from .Texture import Texture
from .Camera import Camera

class Renderer:
 models: list[Model]
 entities: list[Entity]
 textures: list[Texture]
 camera: Camera
 
 def __init__(this, models: list[Model], entities: list[Entity], textures: list[Texture], camera: Camera):
  this.models = models
  this.entities = entities
  this.textures = textures
  this.camera = camera