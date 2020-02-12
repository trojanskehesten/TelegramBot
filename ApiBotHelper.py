#import json
import requests
#import time
#import urllib

class ApiBotHelper:

  def __init__(self, token):
    self.__token = token
    self.__base_url = 'https://api.telegram.org/bot{}/'.format(token)
    self.__type_message = 'message'

  def set_type_message(self, type_message):
    self.__type_message = type_message

  def get_updates(self, offset=None, timeout=50):
    if offset != None:
      offset += 1
    url = self.__base_url + 'getUpdates'
    params = {'timeout': timeout, 'offset': offset}
    response = requests.get(url, data=params)
    js = response.json()
    return js['result']

  def get_last_update_id(self, updates):
    update_ids = []
    if updates == []:
      return None
    for update in updates:
      update_ids.append(int(update['update_id']))
    return max(update_ids)

  def send_message(self, text, chat_id):
    url = self.__base_url + 'sendMessage'
    params = {'text' : text, 'chat_id' : chat_id}
    response = requests.post(url, data=params)
    return response

  def get_is_photo(self, update):
    if 'photo' in update[self.__type_message]:
      return True
    return False
    
  def __get_is_image(self, update):
    if 'document' in update[self.__type_message]:
      if update[self.__type_message]['document']['mime_type'][:5] == 'image': # первые пять символов - image
        return True
    return False

  def get_is_voice(self, update):
    if 'voice' in update[self.__type_message]:
      return True
    return False

  def __get_is_audio(self, update):
    if 'audio' in update[self.__type_message]:
      return True
    return False

  def __get_url_file_by_id(self, file_id):
    par = {'file_id': file_id}
    file_json = requests.get(self.__base_url + 'getFile', par).json()
    url_file = 'https://api.telegram.org/file/bot{}/'.format(self.__token) + file_json['result']['file_path']
    return url_file

  def get_url_photo(self, update):
    file_id = update[self.__type_message]['photo'][2]['file_id']
    url_photo = self.__get_url_file_by_id(file_id)
    return url_photo

  def get_url_voice(self, update):
    file_id = update[self.__type_message]['voice']['file_id']
    url_voice = self.__get_url_file_by_id(file_id)
    return url_voice

  def get_chat_id(self, update):
    return update[self.__type_message]['chat']['id']

  def get_is_text(self, update):
    if 'text' in update[self.__type_message]:
      return True
    return False

  def get_text(self, update):
    return update[self.__type_message]['text']

  def get_and_set_is_message_or_edited_message(self, update):
    if 'message' in update:
      self.__type_message = 'message'
      return True
    elif 'edited_message' in update:
      self.__type_message = 'edited_message'
      return True
    return False