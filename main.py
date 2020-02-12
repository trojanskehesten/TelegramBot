import ApiBotHelper
import DBHelper
import Audio_processing
import Image_processing
import config
import time
import json

def main():
  token = config.token
  api = ApiBotHelper.ApiBotHelper(token)
  db = DBHelper.DBHelper()
  audio = Audio_processing.Audio_processing()
  image = Image_processing.Image_processing()
  last_update_id = None
  error_uid = 0
  
  def error_sending(error, e):
    admin_chat_id = 377169456
    api.send_message('Я грохнулся, помоги! :( ({}) '.format(error), admin_chat_id)
    api.send_message(e, admin_chat_id)
 
  while True:
    updates = api.get_updates(offset=last_update_id)
    for update in updates:
      try:
        if api.get_and_set_is_message_or_edited_message(update):
          try:
            chat_id = api.get_chat_id(update)
          except Exception as e:
            error_sending('chat_id', e)
          is_added = False
          if api.get_is_photo(update):
            try:
              im_url = api.get_url_photo(update)
            except Exception as e:
              error_sending('get_url_photo', e)
            max_uid_photo = db.get_max_photo_id()
            try:
              is_added = image.save_file(im_url, max_uid_photo)
            except Exception as e:
              error_sending('im_save_file', e)
            if is_added:
              api.send_message('Photo added', chat_id)
              db.add_photo_id(chat_id, max_uid_photo)
            else:
              api.send_message("Photo without face isn't added. Please send voice or photo with face", chat_id)
          elif api.get_is_voice(update):
            try:
              voice_url = api.get_url_voice(update)
            except Exception as e:
              error_sending('get_url_voice', e)
            max_uid_voice = db.get_max_audio_id()
            try:
              audio.process_audio(voice_url, max_uid_voice)
            except Exception as e:
              error_sending('process_audio', e)
            is_added = db.add_audio_id(chat_id, max_uid_voice)
            if is_added:
              api.send_message('Voice added', chat_id)
          elif api.get_is_text(update):
            if api.get_text(update) == '/start':
              api.send_message('Hi! Send me photo with face or voice message and I will save you! :)', chat_id)
            else:
              api.send_message("I don't understand text. You can write /start .", chat_id)
          else:
            api.send_message("Object isn't added. Please send voice or photo with face", chat_id)
      except Exception as e:
        error_sending('СРОЧНО, НЕ ОБРАБОТАН UPDATE!', e)
        error_uid += 1
        is_send = False
        try:
          api.send_message("I can't recognize the message. I will check it later. Message UID = {}".format(error_uid), chat_id)
          is_send = True
        except Exception as e:
          error_sending('Я не смог отправить пользователю информацию об ошибке', e)
        filename_json = 'update-' + str(error_uid) + '_is_send-' + str(is_send) + '.json'
        with open(filename_json, 'w') as f:
          json.dump(update, f)

    last_update_id = api.get_last_update_id(updates)
    time.sleep(1)

try:
  main()
except Exception as error:
  api.send_message('!!! Программа вылетела! :( ({}) '.format(error), 377169456)
