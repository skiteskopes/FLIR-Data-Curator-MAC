'''
-------------------------------------------------------
FLIR Systems - Windows Data_Curation_Tool ver 1.1.0
-------------------------------------------------------
by: Bill Zhang
- Tkinter application for opening and cropping the RGB counterparts of FLIR
  IR camera images to better match the resolution and frame of reference.
- Internal AGC functionality is translated from Andres Prieto-Moreno's
  BosonUSB.cpp
- https://github.com/FLIR/BosonUSB/blob/master/BosonUSB.cpp
- 8-21-2019: Functionality with keypress
- 8-30-19: Integration of side_by_side.py along with frame_cropper tool
- 8-30-19: Integration of Delete button in side_by_side with makedirs
- 8-31-19: Integration of keypress for side_by_side tool
- 8-31-19: Integration of Error Message system for user friendliness
- 9-4-19: Integration of Pair Count and filename label for image_viewer_function
- 9-6-19: Mac OS version available
- 9-4-19: Integration of metafiledata for FocalLength

'''
from Tkinter import *
import ffmpy
import shutil
import cv2
import numpy as np
import imghdr
import os
import PIL.Image, PIL.ImageTk
import numpy as np
import tkFileDialog as filedialog
import math
import gc
import tkMessageBox as messagebox
import tifffile as tiff
global counter
global number_label
import tifffile

''' import libraries'''
root = Tk()
root.title("FLIR Data Curation Tool ver 1.1.0")
root.iconbitmap('flam.icns')
root.geometry("350x150")
menu_label = Label(root,text="Data_Curation_Tool version 1.1.0 by Bill Zhang").place(x=15,y=10)
frame_cropper_label = Label(root,text="Use Frame Cropper Tool:").place(x=15,y=50)
side_by_side_label = Label(root,text="Open RGB and IR Tool:").place(x=15,y=100)

def image_viewer_function():
    root.withdraw()
    global counter
    window = Toplevel()
    window.title("FLIR Image Viewer")
    window.iconbitmap('flam.icns')
    window.geometry("850x175")
    counter = 0
    '''initialize root window basics'''

    def select_rgb():
        filename1 = filedialog.askdirectory()
        label1 = Label(window, text = filename1).grid(row =2, column =2)
        global rgbfilepath
        rgbfilepath = filename1
    '''Tkinter functions that are binded to sample selection buttons'''

    rgbbutton = Button(window, text = "Select", command =
    select_rgb, bg = 'navy', fg = 'white').grid(row =2, column =1)
    ''' button widgets for selecting sample images'''

    def thirteen():
       global scale_percent
       scale_percent = 88

    def nineteen():
        global scale_percent
        scale_percent = 200
    def twentyfive():
        global scale_percent
        scale_percent = 225
    ''' functions for resizing the IR image based off radio button'''

    radioselection = IntVar()

    R1 = Radiobutton(window, text="13mm 640, 32 deg HFOV", variable=radioselection, value=1,
                      command=thirteen)
    R1.grid(row=4,column=1 )

    R2 = Radiobutton(window, text="19mm 640, 32 deg HFOV", variable=radioselection, value=2,
                      command=nineteen)
    R2.grid(row=5,column=1 )

    R3 = Radiobutton(window, text="25mm 640, 32 deg HFOV", variable=radioselection, value=3,
                      command=twentyfive)
    R3.grid(row=6,column=1 )
    '''radio button configuration'''

    radiolabel = Label(window,text="Select camera model here:").grid(row=4,column=0)
    instructions = Label(window,text="Select Directory for Data containting RGB and IR images:").grid(row=0,column=1)
    RGB = Label(window,text="Directory").grid(row = 2, column = 0)

    ''' Labels for the button widgets and instructions in the root window'''

    def open_images():
        global sad_label
        global scale_percent
        global photo
        global photo1
        global new_ir
        global new_rgb
        global path
        global canvas1
        global pair_amount

        gc.disable()
        window1 = Toplevel()
        window1.title("FLIR Image Viewer")
        window1.iconbitmap('flam.icns')
        global rgbfilepath
        try:
            path = rgbfilepath
        except:
            window1.destroy()
            sad_label = Label(window,text="ERROR: Failed to Select Folder", fg = 'red')
            sad_label.grid(row=5,column=2)

        tiff_files = list()
        jpg_files = list()
        new_rgb = list()
        new_ir = list()
        for ir_filename in os.listdir(path):
            if ir_filename.endswith('.TIFF'):
                tiff_files.append(ir_filename)
        for rgb_filename in os.listdir(path):
            if rgb_filename.endswith('JPG'):
                jpg_files.append(rgb_filename)
        try:
            sad_label.config(text = 'CORRECTED: Folder Processed', fg = 'green')
        except:
            print('hello')
        for file in tiff_files:
            ir_name = file[:19]
            for files in jpg_files:
                rgb_name = files[:19]
                if ir_name == rgb_name:
                    new_rgb.append(files)
                    new_ir.append(file)
        pair_amount= len(new_rgb)
        grabrgb = path + str('/')+str(new_rgb[0])
        grabir = path + str('/')+str(new_ir[0])
        rgb_img1 = cv2.cvtColor(cv2.imread(grabrgb), cv2.COLOR_BGR2RGB)
        rgb_scale_percent = 15
        rgb_width = int(rgb_img1.shape[1] * rgb_scale_percent / 100)
        rgb_height = int(rgb_img1.shape[0] * rgb_scale_percent / 100)
        dim1 = (rgb_width, rgb_height)
        rgb_img = cv2.resize(rgb_img1, dim1, interpolation = cv2.INTER_AREA)

        '''creates array for RGB image sample'''

        ir_img = np.zeros((512, 640), dtype = "uint8")
        ir_img_mask = np.zeros((512, 640), dtype = "uint8")
        array=tiff.imread(grabir)
        max = np.amax(array)
        min = np.amin(array)
        for a in range (0,512):
            for b in range (0,640):
                ir_img[a][b] = ( ( 255 * ( array[a][b] - min) ) ) // (max-min)

        try:
            ir_resized_width = int(ir_img.shape[1] * scale_percent // 100)
        except:
            sad_label = Label(window,text="ERROR: Failed to Select Camera Model", fg = 'red')
            sad_label.grid(row=4,column=2)
            window1.destroy()
        ir_resized_height = int(ir_img.shape[0] * scale_percent // 100)
        try:
            sad_label.config(text = 'CORRECTED: Files Processed', fg = 'green')
        except:
            print('hello')
        dim = (ir_resized_width, ir_resized_height)
        ir_img1 = cv2.resize(ir_img, dim, interpolation =cv2.INTER_AREA)
        '''Translation of BosonUSB's AGC to properly create array for IR image'''

        height, width, nochannels = rgb_img.shape
        height1, width1, = ir_img1.shape
        newheight = height +75
        newwidth = width +563
        window1.geometry('{0}x{1}'.format(newwidth,newheight))
        window1.resizable(width=False, height=False)

        def Next():
            global new_rgb
            global new_ir
            global path
            global scale_percent
            global canvas1
            global photo
            global photo1
            global counter
            global pair_amount
            global grabrgb
            global grabir
            global number_label

            counter = counter + 1

            if counter > (pair_amount-1):
                counter = (pair_amount-1)

            grabrgb = path + str('/')+str(new_rgb[counter])
            grabir = path + str('/')+str(new_ir[counter])

            rgb_img1 = cv2.cvtColor(cv2.imread(grabrgb), cv2.COLOR_BGR2RGB)
            rgb_scale_percent = 15
            rgb_width = int(rgb_img1.shape[1] * rgb_scale_percent / 100)
            rgb_height = int(rgb_img1.shape[0] * rgb_scale_percent / 100)
            dim1 = (rgb_width, rgb_height)
            rgb_img = cv2.resize(rgb_img1, dim1, interpolation = cv2.INTER_AREA)

            ir_img = np.zeros((512, 640), dtype = "uint8")
            array=tiff.imread(grabir)
            max = np.amax(array)
            min = np.amin(array)
            for a in range (0,512):
                for b in range (0,640):
                    ir_img[a][b] = ( ( 255 * ( array[a][b] - min) ) ) // (max-min)
            ir_resized_width = int(ir_img.shape[1] * scale_percent // 100)
            ir_resized_height = int(ir_img.shape[0] * scale_percent // 100)
            dim = (ir_resized_width, ir_resized_height)
            ir_img1 = cv2.resize(ir_img, dim, interpolation =cv2.INTER_AREA)
            height, width, nochannels = rgb_img.shape
            height1, width1, = ir_img1.shape
            newheight = height +  25
            newwidth = width*2
            ir_resized_width = int(ir_img.shape[1] * scale_percent // 100)
            ir_resized_height = int(ir_img.shape[0] * scale_percent // 100)
            dim = (ir_resized_width, ir_resized_height)
            ir_img1 = cv2.resize(ir_img, dim, interpolation =cv2.INTER_AREA)
            rgbimage = PIL.Image.fromarray(rgb_img)
            photo = PIL.ImageTk.PhotoImage(rgbimage)
            canvas1_w = width/2
            canvas1_h = height/2 + 25
            canvas1.create_image(canvas1_w, canvas1_h ,image=photo)


            canvas2_w =  width1/2
            canvas2_h = height1/2 +25
            irimage = PIL.Image.fromarray(ir_img1)
            photo1 = PIL.ImageTk.PhotoImage(irimage)
            canvas2 = canvas1.create_image(canvas2_w + width,canvas2_h,image=photo1)
            next_label = Label(canvas1, text = '{0} of {1}'.format(counter+1, pair_amount), bg = 'navy', fg = 'white').place(x=width-21, y=height + 40)
            rgblabel2 = Label(canvas1, text = '{0}'.format(new_rgb[counter]), bg = 'navy', fg = 'white').place(x=width//2-80, y=height + 40)
            irlabel2 =  Label(canvas1, text = '{0}'.format(new_ir[counter]), bg = 'navy', fg = 'white').place(x=width+563//2-50, y=height + 40)
        def Back():
            global new_rgb
            global new_ir
            global path
            global scale_percent
            global canvas1
            global photo
            global photo1
            global counter
            global pair_amount
            global grabrgb
            global grabir
            global number_counter
            global number_label
            counter = counter - 1
            if counter < 0:
                counter = 0

            grabrgb = path + str('/')+str(new_rgb[counter])
            grabir = path + str('/')+str(new_ir[counter])

            rgb_img1 = cv2.cvtColor(cv2.imread(grabrgb), cv2.COLOR_BGR2RGB)
            rgb_scale_percent = 15
            rgb_width = int(rgb_img1.shape[1] * rgb_scale_percent / 100)
            rgb_height = int(rgb_img1.shape[0] * rgb_scale_percent / 100)
            dim1 = (rgb_width, rgb_height)
            rgb_img = cv2.resize(rgb_img1, dim1, interpolation = cv2.INTER_AREA)

            ir_img = np.zeros((512, 640), dtype = "uint8")
            array=tiff.imread(grabir)
            max = np.amax(array)
            min = np.amin(array)
            for a in range (0,512):
                for b in range (0,640):
                    ir_img[a][b] = ( ( 255 * ( array[a][b] - min) ) ) // (max-min)
            ir_resized_width = int(ir_img.shape[1] * scale_percent // 100)
            ir_resized_height = int(ir_img.shape[0] * scale_percent // 100)
            dim = (ir_resized_width, ir_resized_height)
            ir_img1 = cv2.resize(ir_img, dim, interpolation =cv2.INTER_AREA)
            height, width, nochannels = rgb_img.shape
            height1, width1, = ir_img1.shape
            newheight = height +  25
            newwidth = width*2
            ir_resized_width = int(ir_img.shape[1] * scale_percent // 100)
            ir_resized_height = int(ir_img.shape[0] * scale_percent // 100)
            dim = (ir_resized_width, ir_resized_height)
            ir_img1 = cv2.resize(ir_img, dim, interpolation =cv2.INTER_AREA)
            rgbimage = PIL.Image.fromarray(rgb_img)
            photo = PIL.ImageTk.PhotoImage(rgbimage)
            canvas1_w = width/2
            canvas1_h = height/2 + 25
            canvas1.create_image(canvas1_w, canvas1_h ,image=photo)


            canvas2_w =  width1/2
            canvas2_h = height1/2 +25
            irimage = PIL.Image.fromarray(ir_img1)
            photo1 = PIL.ImageTk.PhotoImage(irimage)
            canvas2 = canvas1.create_image(canvas2_w + width,canvas2_h,image=photo1)
            print(counter)
            back_label = Label(canvas1, text = '{0} of {1}'.format(counter+1, pair_amount), bg = 'navy', fg = 'white').place(x=width-21, y=height + 40)
            rgblabel3 = Label(canvas1, text = '{0}'.format(new_rgb[counter]), bg = 'navy', fg = 'white').place(x=width//2-80, y=height + 40)
            irlabel3 =  Label(canvas1, text = '{0}'.format(new_ir[counter]), bg = 'navy', fg = 'white').place(x=width+563//2-50, y=height + 40)
        def Delete():
            global counter
            grabrgb = path + str('/')+str(new_rgb[counter])
            grabir = path + str('/')+str(new_ir[counter])
            os.chdir(rgbfilepath)

            directory = os.getcwd()
            trash = directory + str('/')+ 'Trash'

            try:
                os.makedirs(trash)
            except:
                print('file exists')

            print(grabrgb)
            print(grabir)
            print(trash)
            shutil.move(grabrgb,trash)
            shutil.move(grabir,trash)

        def Help():
            messagebox.showinfo('Help','Use the Up and Down arrow Keys to better navigate through the images. Delete transfers unwanted images into a newly created folder for future reference')


        def next_key(event):
            Next()
        def back_key(event):
            Back()
        window1.bind("<Up>",next_key)
        window1.bind("<Down>",back_key)
        'Integrates keyboard functionality to navigate throught the pictures'
        canvas1 = Canvas(window1, width = width, height = height, bg='navy blue')
        canvas1.pack(expand = YES, fill=BOTH)
        rgblabel1 = Label(canvas1, text = '{0}'.format(new_rgb[0]), bg = 'navy', fg = 'white').place(x=width//2-80, y=height + 40)
        irlabel1 =  Label(canvas1, text = '{0}'.format(new_ir[0]), bg = 'navy', fg = 'white').place(x=width+563//2-50, y=height + 40)
        number_label = Label(canvas1, text = '{0} of {1}'.format(counter+1, pair_amount), bg = 'navy', fg = 'white').place(x=width-21, y=height + 40)
        next_button = Button(canvas1, text = "Next", command = Next, bg ='navy', fg='white').place(x=0,y=0)
        back_button = Button(canvas1, text="Back", command = Back, bg= 'navy', fg='white').place(x=35,y=0)
        delete_button = Button(canvas1, text="Delete", command = Delete, bg= 'navy', fg='white').place(x=70,y=0)
        help_button = Button(canvas1, text="Help", command = Help, bg= 'navy', fg='white').place(x=112,y=0)
        rgbimage = PIL.Image.fromarray(rgb_img)
        photo = PIL.ImageTk.PhotoImage(rgbimage)
        canvas1_w = width/2
        canvas1_h = height/2 + 25
        canvas1.create_image(canvas1_w, canvas1_h ,image=photo)
        canvas2_w =  width1/2
        canvas2_h = height1/2 +25
        irimage = PIL.Image.fromarray(ir_img1)
        photo1 = PIL.ImageTk.PhotoImage(irimage)
        canvas2 = canvas1.create_image(canvas2_w + width,canvas2_h,image=photo1)
    button = Button(window, text = "Start", bg = 'navy blue', fg = 'white',
    command = open_images).grid(row = 7, column = 1)
    window.resizable(width=False, height=False)

def frame_cropper_function():
    global irfilepath
    global focal_counter
    global focal_label
    global rgb_counter
    global label1
    global label2
    global ir_counter
    global FocalLength
    root.withdraw()
    window = Tk()
    window.title("FLIR Frame Cropper Tool V1")
    window.iconbitmap('flam.icns')
    window.geometry("850x175")
    '''initialize root window basics'''
    focal_counter = 0
    rgb_counter = 0
    ir_counter = 0
    focal_label = Label(window,text="dummy", fg = 'Green')
    label1 = Label(window,text="dummy", fg = 'Green')
    label2 = Label(window,text="dummy", fg = 'Green')
    def select_rgb():
        global label1
        global rgb_counter
        if rgb_counter >= 1 or rgb_counter == 0:
            label1.destroy()
        filename1 = filedialog.askopenfilename()
        label1 = Label(window, text = filename1)
        label1.grid(row =2, column =2)
        global rgbfilepath
        rgbfilepath = filename1
        rgb_counter = rgb_counter + 1
    def select_ir():
        global irfilepath
        global FocalLength
        global focal_counter
        global focal_label
        global label2
        global ir_counter
        if ir_counter >= 1 or rgb_counter == 0:
            label2.destroy()
        filename2 = filedialog.askopenfilename()
        label2 = Label(window, text = filename2)
        label2.grid(row=3, column=2)
        irfilepath = filename2
        with tifffile.TiffFile(irfilepath) as tif:
            tif_tags = {}
            for tag in tif.pages[0].tags.values():
                name, value = tag.name, tag.value
                tif_tags[name] = value
            cc=tif_tags['ExifTag']
            ee = cc['FocalLength']
            FocalLength = ee[0]

            if focal_counter >= 1 or focal_counter == 0:
                focal_label.destroy()
            if FocalLength == 19:
                focal_label = Label(window,text="{0}mm sized lens detected from file".format(FocalLength), fg = 'Green')
                focal_label.grid(row = 5, column = 2)
                R2.select()
                R1.deselect()
                R3.deselect()
                R2.invoke()
            if FocalLength == 13:
                focal_label = Label(window,text="{0}mm sized lens detected from file".format(FocalLength), fg = 'Green')
                focal_label.grid(row = 4, column = 2)
                R2.deselect()
                R1.select()
                R3.deselect()
                R1.invoke()
            if FocalLength == 25:
                focal_label = Label(window,text="{0}mm sized lens detected from file".format(FocalLength), fg = 'Green')
                focal_label.grid(row = 6, column = 2)
                R3.select()
                R2.deselect()
                R1.deselect()
                R3.invoke()
            focal_counter = focal_counter + 1
            ir_counter = ir_counter + 1
    '''Tkinter functions that are binded to sample selection buttons'''

    rgbbutton = Button(window, text = "Select", command =
    select_rgb,bg ='navy', fg='white').grid(row =2, column =1)
    irbutton = Button(window, text = "Select", command =
    select_ir,bg ='navy', fg='white').grid(row=3, column =1)
    ''' button widgets for selecting sample images'''

    def thirteen():
       global scale_percent
       scale_percent = 175
    def nineteen():
        global scale_percent
        scale_percent = 175
    def twentyfive():
        global scale_percent
        scale_percent = 175
    ''' functions for resizing the IR image based off radio button'''
    radioselection = IntVar()

    R1 = Radiobutton(window, text="13mm 640, 32 deg HFOV", variable=radioselection, value=1,
                      command=thirteen)
    R1.grid(row=4,column=1 )

    R2 = Radiobutton(window, text="19mm 640, 32 deg HFOV", variable=radioselection, value=2,
                      command=nineteen)
    R2.grid(row=5,column=1 )

    R3 = Radiobutton(window, text="25mm 640, 32 deg HFOV", variable=radioselection, value=3,
                      command=twentyfive)
    R3.grid(row=6,column=1 )
    '''radio button configuration'''
    R1.select()
    radiolabel = Label(window,text="Select camera model here:").grid(row=4,column=0)
    instructions = Label(window,text="Select files for sample RGB and IR frames here:").grid(row=0,column=1)
    RGB = Label(window,text="RGB:").grid(row = 2, column = 0)
    IR = Label(window,text="IR:").grid(row = 3, column = 0)
    ''' Labels for the button widgets and instructions in the root window'''

    def open_images():
        global photo
        global star
        global rgbimage
        global rgbfilepath
        global irfilepath
        global irimage
        global photo1
        global label1
        global height
        global width
        global height1
        global width1
        global scale_percent
        global sad_label
        global rgb_error
        global ir_error
        global FocalLength
        '''creates global variables to extract data from root window'''
        gc.disable()
        '''disable garbage collection to prevent images from being deleted from memory'''

        window1 = Toplevel()
        window1.title("FLIR Frame Cropper Tool V1")
        window1.iconbitmap('flam.icns')


        '''initializes new window basics'''

        try:
            rgb_img1 = cv2.cvtColor(cv2.imread(rgbfilepath), cv2.COLOR_BGR2RGB)
        except:
            window1.destroy()
            rgb_error = Label(window,text="ERROR: Missing RGB File", fg = 'red')
            rgb_error.grid(row=5,column=2)

        rgb_scale_percent = 50
        rgb_width = int(rgb_img1.shape[1] * rgb_scale_percent / 100)
        try:
            rgb_error.config(text = 'CORRECTED: RGB File Present', fg = 'green')
        except:
            print('hello')
        rgb_height = int(rgb_img1.shape[0] * rgb_scale_percent / 100)
        dim1 = (rgb_width, rgb_height)
        rgb_img = cv2.resize(rgb_img1, dim1, interpolation = cv2.INTER_AREA)
        '''creates array for RGB image sample'''

        ir_img = np.zeros((512, 640), dtype = "uint8")
        ir_img_mask = np.zeros((512, 640), dtype = "uint8")
        try:
            array=tiff.imread(irfilepath)
        except:
            window1.destroy()
            ir_error = Label(window,text="ERROR: Missing IR File", fg = 'red')
            ir_error.grid(row=6,column=2)
        max = np.amax(array)
        min = np.amin(array)
        try:
            ir_error.config(text = 'CORRECTED: IR File Present', fg = 'green')
        except:
            print('hello')
        for a in range (0,512):
            for b in range (0,640):
                ir_img[a][b] = ( ( 255 * ( array[a][b] - min) ) ) // (max-min)
        try:
            ir_resized_width = int(ir_img.shape[1] * scale_percent // 100)
        except:
            sad_label = Label(window,text="ERROR: Failed To Select Camera Model", fg = 'red')
            sad_label.grid(row=4,column=2)
            window1.destroy()

        ir_resized_height = int(ir_img.shape[0] * scale_percent // 100)
        try:
            sad_label.config(text = 'CORRECTED: Files Processed', fg = 'green')
        except:
            print('Hello')
        dim = (ir_resized_width, ir_resized_height)
        ir_img1 = cv2.resize(ir_img, dim, interpolation =cv2.INTER_AREA)
        '''Translation of BosonUSB's AGC to properly create array for IR image'''

        height, width, nochannels = rgb_img.shape
        height1, width1, = ir_img1.shape
        newheight = height +  25
        newwidth = width
        window1.geometry('{0}x{1}'.format(newwidth,height))

        '''assigns proper variables for new windowsize based off arrays created'''

        def Submit():
            global sad_label
            global canvas2_w
            global canvas2_h
            datax =  canvas2_w - width1//2
            datay =  -(canvas2_h - (height1//2) - 25)
            datax1 = datax + width1
            datay1 = datay + height1
            select_file = filedialog.askdirectory()
            os.chdir(select_file)
            for file in os.listdir(select_file):
                if file.endswith('JPG' or 'jpg'):
                    img = cv2.imread(file)
                    crop_img = img[int(datay*2):int(datay1*2),int(datax*2):int(datax1*2)]
                    cv2.imwrite('{0}_new.jpg'.format(file),crop_img)
            success_label = Label(window,text="Successfully Cropped Images :^)", fg = 'green').grid(row=4,column=2)

        def Crop():
            global canvas2_w
            global canvas2_h
            global datax
            global datay
            global datax1
            global datay1
            datax =  canvas2_w - width1//2
            datay =  -(canvas2_h - (height1//2) - 25)
            upper_right_corner = (datax,datay)

            datax1 = datax + width1
            datay1 = datay + height1

            img = cv2.imread(rgbfilepath)
            crop_img = img[int(datay*2):int(datay1*2),int(datax*2):int(datax1*2)]
            cv2.imshow("Crop_Sample",crop_img)
            instructions = Label(window,text="Select files for sample RGB and IR frames here:").grid(row=0,column=1)

        def Help():
            messagebox.showinfo('Help', "Crop creates sample cropped image. Submit asks for directory where you want your RGB images to be cropped. Match the bounding box of the IR counterpart onto the RGB counterpart with WASD and click Submit.")
        canvas1 = Canvas(window1, width = width, height = height, bg='navy blue')
        canvas1.pack(expand = YES, fill=BOTH)

        crop_button = Button(canvas1, text = "Crop", command = Crop, bg ='navy', fg='white').place(x=0,y=0)
        save_button = Button(canvas1, text="Submit", command = Submit, bg= 'navy', fg='white').place(x=35,y=0)
        help_button = Button(canvas1, text="Help", command = Help, bg= 'navy', fg='white').place(x=85,y=0)
        #buttons

        rgbimage = PIL.Image.fromarray(rgb_img)
        photo = PIL.ImageTk.PhotoImage(rgbimage)
        canvas1_w = width/2
        canvas1_h = height/2 + 25

        canvas1.create_image(canvas1_w, canvas1_h ,image=photo)
        #code for the IR images
        global canvas2_w
        global canvas2_h
        canvas2_w =  width1/2
        canvas2_h = height1/2 +25
        irimage = PIL.Image.fromarray(ir_img1)
        photo1 = PIL.ImageTk.PhotoImage(irimage)
        canvas2 = canvas1.create_image(canvas2_w,canvas2_h,image=photo1)
        left, right, up, down = -10,10,-10,10
        def keypress(event):
            global text
            global canvas2_w
            global canvas2_h
            x = 0
            y= 0
            xturn =0
            yturn =0
            if event.char =="a":
                x= left
                canvas2_w = canvas2_w - 10
            elif event.char=="d":
                x = right
                canvas2_w = canvas2_w + 10
            elif event.char=="w":
                y = up
                canvas2_h = canvas2_h + 10
            elif event.char=="s":
                y = down
                canvas2_h = canvas2_h - 10
            canvas1.move(canvas2, x, y)

        window1.bind("<Key>", keypress)

    button = Button(window, text = "Start", bg = 'navy blue', fg = 'white',
    command = open_images).grid(row = 7, column = 1)
    window.resizable(width=False, height=False)

frame_cropper_button = Button(root, text = "Start", command =
frame_cropper_function, bg = 'navy blue', fg = 'white').place(x=250,y=50)

side_by_side_button = Button(root, text = "Start", command =
image_viewer_function, bg = 'navy blue', fg = 'white').place(x=250,y=100)

root.resizable(width=False, height=False)
root.mainloop()
