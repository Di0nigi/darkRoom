import numpy as np
from PIL import Image, ImageTk
import rawpy # type: ignore
from scipy.ndimage import zoom



class photo:
    def __init__(self,data,format,channels):
        self.type=format
        self.dataArr=data
        self.dimensions=data.shape
        self.channels=channels
        return
    def toTkImage(self):
        self.pilIm=Image.fromarray(self.dataArr)
      
        self.tkIm = ImageTk.PhotoImage(self.pilIm)
        return self.tkIm
    def resize(self, size):    
        factors = [n / o for n, o in zip(size, self.dataArr.shape[:2])]  
        resized = zoom(self.dataArr, factors + [1], order=3) 
        return resized







def openImage(filePath,height=4000,width=6000):
    with rawpy.imread(filePath) as raw:
        im=raw.postprocess()

       
        
        #im=Image.fromarray(im)
   
        #imgArray = np.fromfile(file,np.uint)
        #l=len(imgArray)
        #datalen=l-72000000
        #cutDownArray= np.array( imgArray[datalen:72000000])


        #cutDownArray.reshape((height,width,3))
        ph = photo(im,filePath[::-1][0:4][::-1],3)
    
        







    return ph