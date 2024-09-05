import tkinter as tk
from tkinter import filedialog
import imageManager as im
from PIL import Image, ImageTk
import numpy as np
#import cv2


class app:
    def __init__(self,root):
        self.r=root
        self.w=900
        self.h=900
        self.r.title("darkRoom")
        self.r.geometry(f"{self.w}x{self.h}")
        self.r.configure(bg="black")
        self.settingBar= tk.Frame(self.r,bg="dark grey",height=15)
        self.settingBar.pack(side="top", fill="x")
        self.initSettingsBar()
        self.mainFrame = tk.Canvas(self.r,height=self.h-15,width=self.w-100,bg="black",highlightthickness=0,borderwidth=0)

        self.blank = ImageTk.PhotoImage(Image.fromarray(np.zeros((self.h-15,self.w-100, 3), dtype=np.uint8)))
        self.imageDisplayed=self.mainFrame.create_image(0,0,image=self.blank)
        self.mainFrame.pack(side="left")
        self.editColumn=tk.Frame(self.r,height=self.h-15,width=100,bg="dark grey")
        self.editColumn.pack(side="right")
        
        return
    
    def initSettingsBar(self):
        self.fileBt=tk.Button(self.settingBar, text="file", command=self.importFile)
        self.fileBt.pack(side="left")



        return
    def initEditColumn(self):
        return
    
    def importFile(self):
        self.currentImage=filedialog.askopenfilename(
        title="Select a File",
        filetypes=[("All files", "*.*")]
    )
        print(self.currentImage)
        if self.currentImage:
            image=im.openImage(self.currentImage)
            image.dataArr=image.resize((self.w,self.h,3))
            tkim=image.toTkImage()
            self.mainFrame.itemconfig(self.imageDisplayed,image=tkim)
            self.mainFrame.image = tkim
            self.mainFrame.pack()

            
            #image.pilIm.show()
            
            ##cv2.imshow('Image', image)

# Step 3: Use cv2.waitKey() to display the window until a key is pressed
            #cv2.waitKey(0)

# Step 4: Close all OpenCV windows
            #cv2.destroyAllWindows()
            
        
        return
    
    def run(self):
        self.r.mainloop()
        return