import numpy as np
from PIL import Image
import hashlib



def PRNG0(seed, total_pixels):
    # phương pháp dựa trên lý thuyết số học
    # Blum Blum Shub algorithm với p = 21169 và q = 22189
    return int(int(seed) ** 2 % (21169 * 22189)) % total_pixels

def PRNG1(seed, total_pixels):
    # phương pháp cơ bản
    # Phương pháp nửa bình phương (Middle-square method)
    return int(str(int(seed) ** 2).zfill(8)[2:6]) % total_pixels

def PRNG2(seed, total_pixels):
    # phương pháp cơ bản
    # phương pháp đồng dư bậc 2 với n = 10
    return int(int(seed) * (int(seed) + 1) % 2**10) % total_pixels

def PRNG3(seed, total_pixels):
    # phương pháp dựa trên mật mã học nguyên thuỷ
    # phương pháp sử dụng hàm băm SHA-256
    return int.from_bytes(hashlib.sha256(str(seed).encode()).digest(), "little") % total_pixels


def encode(src, message, dest):

    img = Image.open(src, 'r')
    width, height = img.size
    array = np.array(list(img.getdata()))

    if img.mode == 'RGB':
        n = 3
    elif img.mode == 'RGBA':
        n = 4
    else:
        n=0
    total_pixels = array.size//n
    print("hello there" , total_pixels)
    if message != None:
        message += "$t3g0" 
    else:
        message = ""
    b_message = ''.join([format(ord(i), "08b") for i in message])
    req_pixels = len(b_message) 
    print("leng message" , req_pixels)
    if req_pixels > total_pixels:
        print("ERROR: Need larger file size")

    else:
        index=0
        already_seen = list()
        seed = 1234
        while index < req_pixels:
            seed = PRNG3(seed , total_pixels)
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

        array=array.reshape(height, width, n)
        enc_img = Image.fromarray(array.astype('uint8'), img.mode)
        enc_img.save(dest)
        print("Image Encoded Successfully")
    
encode("C:\\Users\\84961\\Desktop\\SetoLSB\\raw\\cleanImg.png", "select message", "C:\\Users\\84961\\Desktop\\SetoLSB\\encode\\done.png")