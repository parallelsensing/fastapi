

def get_obj_from_list(arr: list, id: int) -> dict|None:
  for i in range(0, len(arr)):
    if arr[i].id == id:
      return arr[i]
  return None