from tkinter import *
from tkinter import ttk  # combobox
from tkinter import messagebox
from tkinter import filedialog
import tkinter

import numpy as np
from PIL import Image, ImageTk

window = Tk()
window.title("Decode LSB")
window.geometry("600x400")

# phương pháp dựa trên lý thuyết số học
# Blum Blum Shub algorithm với p = 21169 và q = 22189
def PRNG0(seed, total_pixels):
    return int(int(seed) ** 2 % (21169 * 22189)) % total_pixels


def decode(src):

    img = Image.open(src, 'r')
    array = np.array(list(img.getdata()))

    if img.mode == 'RGB':
        n = 3
    elif img.mode == 'RGBA':
        n = 4
    else:
        n = 0
    total_pixels = array.size//n
    print("total pixels : ", total_pixels)
    flag = 0
    while flag == 0:
        hidden_bits = ""
        temp_seed = 1234
        count = 1
        for p in range(total_pixels):
            temp_seed = PRNG0(temp_seed, total_pixels)
            count = count + 1
            if count > total_pixels:
                flag = 1
                break
            for q in range(0, 3):
                hidden_bits += (bin(array[temp_seed][q])[2:][-1])

        hidden_bits = [hidden_bits[i:i+8]
                       for i in range(0, len(hidden_bits), 8)]
        # print("hidden bits" , hidden_bits)

    print("length array", len(hidden_bits))
    global msg
    message = ""
    for i in range(len(hidden_bits)):
        if message[-5:] == "$t3g0":
            break
        else:
            message += chr(int(hidden_bits[i], 2))
    if "$t3g0" in message:
        msg = message[:-5]
        print("Message:", message[:-5])
    else:
        print("No Hidden Message Found")

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


def clickDecode():
    src = imagePath
    print(src)
    decode(src)
    txtMessage.insert(0, msg)


btnEncode = Button(window, text="DECODE", command=clickDecode)
btnEncode.grid(column=1, row=2)

window.mainloop()
