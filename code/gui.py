import tkinter as tk
from tkinter import filedialog
import imageManager as im
from PIL import Image, ImageTk
import numpy as np
from joblib import Parallel, delayed
#import cv2

processes=Parallel(n_jobs=1, backend='loky', prefer='processes', return_as="list")

class app:
    def __init__(self,root):
        
        self.r=root
        self.dpi = self.r.winfo_fpixels('1i')
        self.currentPhoto=None
        self.sR=1
        self.sB=1
        self.w=1000
        self.h=800
        self.r.title("darkRoom")
        self.r.geometry(f"{self.w}x{self.h}")
        self.r.configure(bg="black")
        self.settingBar= tk.Frame(self.r,bg="dark grey",height=15)
        self.settingBar.pack(side="top", fill="x")
        self.initSettingsBar()
        self.mainFrame = tk.Canvas(self.r,height=self.h-15,bg="grey",width=self.w-100,highlightthickness=0,borderwidth=0)

        self.blank = ImageTk.PhotoImage(Image.fromarray(np.zeros(shape=(100,1500, 3), dtype=np.uint8)))
        self.imageDisplayed=self.mainFrame.create_image(0,0,anchor="nw",image=self.blank)
        self.mainFrame.pack(side="left")
        self.editColumn=tk.Frame(self.r,height=self.h-15,width=100,bg="dark grey")
        self.initEditColumn()
        self.editColumn.pack(side="right")
        
        
        return
    
    def initSettingsBar(self):
        self.fileBt=tk.Button(self.settingBar, text="file", command=self.importFile)
        self.fileBt.pack(side="left")
        self.saveBt=tk.Button(self.settingBar, text="save", command=self.saveFile)
        self.saveBt.pack(side="left")



        return
    
    def initEditColumn(self):
        self.invertBt=tk.Button(self.editColumn, text="invert", command=self.invertImage)
        self.invertBt.pack(side="top")
        self.adjustWbBt=tk.Button(self.editColumn, text="WB adjust", command=self.adjustWhiteBalance)
        self.adjustWbBt.pack(side="top")
        self.setWbBt=tk.Button(self.editColumn, text="WB", command=self.setWhiteBalance)
        self.setWbBt.pack(side="top")
        sliderTemp = tk.Scale(self.editColumn, from_=1500, to=6000,resolution=1, orient='horizontal',command=self.setTemp)
        sliderTemp.pack()
        #sliderR = tk.Scale(self.editColumn, from_=-2, to=2,resolution=0.01, orient='horizontal',command=self.setSr)
        #sliderR.pack()
        self.rotateRBt=tk.Button(self.editColumn, text="rotate right", command= lambda: self.rotateImage("r"))
        self.rotateRBt.pack()
        self.rotateLBt=tk.Button(self.editColumn, text="rotate left", command= lambda: self.rotateImage("l"))
        self.rotateLBt.pack()






        return
    
    def importFile(self):
        self.currentImage=filedialog.askopenfilename(
        title="Select a File",
        filetypes=[("All files", "*.*")]
    )
        print(self.currentImage)

        if self.currentImage:
            image=im.openImage(self.currentImage)
            self.currentPhoto=image
            self.updatePhoto()
            #print("here3")
            #image.pilIm.show()
            
            
            
            
        
        return
    def saveFile(self):
        return
    def invertImage(self):
        if self.currentPhoto:
            i,p=im.invertGpu(self.currentPhoto.dataArr)
            newPhoto=im.photo(i,p,format=".RAF",channels=3,orientation=self.currentPhoto.orientation)
            self.currentPhoto=newPhoto
            self.updatePhoto()

            #print("done")
            #i=Image.fromarray(p)
            #i.show()
            

            
        return
    
    def rotateImage(self,dir):
        
        if self.currentPhoto:
            if dir=="r":
                r,p = im.rotateImage(self.currentPhoto.dataArr,dir="r")
                if self.currentPhoto.orientation=="l":
                    newPhoto=im.photo(r,p,format=".RAF",channels=3,orientation="p")
                elif self.currentPhoto.orientation=="p":
                    newPhoto=im.photo(r,p,format=".RAF",channels=3,orientation="l")
            elif dir=="l":
                r,p = im.rotateImage(self.currentPhoto.dataArr,dir="l")
                if self.currentPhoto.orientation=="l":
                    newPhoto=im.photo(r,p,format=".RAF",channels=3,orientation="p")
                elif self.currentPhoto.orientation=="p":
                    newPhoto=im.photo(r,p,format=".RAF",channels=3,orientation="l")
            self.currentPhoto=newPhoto
            self.updatePhoto()

        return
    
    def adjustWhiteBalance(self):
        if self.currentPhoto:
            m=257
            #ref=[201*m,150*m,118*m]
            ref2=[50008, 32311, 25322]
            #target=[71*m,182*m,175*m]
            target2=[128*m,128*m,128*m]
            correctionR=(target2[0]/ref2[0])
            correctionG=(target2[1]/ref2[1])
            correctionB=(target2[2]/ref2[2])
            #print(correctionR)
            #print(correctionB)
            b,p=im.editWB(self.currentPhoto.dataArr,correctionR,correctionG,correctionB)
            newPhoto=im.photo(b,p,format=".RAF",channels=3,orientation=self.currentPhoto.orientation)
            self.currentPhoto=newPhoto
            self.updatePhoto()
        return
    
    def setWhiteBalance(self):
        if self.currentPhoto:
         
            b,p=im.editWB(self.currentPhoto.dataArr,self.sR,self.sG,self.sB)
            
            newPhoto=im.photo(b,p,format=".RAF",channels=3,orientation=self.currentPhoto.orientation)
            self.currentPhoto=newPhoto
        
            self.updatePhoto()


        return

    #def setSr(self,val):
     #   self.sR=float(val)
        
      #  return
    #def setSb(self,val):
    #    self.sB=float(val)
     
    #    return

    def setTemp(self,val):
        self.temp=float(val)
        ref=6500
        desiredRGB = im.kelvinToRgb(self.temp)
  
        refRGB = im.kelvinToRgb(ref)
    
   
        epsilon = 1e-6  
        
        self.sR = desiredRGB[0] / (refRGB[0] + epsilon)
        self.sG = desiredRGB[1] / (refRGB[1] + epsilon)
        self.sB = desiredRGB[2] / (refRGB[2] + epsilon)
        




        return
    
    def updatePhoto(self):
        if self.currentPhoto.orientation=="l":
            # print(self.mainFrame.winfo_width()-1)
            prev=self.currentPhoto.preview(shape=self.mainFrame.winfo_width()-1)
        elif self.currentPhoto.orientation=="p":
            # print(self.mainFrame.winfo_height()-1)
            prev=self.currentPhoto.preview(shape=self.mainFrame.winfo_height()-1)
        self.mainFrame.itemconfig(self.imageDisplayed,image=prev)
        self.mainFrame.image = prev
        self.mainFrame.pack()

        return
    
    def run(self):
        self.r.mainloop()
        return