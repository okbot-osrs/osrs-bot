import win32gui
import win32api
import win32con
import time

import zulrah
print("make sure all these items are fully charged:")
print("sanguenesti staff")
print("serp helm")
print("toxic blowpipe or crystal armor")
print("serp helm")
print("rune pouch")
print("house tablets")
print("camelot tablets")

def pushButton(button):
  win32api.keybd_event(button, 0, 0, 0)
  time.sleep(.15)
  win32api.keybd_event(button, 0, win32con.KEYEVENTF_KEYUP, 0)

def upCam():
  pushButton(38)

def f1():
  pushButton(0x70)

def f3():
  pushButton(0x72)

def f4():
  pushButton(0x73)

def esc():
  pushButton(27)

from inventoryGetter import InventoryGetter

ig = InventoryGetter()
zul = zulrah.Zulrah(ig)

import hashlib
from PIL import ImageGrab, Image
import numpy as np

rlX = ig.rct[0]
rlY = ig.rct[1]
def getTicHash():
  tic = np.array(ImageGrab.grab(bbox = (rlX+500, rlY+345, rlX+505, rlY+350)))
  return hashlib.sha1(tic).hexdigest()
def getTicHashMulti():
  tic = np.array(ImageGrab.grab(bbox = (rlX+465, rlY+345, rlX+470, rlY+350)))
  return hashlib.sha1(tic).hexdigest()

grey = "1b12d6a90c49eb2145a7f5866fcea07af9203269"
whit = "e4b993eedd3f9ff7702585b7fc1f955665a1fa76"
grey2 = "3842edb85effd14743b76e498ee3ecd90893ccdd"
whit2 = "893fb0a8d60bd36c860622862e1db97561ec953a"

def w8NextTic(cur):
  h = getTicHash()
  while(h == cur):
    h = getTicHash()
  return h


def filterRedEx(pic):
  shape = pic.shape
  redCount = 0
  for i in range(shape[0]):
    for j in range(shape[1]):
      if(pic[i][j][0] == 255 and pic[i][j][1] != 255):
        redCount += 1
  return redCount > 6

def click(xy):
  win32api.SetCursorPos((ig.rct[0]+xy[0],ig.rct[1]+xy[1]))
  time.sleep(0.02)
  win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, ig.rct[0]+xy[0], ig.rct[1]+xy[1], 0, 0)
  time.sleep(0.02)
  win32api.SetCursorPos((ig.rct[0]+xy[0],ig.rct[1]+xy[1]))
  win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, ig.rct[0]+xy[0], ig.rct[1]+xy[1], 0, 0)


def clickR(xy):
  win32api.SetCursorPos((ig.rct[0]+xy[0],ig.rct[1]+xy[1]))
  win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, ig.rct[0]+xy[0], ig.rct[1]+xy[1], 0, 0)
  time.sleep(0.012)
  win32api.SetCursorPos((ig.rct[0]+xy[0],ig.rct[1]+xy[1]))
  win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, ig.rct[0]+xy[0], ig.rct[1]+xy[1], 0, 0)

def redClick(p):
  x = int(p[0] + ig.rct[0])
  y = int(p[1] + ig.rct[1])
  win32api.SetCursorPos((x+2,y))
  time.sleep(0.01)
  win32api.SetCursorPos((x,y))
  time.sleep(0.01)
  win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
  time.sleep(0.01)
  box = (x - 8,
         y - 8,
         x + 8,
         y + 8)
  dot = np.array(ImageGrab.grab(bbox=box))
  Image.fromarray(dot).save("dot.png")
  win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)
  if(filterRedEx(dot)):
    print("cool")
  else:
    print("not Cool")

def changeGear(magic):
  #before = ig.capFullInvent()
  f1()
  h = getTicHashMulti()
  for i in range(2):
    for j in range(2):
      click([587 + i*44, 256 + j*35])
  h = w8NextTicMulti(h)
  click([587 + 2*44, 256])
  click([587 + 2*44, 256 + 35])
  click([587 + 3*44, 256])
  if(magic):
    click([587 + 3*44, 256 + 35])
  #after = ig.capFullInvent()
  return h

def containsRedText(txtImg):
  numRed = 0
  for i in range(99):
    if(txtImg[0][i][0] == 255 and
       txtImg[0][i][1] == 0 and
       txtImg[0][i][2] == 0):
      numRed = numRed + 1
  print(numRed)
  return numRed > 5

def classifyPhase(colorToMatch):
  img = ImageGrab.grab(bbox=(ig.rct[0]+313, ig.rct[1]+222, ig.rct[0]+360, ig.rct[1]+285))
  toClassify = np.array(img)
  count = 0
  for i in range(toClassify.shape[0]):
    for j in range(toClassify.shape[1]):
      if(toClassify[i][j][0] < colorToMatch[0]+10 and
         toClassify[i][j][0] > colorToMatch[0]-10 and
         toClassify[i][j][1] < colorToMatch[1]+10 and
         toClassify[i][j][1] > colorToMatch[1]-10 and
         toClassify[i][j][2] < colorToMatch[2]+10 and
         toClassify[i][j][2] > colorToMatch[2]-10):
        count+=1
        if(count > 5):
          return True
  return False

def classifyMelePhase(colorToMatch):
  img = ImageGrab.grab(bbox=(ig.rct[0]+184, ig.rct[1]+166, ig.rct[0]+218, ig.rct[1]+193))
  img.save("phase.png")
  toClassify = np.array(img)
  count = 0
  for i in range(toClassify.shape[0]):
    for j in range(toClassify.shape[1]):
      if(toClassify[i][j][0] < colorToMatch[0]+10 and
         toClassify[i][j][0] > colorToMatch[0]-10 and
         toClassify[i][j][1] < colorToMatch[1]+10 and
         toClassify[i][j][1] > colorToMatch[1]-10 and
         toClassify[i][j][2] < colorToMatch[2]+10 and
         toClassify[i][j][2] > colorToMatch[2]-10):
        count+=1
        if(count > 5):
          return True
  return False

class getHP:
  def __init__(self, bigR):
    self.hpHashes = np.load("healthHashArray.npy")
    self.healthBBOX = (bigR[0]+530, bigR[1]+85, bigR[0]+555, bigR[1]+98)
  def get(self):
    return (len(self.hpHashes)-np.where(self.hpHashes == self.getHealthHash())[0]+1)[0]
  def getHealthHash(self):
    arr = np.array(ImageGrab.grab(bbox=self.healthBBOX))
    hash = hashlib.sha1(arr).hexdigest()
    return hash
hpGetter = getHP([rlX, rlY])
#print(hpGetter.get())

def w8ticsMulti(num, curHash, text, pt):#deprecated : when i eat it runs to boss??!?!
  curHash = w8NextTicMulti(curHash)
  #k = 0
  #if(hpGetter.get() < 75):
  #  if(not zul.eat(f1)):
  #    return False#We're out of food
  #  k = 4
  #  curHash = w8NextTicMulti(curHash)
  #  curHash = w8NextTicMulti(curHash)
  #  curHash = w8NextTicMulti(curHash)
  #  curHash = w8NextTicMulti(curHash)
  #print("the pt is {}".format(pt))
  zul.clickR(pt)
  for i in range(num-1):#-k):
    curHash = w8NextTicMulti(curHash)
    print(text.format(i))
  return True
  return curHash#FACKKKKKKK. Gotta make a hash object live.

def w8NextTicMulti(cur):
  h = getTicHashMulti()
  while(h == cur):
    h = getTicHashMulti()
  if(hpGetter.get() < 45):
    zul.eat(f1)
  return h

def killZul():
  tic = getTicHash()
  print(tic)
  while(getTicHash() == tic):
    pass
    #print("test")
  print(getTicHash())
  time.sleep(0.2)
  zul.clickRblue(0, [299, 197])#boat
  time.sleep(3)
  aHash = getTicHash()
  while((aHash != grey and aHash != whit) and 
        (aHash != grey2 and aHash != whit2)):
    aHash = getTicHash()
    #print(aHash)
  click([674, 472])#Staff
  aHash = w8NextTicMulti(aHash)
  
  f4()
  click([615, 406])#thrawl
  click([642, 67])#NE map
  click([570, 51])#compas
  f3()
  click([734,401])#preserve
  click([693,444])#augury
  #print("hear")
  aHash = w8NextTicMulti(aHash)
  upCam()
  aHash = w8NextTicMulti(aHash)
  print(1)
  zul.prePot1(f1)
  aHash = w8NextTicMulti(aHash)
  print(2)
  aHash = w8NextTicMulti(aHash)
  print(3)
  aHash = w8NextTicMulti(aHash)
  print(4)
  aHash = w8NextTicMulti(aHash)
  print(5)
  zul.prePot2()
  aHash = w8NextTicMulti(aHash)
  print(6)
  if(not ig.weildingSang()):
    print("lmao hopefully i click this time!")
    click([674, 472])#Staff
  
  aHash = w8NextTicMulti(aHash)
  print(7)
  
  for e in range(8, 11):
    aHash = w8NextTicMulti(aHash)
    print(e)
  
  zul.clickR([185, 225])#click on zulrah
  
  for e in range(16):#maging first spawn
    aHash = w8NextTicMulti(aHash)
    print(e)
  
  f3()
  click([653, 363])#rangeprotect
  
  for e in range(5):
    aHash = w8NextTicMulti(aHash)
  print("classifying nowwwwwww")
  
  #now classify the snake
  #Using brute force and numpy arrays. This is the only action done in the tic.
  if(classifyPhase([121, 30, 168])):
    print("mage")
    aHash = changeGear(False)
    aHash = w8NextTicMulti(aHash)
    zul.clickR([337, 248])
    aHash = w8NextTicMulti(aHash)
    f3()
    click([611, 368])#mage protect
    click([655, 446])#rigour
    aHash = w8ticsMulti(26, aHash, "(mage)first spawn (mage east): {}/26", [337, 248])
    click([606, 134])
    aHash = w8NextTicMulti(aHash)
    aHash = changeGear(True)
    aHash = w8NextTicMulti(aHash)
    f3()
    click([654, 369])#range
    click([691, 447])#augury
    aHash = w8NextTicMulti(aHash)
    for i in range(7):
      aHash = w8NextTicMulti(aHash)
      print("(mage)seccond spawn(range South) running to spot: {}/7".format(i))
      
    zul.clickR([381, 349])
  
    aHash = w8ticsMulti(20, aHash, "(mage)seccond spawn(range South): {}/20", [381, 349])
  
    aHash = changeGear(False)
    aHash = w8NextTicMulti(aHash)
    f3()
    click([611, 368])#mage protect
    click([655, 446])#rigour
    aHash = w8NextTicMulti(aHash)
    aHash = w8NextTicMulti(aHash)
    aHash = w8NextTicMulti(aHash)
    zul.clickR([212, 181])
  
    aHash = w8ticsMulti(24, aHash, "(mage)third spawn(mager west): {}/24", [212, 181])
  
    aHash = changeGear(True)
    aHash = w8NextTicMulti(aHash)
    f3()
    click([611, 368])#mage protect
    click([691, 447])#augury
    aHash = w8NextTicMulti(aHash)
    aHash = w8NextTicMulti(aHash)
    aHash = w8NextTicMulti(aHash)
    aHash = w8NextTicMulti(aHash)
  
    zul.clickR([351, 156])
    aHash = w8ticsMulti(22, aHash, "(mage)fifth spawn(meleer): {}/22", [351, 156])
    
    f3()
    click([654, 369])#range
    click([704, 114])#go east on minimap
    print("going east rn")
    for i in range(6):
      aHash = w8NextTicMulti(aHash)
      print("(mage)running to sixth spawn(range east): {}/6".format(i))
    f4()
    click([615, 406])#thrawl
    aHash = w8NextTicMulti(aHash)
    zul.clickR([332, 188])
    aHash = w8ticsMulti(17, aHash, "(mage)sixth spawn(range east): {}/17", [332, 188])
    zul.clickR([186, 310])
  
    f3()
    click([654, 369])#range
    aHash = w8ticsMulti(10, aHash, "(mage)seventh spawn(range south): {}/10", [186, 310])
    #run west here
    click([606, 110])
    aHash = w8NextTicMulti(aHash)
    aHash = w8NextTicMulti(aHash)
    aHash = w8NextTicMulti(aHash)
    aHash = w8NextTicMulti(aHash)
    aHash = w8NextTicMulti(aHash)
    aHash = w8NextTicMulti(aHash)
    aHash = w8NextTicMulti(aHash)
    aHash = w8NextTicMulti(aHash)
    zul.clickR([368, 336])
    aHash = w8ticsMulti(17, aHash, "(mage)seccond seventh spawn(range south): {}/17", [368, 336])
    
    aHash = changeGear(False)
    aHash = w8NextTicMulti(aHash)
    f3()
    click([611, 368])#mage protect
    click([655, 446])#rigour
    aHash = w8NextTicMulti(aHash)
  
  
    zul.clickR([214, 200])
    aHash = w8ticsMulti(28, aHash, "(mage)eigth spawn(mage west): {}/28", [214, 200])
  
    
    aHash = w8NextTicMulti(aHash)
    f3()
    click([654, 369])#range
    click([691, 447])#augury
    aHash = w8NextTicMulti(aHash)
    aHash = changeGear(True)
    aHash = w8NextTicMulti(aHash)
    
    zul.clickR([352, 165])
    aHash = w8ticsMulti(28, aHash, "(mage)ninth spawn(range middle): {}/28", [352, 165])
    return
  ########################################################
  ########################################################
  aHash = w8NextTicMulti(aHash)
  
  if(classifyPhase([167, 166, 137])):
    print("range")
    aHash = w8NextTicMulti(aHash)
    aHash = w8NextTicMulti(aHash)
    zul.clickR([337, 248])
    for i in range(20):
      aHash = w8NextTicMulti(aHash)
      print("(range)first spawn: {}/20".format(i))
    click([606, 129])#map bot left
  
    f3()#             turn off
    click([654, 374])#range
  
    for i in range(10):
      aHash = w8NextTicMulti(aHash)
    aHash = w8NextTicMulti(aHash)
    
    zul.clickR([346, 171])
    for i in range(5):
      aHash = w8NextTicMulti(aHash)
    print("cp1")
    f4()
    click([615, 406])#thrawl
    click([673, 51])#north left NEEDS UPDATE
    aHash = w8NextTicMulti(aHash)
    aHash = w8NextTicMulti(aHash)
    aHash = w8NextTicMulti(aHash)
    aHash = w8NextTicMulti(aHash)
    aHash = w8NextTicMulti(aHash)
    zul.clickR([322, 245])
    for i in range(3):
      aHash = w8NextTicMulti(aHash)
    for i in range(5):
      aHash = w8NextTicMulti(aHash)
    click([640, 123])#safe spot
    print("cp2")
    aHash = w8NextTicMulti(aHash)
    aHash = w8NextTicMulti(aHash)
    aHash = w8NextTicMulti(aHash)
    zul.clickR([345, 188])
    for i in range(2):
      aHash = w8NextTicMulti(aHash)
    click([661, 99])#north left, but yyyyy???!
    print("cp3")
    aHash = w8NextTicMulti(aHash)
    aHash = w8NextTicMulti(aHash)
    zul.clickR([332, 225])
    aHash = w8NextTicMulti(aHash)
    zul.clickR([332, 225])
    aHash = w8NextTicMulti(aHash)
    aHash = w8NextTicMulti(aHash)
    aHash = w8NextTicMulti(aHash)
    aHash = w8NextTicMulti(aHash)
    aHash = w8NextTicMulti(aHash)
    aHash = w8NextTicMulti(aHash)
    f3()
    click([616, 370])#mage prayer
    click([654, 438])#rigour
    aHash = w8NextTicMulti(aHash)
  
    aHash = w8NextTicMulti(aHash)
    aHash = changeGear(False)
    aHash = w8NextTicMulti(aHash)
    aHash = w8NextTicMulti(aHash)
    aHash = w8NextTicMulti(aHash)
    aHash = w8NextTicMulti(aHash)
    zul.clickR([161, 268])#mage West
  
    print("cp4")
  
    for i in range(16):
      aHash = w8NextTicMulti(aHash)
      print("(range)thrid spawn(mage west): {}/16".format(i))
    click([647, 135])
    aHash = w8NextTicMulti(aHash)
    f3()
    click([654, 369])#range
    click([691, 447])#augury
    aHash = w8NextTicMulti(aHash)
    aHash = changeGear(True)
    aHash = w8NextTicMulti(aHash)
    aHash = w8NextTicMulti(aHash)
    aHash = w8NextTicMulti(aHash)
    zul.clickR([380, 309])
    
    for i in range(15):
      aHash = w8NextTicMulti(aHash)
      print("(range)fourth spawn(range south): {}/15".format(i))
    click([704, 111])
    aHash = w8NextTicMulti(aHash)
    f3()
    click([616, 370])#mage prayer
    click([654, 438])#rigour
  
    aHash = w8NextTicMulti(aHash)
    aHash = w8NextTicMulti(aHash)
    aHash = changeGear(False)
    aHash = w8NextTicMulti(aHash)
    aHash = w8NextTicMulti(aHash)
    aHash = w8NextTicMulti(aHash)
    aHash = w8NextTicMulti(aHash)
  
    zul.clickR([327, 173])
    #run west here
    for i in range(14):
      aHash = w8NextTicMulti(aHash)
      print("(range)fifth spawn(mage east): {}/14".format(i))
    
    click([607, 112])
  
    aHash = changeGear(True)
    aHash = w8NextTicMulti(aHash)
    f3()
    click([616, 370])#mage prayer
    click([691, 447])#augury
    aHash = w8NextTicMulti(aHash)
    aHash = w8NextTicMulti(aHash)
    for i in range(4):
      aHash = w8NextTicMulti(aHash)
      print("(range)running to sixth spawn(range middle): {}/4".format(i))
  
    f3()
    click([654, 369])#range
    aHash = w8NextTicMulti(aHash)
    aHash = w8NextTicMulti(aHash)
    f4()
    click([615, 406])#thrawl
    aHash = w8NextTicMulti(aHash)
    zul.clickR([345, 166])
    for i in range(21):
      aHash = w8NextTicMulti(aHash)
      print("(range)sixth spawn(range middle): {}/23".format(i))
    
    zul.clickR([222, 194])
    for i in range(18):
      aHash = w8NextTicMulti(aHash)
      print("(range)seventh spawn(range west): {}/18".format(i))
    aHash = changeGear(False)
    aHash = w8NextTicMulti(aHash)
    f3()
    click([616, 370])#mage prayer
    click([654, 438])#rigour
    zul.clickR([345, 166])
    for i in range(24):
      aHash = w8NextTicMulti(aHash)
      print("(range)eigth spawn(last mage middle): {}/24".format(i))
    exit()
  
  print("mele")
  f3()
  click([655, 367])#turn off range protect
  aHash = w8NextTicMulti(aHash)
  aHash = w8NextTicMulti(aHash)
  zul.clickR([186, 223])
  aHash = w8NextTicMulti(aHash)
  for i in range(6):
    aHash = w8NextTicMulti(aHash)
  click([644, 103])#map
  aHash = w8NextTicMulti(aHash)
  aHash = w8NextTicMulti(aHash)
  zul.clickR([217, 239])
  for i in range(8):
    aHash = w8NextTicMulti(aHash)
  f3()
  click([616, 370])#mage prayer
  click([654, 438])#rigour
  aHash = w8NextTicMulti(aHash)
  aHash = changeGear(False)
  aHash = w8NextTicMulti(aHash)
  zul.clickR([220, 230])
  for i in range(12):
    aHash = w8NextTicMulti(aHash)
  aHash = changeGear(True)
  click([614, 137])
  aHash = w8NextTicMulti(aHash)
  f3()
  click([654, 368])#range prayer
  click([703, 449])#augury
  for i in range(10):
    print(i)
    aHash = w8NextTicMulti(aHash)
  if(classifyMelePhase([167, 166, 137])):
    print("range west")
    zul.clickR([222, 195])
    f3()
    click([654, 368])#range prayer
    for i in range(22):
      aHash = w8NextTicMulti(aHash)
      print("(range west(mele)) {}/22 third spawn range west".format(i))

    f3()
    click([616, 370])#mage prayer
    click([654, 438])#rigour
    aHash = w8NextTicMulti(aHash)
    aHash = w8NextTicMulti(aHash)
    aHash = changeGear(False)
    aHash = w8NextTicMulti(aHash)
    aHash = w8NextTicMulti(aHash)
    zul.clickR([371, 307])
    for i in range(9):
      aHash = w8NextTicMulti(aHash)
      print("(range west(mele)) {}/9 fourth spawn mage south".format(i))
    click([669, 129])
    aHash = w8NextTicMulti(aHash)
    aHash = w8NextTicMulti(aHash)
    aHash = w8NextTicMulti(aHash)
    zul.clickR([270, 264])
    for i in range(22):
      aHash = w8NextTicMulti(aHash)
      print("(range west(mele)) {}/22 fourth spawn mage south".format(i))
    click([630, 97])
    aHash = w8NextTicMulti(aHash)
    f3()
    click([616, 370])#mage prayer
    click([703, 449])#augury
    aHash = w8NextTicMulti(aHash)
    aHash = w8NextTicMulti(aHash)
    aHash = changeGear(True)
    aHash = w8NextTicMulti(aHash)
    f4()
    click([615, 406])#thrawl
    zul.clickR([376, 149])
    aHash = w8ticsMulti(18, aHash, "(range west(mele)) {}/18 fifth spawn mele middle", [376, 149])
    click([678, 128])
    aHash = w8NextTicMulti(aHash)
    f3()
    click([654, 368])#range prayer
    aHash = w8NextTicMulti(aHash)
    aHash = w8NextTicMulti(aHash)
    aHash = w8NextTicMulti(aHash)
    aHash = w8NextTicMulti(aHash)
    zul.clickR([393, 134])
    aHash = w8ticsMulti(16, aHash, "(range west(mele)) {}/16 sixth range east", [393, 134])
    click([625, 103])
    f3()
    click([616, 370])#mage prayer
    click([654, 438])#rigour
    aHash = changeGear(False)
    aHash = w8NextTicMulti(aHash)
    aHash = w8NextTicMulti(aHash)
    aHash = w8NextTicMulti(aHash)
    zul.clickR([362, 301])
    aHash = w8ticsMulti(24, aHash, "(range west(mele)) {}/24 seventh mage south", [362, 301])
  
  else:
    print("range South")
    zul.clickR([372, 310])
    for i in range(34):
      aHash = w8NextTicMulti(aHash)
      print("(range south(mele)) {}/34 third spawn range south".format(i))
    f3()
    click([655, 370])#range off
    aHash = w8NextTicMulti(aHash)
    aHash = w8NextTicMulti(aHash)
    f4()
    click([615, 406])#thrawl
    zul.clickR([344, 170])
    for i in range(19):
      aHash = w8NextTicMulti(aHash)
      print("(range south(mele)) {}/19 fourth spawn mele middle".format(i))
    f3()
    click([616, 370])#mage prayer
    click([654, 438])#rigour
    aHash = w8NextTicMulti(aHash)
    aHash = changeGear(False)
    aHash = w8NextTicMulti(aHash)
    aHash = w8NextTicMulti(aHash)
    aHash = w8NextTicMulti(aHash)
    zul.clickR([218, 180])
    for i in range(14):
      aHash = w8NextTicMulti(aHash)
      print("(range south(mele)) {}/14 fifth spawn mage west".format(i))
  
    click([705, 111])
    aHash = changeGear(True)
    aHash = w8NextTicMulti(aHash)
    f3()
    click([654, 368])#range prayer
    click([703, 449])#augury
    aHash = w8NextTicMulti(aHash)
    aHash = w8NextTicMulti(aHash)
    aHash = w8NextTicMulti(aHash)
    aHash = w8NextTicMulti(aHash)
    aHash = w8NextTicMulti(aHash)
    zul.clickR([185, 316])#range South
    aHash = w8ticsMulti(24, aHash, "(range south(mele)) {}/24 sixth spawn range south", [185, 316])
    f3()
    click([616, 370])#mage prayer
    click([654, 438])#rigour
    aHash = w8NextTicMulti(aHash)
    aHash = changeGear(False)
    zul.clickR([185, 316])#mage South
    aHash = w8ticsMulti(24, aHash, "(range south(mele)) {}/24 sixth spawn mage south", [185, 316])

if(__name__ == "__main__"):
  killZul()