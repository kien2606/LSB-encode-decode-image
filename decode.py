
import numpy as np
from PIL import Image

def PRNG0(seed, total_pixels):
    # phương pháp dựa trên lý thuyết số học
    # Blum Blum Shub algorithm với p = 21169 và q = 22189
    return int(int(seed) ** 2 % (21169 * 22189)) % total_pixels

def decode(src):

    img = Image.open(src, 'r')
    array = np.array(list(img.getdata()))

    if img.mode == 'RGB':
        n = 3
    elif img.mode == 'RGBA':
        n = 4
    else:
        n=0
    total_pixels = array.size//n
    print("total pixels : " , total_pixels)
    flag = 0
    while flag == 0:
        hidden_bits = ""
        temp_seed = 1234
        count = 1
        for p in range(total_pixels):
            temp_seed = PRNG0(temp_seed, total_pixels)
            count = count + 1
            if count > total_pixels :
                flag = 1
                break
            for q in range(0, 3):
                hidden_bits += (bin(array[temp_seed][q])[2:][-1])

        hidden_bits = [hidden_bits[i:i+8] for i in range(0, len(hidden_bits), 8)]
        # print("hidden bits" , hidden_bits)

    print("length array" ,len(hidden_bits) )
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

decode("C:\\Users\\Tran Hoai Nam\\Desktop\\codeLSB\\done.png")