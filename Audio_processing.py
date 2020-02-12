import librosa
import os
import requests

class Audio_processing:

  __temp_name = '1.ogg'

  def __init__(self, path='audio/', audio_format='.wav', sr=16000):
    # By audio path get audio (x & sr), and add init information
    self.__path = path
    self.__audio_format = audio_format
    self.__sr = sr # 16 kHz


  def __url_to_audio(self, url):
    # convert and get name
    doc = requests.get(url)
    with open(self.__temp_name, 'wb') as f:
      f.write(doc.content)

  def __convert_audio_and_change_name(self, loc, audio_uid):
    # Using next audio uid create name and save audio file
    x, sr = librosa.load(loc)
    loc_new = self.__path + 'audio_message_' + str(audio_uid) + self.__audio_format
    librosa.output.write_wav(loc_new, x, sr = sr)
    os.remove(loc)

  def process_audio(self, url, max_uid):
    audio_uid = max_uid + 1
    #loc = self.__path + self.__url_to_audio(url)
    self.__url_to_audio(url)
    self.__convert_audio_and_change_name(self.__temp_name, audio_uid)
    return True