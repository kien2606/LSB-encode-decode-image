from tkinter import *
from tkinter import ttk  # combobox
from tkinter import messagebox
from tkinter import filedialog
import tkinter
from turtle import width

import numpy as np
from PIL import Image, ImageTk

window = Tk()
window.title("Encode LSB")
window.geometry("600x400")

# encode
def PRNG0(seed, total_pixels):
    # phương pháp dựa trên lý thuyết số học
    # Blum Blum Shub algorithm với p = 21169 và q = 22189
    return int(int(seed) ** 2 % (21169 * 22189)) % total_pixels

def encode(src, message, dest):

    img = Image.open(src, 'r')
    width, height = img.size
    array = np.array(list(img.getdata()))

    if img.mode == 'RGB':
        n = 3
    elif img.mode == 'RGBA':
        n = 4
    else:
        n = 0
    total_pixels = array.size//n
    print("hello there", total_pixels)
    if message != None:
        message += "$t3g0"
    else:
        message = ""
    b_message = ''.join([format(ord(i), "08b") for i in message])
    req_pixels = len(b_message)
    print("leng message", req_pixels)
    if req_pixels > total_pixels:
        print("ERROR: Need larger file size")

    else:
        index = 0
        already_seen = list()
        seed = 1234
        while index < req_pixels:
            seed = PRNG0(seed, total_pixels)
            print("Next seed : ", seed)
            if seed not in already_seen:
                already_seen.append(seed)
                for i in range(0, 3):
                    if index < req_pixels:
                        array[seed][i] = int(bin(array[seed][i])[2:9] + b_message[index], 2)
                        print((bin(array[seed][i])[2:9]))
                        print(b_message[index])
                        print(f"array[{seed}][{i}]: " , bin(array[seed][i])[2:9] + b_message[index] )
                        index += 1
            else:
                print("ERROR: Need another key")
                break

        array = array.reshape(height, width, n)
        enc_img = Image.fromarray(array.astype('uint8'), img.mode)
        enc_img.save(dest)
        print("Image Encoded Successfully")


# GUI
def openImage():
    global imagePath
    imagePath = filedialog.askopenfilename()
    load = Image.open(imagePath).resize((300, 300))
    img = ImageTk.PhotoImage(load)
    lblImage.configure(image=img)
    lblImage.image = img


btnSelectImage = Button(window, text="SELECT", command=openImage)
btnSelectImage.grid(column=0, row=0)
img = ImageTk.PhotoImage(Image.open("white.png").resize((300, 300)))
lblImage = Label(window, image=img)
lblImage.grid(column=1, row=0)

lblMessage = Label(window, text="MESSAGE")
lblMessage.grid(column=0, row=1)
txtMessage = Entry(window, width=70)
txtMessage.grid(column=1, row=1)

lblImageOutput = Label(window, text="OUTPUT IMAGE")
lblImageOutput.grid(column=0, row=2)
txtImageOutput = Entry(window, width=70)
txtImageOutput.grid(column=1, row=2)



def clickEncode():
    msg = txtMessage.get()
    print(msg)
    src = imagePath
    print(src)
    dest = txtImageOutput.get()
    print(dest)
    encode(src, msg, dest)
    messagebox.showinfo("Notification", "Image Encoded Successfully")


btnEncode = Button(window, text="ENCODE", command=clickEncode)
btnEncode.grid(column=1, row=3)

window.mainloop()
