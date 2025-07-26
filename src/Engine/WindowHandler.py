import pygame

class WindowHandler:
 width: int
 height: int
 title: str
 window_handle = pygame.Surface
 
 def __init__(this, width: int, height: int, title: str):
  pygame.init()
  
  this.width = width
  this.height = height
  this.title = title
  this.window_handle = pygame.display.set_mode((width, height), pygame.OPENGL | pygame.DOUBLEBUF)
  
 def close():
  pygame.display.quit()
  pygame.quit()
  