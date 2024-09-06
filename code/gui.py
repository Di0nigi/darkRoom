import tkinter as tk
from tkinter import filedialog
import imageManager as im
from PIL import Image, ImageTk
import numpy as np
#import cv2


class app:
    def __init__(self,root):
        
        self.r=root
        self.dpi = self.r.winfo_fpixels('1i')
        self.w=1000
        self.h=800
        self.r.title("darkRoom")
        self.r.geometry(f"{self.w}x{self.h}")
        self.r.configure(bg="black")
        self.settingBar= tk.Frame(self.r,bg="dark grey",height=15)
        self.settingBar.pack(side="top", fill="x")
        self.initSettingsBar()
        self.mainFrame = tk.Canvas(self.r,height=self.h-15,bg="black",width=self.w-100,highlightthickness=0,borderwidth=0)

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
        return
    
    def importFile(self):
        self.currentImage=filedialog.askopenfilename(
        title="Select a File",
        filetypes=[("All files", "*.*")]
    )
        print(self.currentImage)
        print(self.dpi)
        if self.currentImage:
            image=im.openImage(self.currentImage)
            prev=image.preview(shape=self.mainFrame.winfo_width()-1)
            #print("here3")
            #image.pilIm.show()
            self.mainFrame.itemconfig(self.imageDisplayed,image=prev)
            self.mainFrame.image = prev
            self.mainFrame.pack()
            
            
            
        
        return
    def saveFile(self):
        return
    def invertImage(self):
        return
    
    def run(self):
        self.r.mainloop()
        return