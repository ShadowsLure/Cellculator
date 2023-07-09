import pymongo
import time


# Connect to your MongoDB database'
client = pymongo.MongoClient(
  "mongodb+srv://cellulator:22PyhtWYeQy3DtAk@cellculatordata.jh4moy0.mongodb.net/?retryWrites=true&w=majority")
db = client['CellCulator']
collection = db['BrainCells']
collection2 = db['ChaosEntry']

#memory

def create_user_data(user_id, random_int, int1, int2):
  # create a new document with user_id and random_int
  new_data = {
    "user_id": user_id,
    "random_int": random_int,
    "int1": int1,
    "int2": int2,
    "high": random_int,
    "low": random_int
  }
  # insert the new document into the collection
  collection.insert_one(new_data)


def get_user_data(user_id):
  return collection.find_one({'user_id': user_id}, {
    'user_id': 1,
    'random_int': 1,
    'int1': 1,
    'int2': 1
  })

def get_user_history(user_id):
  return collection.find_one({'user_id': user_id}, {
    'user_id': 1,
    'high' : 1,
    'low' : 1,
    'random_int': 1
  })


def update_user_data(user_id, random_int, int1, int2, high, low):
  collection.update_one(
    {'user_id': user_id},
    {'$set': {
      'random_int': random_int,
      'int1': int1,
      'int2': int2,
      'high': high,
      'low' : low
    }})


def time_data(user_id, curr_time):
  new_data = {"user_id": user_id, "curr_time": curr_time}
  collection.insert_one(new_data)


def time_retrieve(user_id):
  return collection.find_one({"user_id": user_id}, {
    "user_id": 1,
    "curr_time": 1
  })


def time_update(user_id, curr_time):
  collection.update_one({"user_id": user_id},
                        {"$set": {
                          "curr_time": curr_time
                        }})


def time_memory(auth_id):
  current_time = time.time()
  user_data = time_retrieve(auth_id)
  if user_data:
    last_time = user_data["curr_time"]
    time_since_last_use = current_time - last_time
    if time_since_last_use < 900:
      return False
  return True


# Alerts Server Database Management Alpha

def add_server_value_and_channel(server_id, value, channel_id:int = None, random_no = 0, message_no = 0, last_sent_time = 0):
  new_data = {
    "server_id" : server_id,
    "value" : value,
    "channel_id" : channel_id,
    "random_no" : random_no,
    "message_no" : message_no,
    "last_sent_time" : last_sent_time

  }
  collection2.insert_one(new_data)


def update_value_and_channel(server_id, value, channel_id:int = None):
  collection2.update_one(
    {'server_id' : server_id},
    {'$set' : {
      'value' : value,
      'channel_id' : channel_id
    }}
  )

def update_random_no(server_id, random_no):
  collection2.update_one(
    {'server_id':server_id},
    {'$set': {
      'random_no':random_no
    }}
  )


def update_last_time(server_id, last_sent_time):
  collection2.update_one(
    {'server_id':server_id},
    {'$set': {
      'last_sent_time':last_sent_time
    }}
  )


def update_message_no(server_id, message_no):
  collection2.update_one(
    {'server_id':server_id},
    {'$set':{
      'message_no' : message_no
    }}
  )


def retrieve_server_value_channel_random_time(server_id):
  return collection2.find_one({'server_id':server_id},
                              {'value':1,
                               'channel_id':1,
                               'random_no' :1,
                               'message_no':1,
                               'last_sent_time':1})
