import numpy as np
import cv2
import requests
import os

class Image_processing:

  def __init__(self, haar_xml='haarcascade_frontalface_default.xml', path='/photos/', image_format='.jpg' ):
    self.__face_cascade = cv2.CascadeClassifier(haar_xml)
    self.__path = path
    self.__image_format = image_format

  def __url_to_image(self, url):
    # download the image, convert it to a NumPy array, and then read it into OpenCV format
    resp = requests.get(url, stream=True).raw
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    return image

  def __bgr2gray(self, image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

  def __get_is_face(self, url):
    # is face on image? It needs only link
    image = self.__url_to_image(url)
    gray = self.__bgr2gray(image)
    faces = self.__face_cascade.detectMultiScale(gray)
    if faces != ():
      return True
    return False

  def save_file(self, url, max_uid):
    if self.__get_is_face(url) == True:
      image = self.__url_to_image(url)
      uid_photo = max_uid + 1
      cur_path = os.getcwd()
      name = 'photo_' + str(uid_photo) + self.__image_format
      photo_path = cur_path + self.__path
      os.chdir(photo_path)
      cv2.imwrite(name, image)
      os.chdir(cur_path)
      return True
    return False