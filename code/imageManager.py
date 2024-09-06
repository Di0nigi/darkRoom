import numpy as np
from PIL import Image, ImageTk
import rawpy 
from scipy.ndimage import zoom



class photo:
    def __init__(self,data,format,channels):
        self.type=format
        self.dataArr=data
        self.dimensions=data.shape
        self.channels=channels
        return
    def preview(self,shape):
        resized=resize(self.dataArr,(computeRatio(shape,3/2),shape,3))
        print("here")
        self.pilIm=Image.fromarray(resized)
        print("here1")
        self.preview = ImageTk.PhotoImage(self.pilIm)
        print("here2")
        return self.preview





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
        im=raw.postprocess()
        ph = photo(im,filePath[::-1][0:4][::-1],3)
    
    return ph