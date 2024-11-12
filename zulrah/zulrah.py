from PIL import ImageGrab, Image
import win32gui
import win32api
import win32con
import time
import numpy as np

class OffensivePrayer(Enum):
  NONE = 0
  AUGURY = 1
  RIGOUR = 2
  PIETY = 3

class DefensivePrayer(Enum):
  NONE = 0
  PROTECT_FROM_MAGIC = 1
  PROTECT_FROM_MISSILES = 2
  PROTECT_FROM_MELEE = 3

class Zulrah:
  def __init__(self, game):
    self.rct = game.rct
    self.eatCount = 0
    self.curOffensivePrayer = OffensivePrayer.NONE
    self.curdefensivePrayer = DefensivePrayer.NONE

  def prePot1(self, inv):
    inv()
    self.click([635, 393])#divine range pot
    self.click([715, 291])#karam

  def prePot2(self):
    self.click([714, 398])#angler
    self.click([673, 394])#forgotten brew

  def eat(self, inv):
    if(self.eatCount <  4):
      inv()
      self.click([595+44*self.eatCount, 365])#manta
      self.click([595, 407])#p pot
      self.click([595+44*self.eatCount, 329])#karam
      self.eatCount += 1
      return True
    return False

  def clickRblue(self, count, xy):
    win32api.SetCursorPos((self.rct[0]+xy[0],self.rct[1]+xy[1]))
    time.sleep(0.02)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, self.rct[0]+xy[0], self.rct[1]+xy[1], 0, 0)
    time.sleep(0.02)
    win32api.SetCursorPos((self.rct[0]+xy[0],self.rct[1]+xy[1]))
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, self.rct[0]+xy[0], self.rct[1]+xy[1], 0, 0)
    time.sleep(0.2)
    aBox = (xy[0]+self.rct[0],
            xy[1]+30+self.rct[1],
            xy[0]+100+self.rct[0],
            xy[1]+31+self.rct[1])
    text = np.array(ImageGrab.grab(bbox=aBox))
    if(not self.containsBlueText(text)):
      print("failed clickR")
      print(count)
      win32api.SetCursorPos((self.rct[0]+xy[0],self.rct[1]+xy[1]-20))
      time.sleep(0.03)
      if(count < 4):
        self.clickRblue(count+1, xy)
      else:
        exit()
    else:
      self.click([xy[0], xy[1]+30])#click attack option
      return

  def clickR(self, xy):
    self.recursiveClickR(0, 0, xy)
  
  def recursiveClickR(self, count, success, xy):
    win32api.SetCursorPos((self.rct[0]+xy[0],self.rct[1]+xy[1]))
    time.sleep(0.02)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, self.rct[0]+xy[0], self.rct[1]+xy[1], 0, 0)
    time.sleep(0.02)
    win32api.SetCursorPos((self.rct[0]+xy[0],self.rct[1]+xy[1]))
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, self.rct[0]+xy[0], self.rct[1]+xy[1], 0, 0)
    time.sleep(0.04)
    aBox = (xy[0]+self.rct[0],
            xy[1]+30+self.rct[1],
            xy[0]+100+self.rct[0],
            xy[1]+31+self.rct[1])
    text = np.array(ImageGrab.grab(bbox=aBox))
    if(not self.containsRedText(text)):
      print("failed clickR")
      print(count)
      win32api.SetCursorPos((self.rct[0]+xy[0],self.rct[1]+xy[1]-20))
      time.sleep(0.03)
      if(count < 4):
        self.recursiveClickR(count+1, success, xy)
      else:
        print("never got the correct text color on right clicks.")
        exit()
    else:
      #could check for a red click,
      # but i think check right click for red is enough.
      self.click([xy[0], xy[1]+25])#click attack option
      if(success != 1):
        self.recursiveClickR(count, success+1, xy)
    
  def click(self, xy):
    win32api.SetCursorPos((self.rct[0]+xy[0],self.rct[1]+xy[1]))
    time.sleep(0.02)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, self.rct[0]+xy[0], self.rct[1]+xy[1], 0, 0)
    time.sleep(0.02)
    win32api.SetCursorPos((self.rct[0]+xy[0],self.rct[1]+xy[1]))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, self.rct[0]+xy[0], self.rct[1]+xy[1], 0, 0)

  def containsRedText(self, txtImg):
    numRed = 0
    for i in range(99):
      if(txtImg[0][i][0] == 255 and
         txtImg[0][i][1] == 0 and
         txtImg[0][i][2] == 0):
        numRed = numRed + 1
    return numRed > 5

  def containsBlueText(self, txtImg):
    numRed = 0
    for i in range(99):
      if(txtImg[0][i][0] == 0 and
         txtImg[0][i][1] == 255 and
         txtImg[0][i][2] == 255):
        numRed = numRed + 1
    return numRed > 5