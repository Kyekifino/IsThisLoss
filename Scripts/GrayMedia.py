from PIL import Image
import os, sys

path = os.path.join("Media", "750ResizedPics")
dirs = os.listdir( path )
final_size = 100;

def greyscale():
    succ = 0
    fail = 0
    i = 0
    print(path)
    print(len(dirs))
    for item in dirs:
        i += 1
        if item == '.DS_Store':
            continue
        if os.path.isfile(os.path.join(path, item)):
            try:
                im = Image.open(os.path.join(path, item))
                new_im = im.convert('LA')
                new_im.save(os.path.join("Media", "750GrayscalePics", "pic-gray-" + item), 'PNG', quality=90)
                print(str(i) + ": " + str(item) + " successfully greyscaled.")
                succ += 1
            except:
                print(str(i) + ": Error on item " + str(item))
                fail += 1
        else:
            print(str(i) + ": " + str(item) + " failed.")
            fail += 1
    print(str(succ) + " successfully greyscaled images.")
    print(str(fail) + " not greyscaled.")
greyscale()
