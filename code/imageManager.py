import numpy as np
from PIL import Image, ImageTk
import rawpy 
from scipy.ndimage import zoom



class photo:
    def __init__(self,dataH,dataL,format,channels):
        self.type=format
        self.dataArr=dataH
        self.dataArrL=dataL
        self.dimensions=dataH.shape
        self.channels=channels
        return
    def preview(self,shape):
        resized=resize(self.dataArrL,(computeRatio(shape,3/2),shape,3))
        print("here")
        self.pilIm=Image.fromarray(resized)
        print("here1")
        self.preview = ImageTk.PhotoImage(self.pilIm)
        print("here2")
        return self.preview



def invert(dataArr):
    invertedArr=[]
    for ind1,elem1 in enumerate(dataArr):
        arr=[]
        for ind2,elem2 in enumerate(elem1):
            l=[]
            l.append(65535-elem2[0])
            l.append(65535-elem2[1])
            l.append(65535-elem2[2])
            l=np.array(l)
            arr.append(l)
        arr=np.array(arr)
        invertedArr.append(arr)
    invertedArr=np.array(invertedArr)
    invertedArr8= (invertedArr / 256).astype(np.uint8)
    return invertedArr,invertedArr8



def resize(dataArr, size):    
    print("here4")
    factors = [n / o for n, o in zip(size, dataArr.shape[:2])]  
    resized = zoom(dataArr, factors + [1], order=3) 
    return resized


def computeRatio(dim,ratio):
    print("here5")

    dim2 = dim / ratio
    return dim2

def openImage(filePath,height=4000,width=6000):
    with rawpy.imread(filePath) as raw:
        imH=raw.postprocess(output_bps=16)
        imL=raw.postprocess(output_bps=8)
        ph = photo(imH,imL,filePath[::-1][0:4][::-1],3)
    
    return ph