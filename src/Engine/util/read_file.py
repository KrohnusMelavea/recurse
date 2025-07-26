def read_file(path: str) -> str:
 with open(path, 'r') as file_handler:
  data = file_handler.read()
  return data