import json
from kazoo.client import KazooClient
from kazoo.recipe.lock import Lock
from ..config import Config

class ZookeeperCounter:
  __GET_COUNTER = "/counter"
  __GET_SERVER_NUMBER = "1"

  def __init__(self):
    self.connection = KazooClient(
        hosts=f"{Config.ZOOKEEPER_HOST}:{Config.ZOOKEEPER_PORT}",
      )
    print("Zookeeper connected successfully")
    self.connection.start()
    print("Zookeeper started successfully")
    self.connection.ensure_path("/servers")
    self.path = f"/servers/server-{self.__GET_SERVER_NUMBER}"
    self.create_new_range_server()
  

  
  def get_number_from_counter(self):
    """
      Used to get value from '/counter'.
      '/counter' is to know new range when creating a new server
    """
    try:
      counter_object = self.connection.get(self.__GET_COUNTER)
      if counter_object:
        counter, _ = counter_object
        counter = int(counter.decode())
        self.connection.set(self.__GET_COUNTER, str(counter + 1).encode("utf-8"))
      return counter
    except Exception as error:
      print("func get_number_from_counter:", error)

  def create_new_range_server(self):
    try:
      lock = Lock(self.connection, f"{self.__GET_COUNTER}")
      with lock:
        start_range = self.get_number_from_counter()
        if not start_range: 
          raise Exception("Unable to find counter")

        end_range = ((start_range + Config.ZOOKEEPER_RANGE_GAP) // Config.ZOOKEEPER_RANGE_GAP) * Config.ZOOKEEPER_RANGE_GAP
        start_range += 1

        counter = self.connection.get(self.__GET_COUNTER)
        counter = str(start_range + Config.ZOOKEEPER_RANGE_GAP)
        self.connection.set(self.__GET_COUNTER, counter.encode("utf-8"))
        
        if not self.connection.exists(self.path):
          self.connection.create(self.path, json.dumps({
            "start": str(start_range),
            "end": str(end_range)
          }).encode("utf-8"))

        print(f"Zookeeper server range created successfully: {self.path}")
    except Exception as error: 
      print("func create_new_range_server:", error)

    
  def update_range_server(self, new_start, end):
    try: 
      lock_range = Lock(self.connection, self.path)
      with lock_range: 
        range_object = {"start": str(new_start), "end": str(end)}
        self.connection.set(self.path, json.dumps(range_object).encode("utf-8"))

    except Exception as error:
      print("func update_range_server:", error)


  def get_number_from_range(self):
    try:
      lock_range = Lock(self.connection, self.path)
      new_start = None
      with lock_range:
        range_tuple = self.connection.get(self.path)

        if range_tuple == None:
          raise Exception("Unable to find range")
        range, _ = range_tuple
        decoded_range = range.decode("utf-8")
        range_object = json.loads(decoded_range)

        start = range_object["start"]
        new_start = int(start) + 1
        end = range_object["end"]
        print(range_object, start, end)

      if new_start == end:
        self.create_new_range_server()
      else:
        self.update_range_server(new_start, end)

      return new_start

    except Exception as error:
      print("func get_number_from_range:", error)


counter = ZookeeperCounter()