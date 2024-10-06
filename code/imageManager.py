import numpy as np
from PIL import Image, ImageTk
import rawpy 
from scipy.ndimage import zoom
import pycuda.autoinit  # Automatically initializes the CUDA driver
import pycuda.driver as cuda
import numpy as np
from pycuda.compiler import SourceModule



class photo:
    def __init__(self,dataH,dataL,dataO,format,channels,orientation="l",name="newPicture"):
        self.type=format
        self.dataArrOg=dataO
        self.dataArr=dataH
        self.dataArrL=dataL
        self.dimensions=dataH.shape
        self.channels=channels
        self.orientation=orientation
        self.name=name
        return
    def preview(self,shape,ratio=3/2):
        if self.orientation=="l":
            resized=resize(self.dataArrL,(computeRatio(shape,ratio),shape,3))
        elif self.orientation == "p":
             resized=resize(self.dataArrL,(shape,computeRatio(shape,ratio),3))


        self.pilIm=Image.fromarray(resized)
    
        self.prev = ImageTk.PhotoImage(self.pilIm)
     
        return self.prev



def invert(dataArr):
    invertedArr = [65535,65535,65535] - dataArr
    #invertedArr=[]
    #for ind1,elem1 in enumerate(dataArr):
     #   arr=[]
      #  for ind2,elem2 in enumerate(elem1):
       #     l=[]
        #    l.append(65535-elem2[0])
         #   l.append(65535-elem2[1])
          #  l.append(65535-elem2[2])
           # l=np.array(l)
            #arr.append(l)
        #arr=np.array(arr)
        #invertedArr.append(arr)
    #invertedArr=np.array(invertedArr)
    invertedArr8= (invertedArr / 256).astype(np.uint8)
    return invertedArr,invertedArr8


def editContrast(dataArr,cFac):
    grey = 32896
    cFac = cFac+0.01
    contrastArr = np.clip( cFac * (dataArr - grey) +grey ,a_min=[0,0,0],a_max=[65535,65535,65535])
    contrastArr8 = (contrastArr / 256).astype(np.uint8)
    return contrastArr,contrastArr8

def editExposure(dataArr, stop):

    return

def editWB(dataArr,sR,sG,sB):
    balancedarr=[]
    balancedarr=np.clip(dataArr*[sR,sG,sB],a_min=[0,0,0],a_max=[65535,65535,65535])

    #for ind1,elem1 in enumerate(dataArr):
    #    arr=[]
    #    for ind2,elem2 in enumerate(elem1):
    #        newR= min(65535, max(0, elem2[0] * sR))
    #        newG= min(65535, max(0, elem2[1] * sG))
    #        newB= min(65535, max(0, elem2[2] * sB))
    #        l=np.array([newR,newG,newB])
    #        arr.append(l)
    #    arr=np.array(arr)
    #    balancedarr.append(arr)
    #balancedarr=np.array(balancedarr)
    balancedarr8= (balancedarr / 256).astype(np.uint8)
    #print("donebalancing")

        

    return balancedarr,balancedarr8

def resize(dataArr, size):    
    factors = [n / o for n, o in zip(size, dataArr.shape[:2])]  
    resized = zoom(dataArr, factors + [1], order=3) 
    return resized

def turn(dataArr,orientation):
    return


def computeRatio(dim,ratio):
    
    dim2 = dim / ratio
    #elif ori == "p":
     #   dim2= ratio * dim
    #print(dim2)
    return dim2


def openImage(filePath,height=4000,width=6000):
    with rawpy.imread(filePath) as raw:
        imH=raw.postprocess(output_bps=16)
        imL=raw.postprocess(output_bps=8)
        imO=imH.copy()
        name=filePath.split("/")[-1][:-4]
        ph = photo(imH,imL,imH,filePath[::-1][0:4][::-1],3,name=name)
        #print(imH[79][3507])
        #print(imL[79][3507])
    return ph





def rotateImage(dataArr,dir):
    if dir=="l":
        rotated= np.transpose(dataArr, axes=(1, 0, 2))
        rotated= np.flipud(rotated)
        rotated8= (rotated / 256).astype(np.uint8)
    elif dir =="r":
        #c=dataArr.shape[1]
        #r=dataArr.shape[0]
        #rotated=np.zeros(shape=(c,r,3),dtype=np.uint16)
        #for x in range(c):
         #   a=dataArr[:, x:x+1]
          #  rotated[x]=a.reshape((1,r,3))#[::-1]
        rotated= np.transpose(dataArr, axes=(1, 0, 2))
        rotated= np.fliplr(rotated)
        rotated8= (rotated / 256).astype(np.uint8)

    return rotated,rotated8



def kelvinToRgb(kelvinTemp):

    temperature = kelvinTemp / 100.0


    if temperature <= 66:
        red = 255
    else:
        red = temperature - 60
        red = 329.698727446 * (red ** -0.1332047592)
        red = max(0, min(255, red))

    if temperature <= 66:
        green = 99.4708025861 * np.log(temperature) - 161.1195681661
        green = max(0, min(255, green))
    else:
        green = temperature - 60
        green = 288.1221695283 * (green ** -0.0755148492)
        green = max(0, min(255, green))


    if temperature >= 66:
        blue = 255
    else:
        if temperature <= 19:
            blue = 0
        else:
            blue = 138.5177312231 * np.log(temperature - 10) - 305.0447927307
            blue = max(0, min(255, blue))


    rgb = (
        int((red / 255.0) * 65535.0),
        int((green / 255.0) * 65535.0),
        int((blue / 255.0) * 65535.0)
    )
    return rgb


'''

def editWBGpu(dataArr, sR, sB):
    # Define the CUDA kernel
    mod = SourceModule("""
    __global__ void editWhiteBalance(float *dataArr, float *balancedArr, float sR, float sB, int height, int width) {
        int idx_x = blockIdx.x * blockDim.x + threadIdx.x;  // Get the x index (for rows)
        int idx_y = blockIdx.y * blockDim.y + threadIdx.y;  // Get the y index (for columns)

        if (idx_x < height && idx_y < width) {
            // Calculate the index for the 3-channel color values
            int index = (idx_x * width + idx_y) * 3;  // Each pixel has 3 values (R, G, B)

            // Extract the RGB values
            float r = dataArr[index];
            float g = dataArr[index + 1];
            float b = dataArr[index + 2];

            // Apply the scaling factors to R and B
            float newR = fminf(65535.0, fmaxf(0.0, r * sR));
            float newB = fminf(65535.0, fmaxf(0.0, b * sB));

            // Store the balanced RGB values back into balancedArr
            balancedArr[index] = newR;
            balancedArr[index + 1] = g;  // G remains unchanged
            balancedArr[index + 2] = newB;
        }
    }
    """, options=["-allow-unsupported-compiler"])

    # Get the kernel function from the compiled module
    editWhiteBalanceKernel = mod.get_function("editWhiteBalance")

    # Get the shape of the input data (height, width, and channels)
    height, width, channels = dataArr.shape  # Assuming dataArr has shape (height, width, 3)

    # Allocate memory on the GPU for the input and output arrays
    dataArrGpu = cuda.mem_alloc(dataArr.nbytes)
    balancedArrGpu = cuda.mem_alloc(dataArr.nbytes)

    # Copy the input data to the GPU
    cuda.memcpy_htod(dataArrGpu, dataArr)

    # Define block size (threads per block) and grid size (blocks per grid)
    blockSize = (16, 16, 1)  # 16x16 threads per block
    gridSize = ((height + blockSize[0] - 1) // blockSize[0], 
                (width + blockSize[1] - 1) // blockSize[1], 1)

    # Call the kernel on the GPU
    editWhiteBalanceKernel(dataArrGpu, balancedArrGpu, np.float32(sR), np.float32(sB), 
                           np.int32(height), np.int32(width), block=blockSize, grid=gridSize)

    # Allocate space for the result on the host (CPU)
    balancedArr = np.empty_like(dataArr)

    # Copy the result back from the GPU to the host
    cuda.memcpy_dtoh(balancedArr, balancedArrGpu)

    # Convert the 16-bit balanced array to 8-bit for display purposes
    balancedArr8 = (balancedArr / 256).astype(np.uint8)

    # Return both the 16-bit balanced array and the 8-bit version
    return balancedArr, balancedArr8


def invertGpu(dataArr):
    mod = SourceModule("""
__global__ void invert_image(unsigned short *data, unsigned short *inverted, unsigned char *inverted8, int width, int height) {
    int idx = threadIdx.x + blockIdx.x * blockDim.x;
    int num_pixels = width * height;

    if (idx < num_pixels) {
        int base_idx = idx * 3;

        // Invert the RGB values
        inverted[base_idx] = 65535 - data[base_idx];     // Red
        inverted[base_idx + 1] = 65535 - data[base_idx + 1]; // Green
        inverted[base_idx + 2] = 65535 - data[base_idx + 2]; // Blue

        // Also create the 8-bit version by dividing by 256
        inverted8[base_idx] = inverted[base_idx] / 256;     // Red
        inverted8[base_idx + 1] = inverted[base_idx + 1] / 256; // Green
        inverted8[base_idx + 2] = inverted[base_idx + 2] / 256; // Blue
    }
}
""",options=["-allow-unsupported-compiler"])

# Define the kernel function
    invert_image = mod.get_function("invert_image")

    height, width, _ = dataArr.shape
    num_pixels = height * width

    # Flatten the input data array to 1D for easier GPU processing
    dataArr_flat = dataArr.astype(np.uint16).reshape(-1)  # Flatten the input (uint16 type)
    
    # Prepare arrays for the output (inverted and inverted8)
    invertedArr_flat = np.zeros_like(dataArr_flat, dtype=np.uint16)  # Inverted array (16-bit)
    invertedArr8_flat = np.zeros_like(dataArr_flat, dtype=np.uint8)  # Inverted array (8-bit)

    # Allocate GPU memory
    data_gpu = cuda.mem_alloc(dataArr_flat.nbytes)
    inverted_gpu = cuda.mem_alloc(invertedArr_flat.nbytes)
    inverted8_gpu = cuda.mem_alloc(invertedArr8_flat.nbytes)

    # Copy data to the GPU
    cuda.memcpy_htod(data_gpu, dataArr_flat)

    # Launch the kernel with enough threads
    block_size = 256
    grid_size = (num_pixels + block_size - 1) // block_size  # Enough blocks to cover all pixels

    # Run the kernel
    invert_image(data_gpu, inverted_gpu, inverted8_gpu, np.int32(width), np.int32(height), 
                 block=(block_size, 1, 1), grid=(grid_size, 1, 1))

    # Copy the result back to the host
    cuda.memcpy_dtoh(invertedArr_flat, inverted_gpu)
    cuda.memcpy_dtoh(invertedArr8_flat, inverted8_gpu)

    # Reshape the output arrays back to 3D
    invertedArr = invertedArr_flat.reshape(height, width, 3)
    invertedArr8 = invertedArr8_flat.reshape(height, width, 3)

    return invertedArr, invertedArr8

'''

