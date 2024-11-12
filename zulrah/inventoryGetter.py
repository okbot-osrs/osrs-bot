from PIL import ImageGrab, Image
import numpy as np
import hashlib
from functions import Functions

from const import FULL_INVENT, GAP_X, GAP_Y, WIDTH_ITEM, HEIGHT_ITEM


class InventoryGetter:
  def __init__(self):
    self.f = Functions()
    self.rct = self.f.rect
    self.invnt = (FULL_INVENT[0] + self.f.rect[0],
                  FULL_INVENT[1] + self.f.rect[1],
                  FULL_INVENT[2] + self.f.rect[0],
                  FULL_INVENT[3] + self.f.rect[1])
    self.capFullInvent()

    self.dramen2600 = "359d76f1cf653d25fd53ba51faf4590bfd1add01"

  def capFullInvent(self):
    self.inventry = np.array(ImageGrab.grab(bbox=self.invnt))
    return self.inventry
  
  def append(self, arr1, arr2):
    return np.append(arr1, arr2, axis=0)

  def getItem(self, pos):#pos: 0-27
    x = pos%4
    y = int(pos/4)
    r = (self.invnt[0]+x*(GAP_X+WIDTH_ITEM),
         self.invnt[1]+y*(GAP_Y+HEIGHT_ITEM),
         self.invnt[0]+x*(GAP_X+WIDTH_ITEM) + WIDTH_ITEM,
         self.invnt[1]+y*(GAP_Y+HEIGHT_ITEM) + HEIGHT_ITEM)
    return hashlib.sha1(np.array(ImageGrab.grab(bbox = r))).hexdigest()
  
  def weildingSang(self):
    hash = self.getItem(26)
    if(hash == self.dramen2600):
      return True
    return False

  # def getItem(self, i):
  #   x = i%4
  #   y = int(i/4)
  #   indx1 = x*(GAP_X + WIDTH_ITEM)
  #   indx2 = ((x+1)*WIDTH_ITEM + x*GAP_X)
  #   indy1 = y*(GAP_Y + HEIGHT_ITEM)
  #   indy2 = ((y+1)*HEIGHT_ITEM + y*GAP_Y)
  #   return self.inventry[indy1:indy2, indx1:indx2]
    

  def processItems(self, fn):#will take an array of 28 items, and make a binary mask of shape (32,32,3), then save it
    items = self.capFullInvent()
    staff = self.getItem(26)
    Image.fromarray(staff).save("staff.png")
    print(hashlib.sha1(staff).hexdigest())
    # bitmapArr = np.ones((28, 32,32,3), dtype = np.uint8)
    # bitmapArr = bitmap * 255
    # print(bitmap.shape)
    # for i in range(1, 28):
    #   itm = self.getItem(i)
    #   for j in range(32):
    #     for k in range(32):
    #       if(first[j][k][0] != itm[j][k][0]):
    #         first[j][k][0] = 0
    #       if(first[j][k][1] != itm[j][k][1]):
    #         first[j][k][1] = 0
    #       if(first[j][k][2] != itm[j][k][2]):
    #         first[j][k][2] = 0
          # if(first[j][k][0] != items[i][j][k][0] or
          #    first[j][k][1] != items[i][j][k][1] or
          #    first[j][k][2] != items[i][j][k][2]):
          #   bitmap[j][k][0] =  0
          #   bitmap[j][k][1] =  0
          #   bitmap[j][k][2] =  0
    # colorArray = np.zeros((32,32,3), dtype = np.uint8)
    # for i in range(32):
    #   for j in range(32):
    #     if(bitmap[i][j][0] == 255):
    #       colorArray[i][j][0] = first[i][j][0]
    #       colorArray[i][j][1] = first[i][j][1]
    #       colorArray[i][j][2] = first[i][j][2]
    # Image.fromarray(bitmap).save("inventItems//bitIMG/"+fn+".png")
    # Image.fromarray(colorArray).save("inventItems/colorIMG/"+fn+".png")
    # np.save("inventItems/bit/"+fn+".npy", bitmap)
    # np.save("inventItems/color/"+fn+".npy", colorArray)
 
    #Image.fromarray(first).save("great karambwan.png")

def saveItemSingle(i, fn):
  #arrEmptyInvent = np.load("inventItems/arrInventEmpty.npy")
  ig = InventoryGetter()
  print(ig.getItem(26))
  # ig.capFullInvent()
  # firstItem = ig.getItem(0)
  # Image.fromarray(firstItem).save("hi.png")
  # res = arrEmptyInvent[0]-firstItem
  # arrBinary = np.zeros((32,32,3), dtype=np.uint8)
  # for i in range(32):
  #   for j in range(32):
  #     for k in range(3):
  #       if(res[i][j][k]!=0):
  #         arrBinary[i][j][0] = 255
  #         arrBinary[i][j][1] = 255
  #         arrBinary[i][j][2] = 255
  # np.save("inventItems/bit/"+fn+".npy", arrBinary)
  # np.save("inventItems/color/"+fn+".npy", np.bitwise_and(arrBinary, firstItem))
  # Image.fromarray(arrBinary).save("inventItems/bitIMG/"+fn+".png")
  # Image.fromarray(np.bitwise_and(arrBinary, firstItem)).save("inventItems/colorIMG/"+fn+".png")

if(__name__ == "__main__"):
  saveItemSingle(0, "garbage4")