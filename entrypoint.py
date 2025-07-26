import json
import time
from src.Engine import Renderer, Model, Entity, Texture, Camera, Shader, ShaderPack, WindowHandler
import src.Engine.util as util
import os
import uuid
import pygame

def main():
 start_time = time.time()
 
 window_handler = WindowHandler(800, 600, "Recursor")
 
 models_raw = util.read_file("res/models.json")
 entities_raw = util.read_file("res/entities.json")
 textures_raw = util.read_file("res/textures.json")
 player_state_raw = util.read_file("state/player.json")
 shaders_raw = util.read_file("res/sha/shaders.json")
 shader_packs_raw = util.read_file("res/sha/shader_packs.json")
 
 models_data = json.loads(models_raw)
 entities_data = json.loads(entities_raw)
 textures_data = json.loads(textures_raw)
 player_state_data = json.loads(player_state_raw)
 camera_data = player_state_data["camera"]
 shaders_data = json.loads(shaders_raw)
 shader_packs_data = json.loads(shader_packs_raw)
 
 models = [Model.from_dict(model) for model in models_data]
 entities = [Entity.from_dict(entity) for entity in entities_data]
 textures = [Texture.from_dict(texture) for texture in textures_data] 
 camera = Camera.from_dict(camera_data)
 shaders = Shader.from_dicts(shaders_data)
 shader_packs = ShaderPack.from_dicts(shader_packs_data)
 
 renderer = Renderer(
  models,
  entities,
  textures,
  camera,
  shaders,
  shader_packs
 )
 renderer.fetch_shaders()
 renderer.compile_shaders()
 
 end_time = time.time()
 
 WindowHandler.close()
 
 print(end_time - start_time)
 
if __name__ == "__main__":
 main()