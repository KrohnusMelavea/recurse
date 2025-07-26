import json
import time
from src.Engine import Renderer, Model, Entity, Texture, Camera
import src.Engine.util as util

def main():
 start_time = time.time()
 
 models_raw = util.read_file("res/models.json")
 entities_raw = util.read_file("res/entities.json")
 textures_raw = util.read_file("res/textures.json")
 player_state_raw = util.read_file("state/player.json")
 
 models_data = json.loads(models_raw)
 entities_data = json.loads(entities_raw)
 textures_data = json.loads(textures_raw)
 player_state_data = json.loads(player_state_raw)
 camera_data = player_state_data["camera"]
 
 models = [Model.from_dict(model) for model in models_data]
 entities = [Entity.from_dict(entity) for entity in entities_data]
 textures = [Texture.from_dict(texture) for texture in textures_data] 
 camera = Camera.from_dict(camera_data)
 
 renderer = Renderer(
  models,
  entities,
  textures,
  camera
 )
 end_time = time.time()
 
 print(end_time - start_time)
 
if __name__ == "__main__":
 main()