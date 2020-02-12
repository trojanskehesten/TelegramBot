import sqlite3

class DBHelper:

  def __init__(self, dbname="todo.sqlite"):
    # connect to database
    self.__conn = sqlite3.connect(dbname)
    self.__setup()

  def __setup(self):
    # create table
    tblstmt = "CREATE TABLE IF NOT EXISTS items (chat_id bigint not null, audio_id bigint, photo_id bigint)"
    itemidx = "CREATE INDEX IF NOT EXISTS itemIndex ON items (chat_id ASC)"         
    self.__conn.execute(tblstmt)
    self.__conn.execute(itemidx)
    self.__conn.commit()

  def __exec(self, query, args=None):
    if args == None:
      res = self.__conn.execute(query)
    else:
      res = self.__conn.execute(query, args)
    self.__conn.commit()
    return res

  def __get_the_only_one_item(self, request):
    # get the only one item from table with the only one item
    res =  [x[0] for x in request]
    return res[0]

  def __get_max_object_id(self, object_type):
    # get max id of photo or audio from database
    # object_type = 'audio' or 'photo'
    if object_type not in ('audio', 'photo'):
      return None
    query = 'SELECT MAX({}_id) FROM items'.format(object_type)
    resp = self.__exec(query)
    for max_object_id in resp:
      max_object_id
    max_object_id = max_object_id[0]
    #max_object_id = self.__get_the_only_one_item(resp)
    if max_object_id == None or max_object_id == 'Null':
      return 0
    return max_object_id      

  def __add_object_id(self, chat_id, max_uid, object_type):
    # add id of photo or audio to database
    # object_type = 'audio' or 'photo'
    if object_type not in ('audio', 'photo'):
      return None
    query = "INSERT INTO items (chat_id, audio_id, photo_id) VALUES (?, ?, ?)"
    id_object = max_uid + 1
    if object_type == 'photo':
      args = (chat_id, None, id_object)
    elif object_type == 'audio':
      args = (chat_id, id_object, None)
    self.__exec(query, args)
    return True

  def __get_id_last_added_object(self, chat_id, object_type):
    # max id from database for chat_id
    # object_type = 'audio' or 'photo'
    if object_type not in ('audio', 'photo'):
      return None
    query = "SELECT MAX({}_id) FROM items WHERE chat_id = (?)".format(object_type)
    args = (chat_id, )
    resp = self.__exec(query, args)
    id_last_added_object = self.__get_the_only_one_item(resp)
    return id_last_added_object

  def add_photo_id(self, chat_id, max_uid):
      return self.__add_object_id(chat_id, max_uid, 'photo')
  def add_audio_id(self, chat_id, max_uid):
      return self.__add_object_id(chat_id, max_uid, 'audio')

  def get_max_photo_id(self):
    return self.__get_max_object_id('photo')
  def get_max_audio_id(self):
    return self.__get_max_object_id('audio')

  def __get_id_last_added_photo(self, chat_id):
    return self.__get_id_last_added_object(chat_id, 'photo')
  def __get_id_last_added_audio(self, chat_id):
    return self.__get_id_last_added_object(chat_id, 'audio')