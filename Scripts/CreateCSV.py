# Written using reference from James Kellas at https://www.quora.com/How-can-my-pixel-data-from-an-image-be-outputted-into-a-CSV-file-like-this-in-Python

from PIL import Image
import os, sys

def CreateCSV(csv_type):
    path = os.path.join("Data", "NonConvolutionalGray", csv_type)
    dirs = os.listdir( path )
    i = 0
    succ = 0
    with open(csv_type + 'DataNCG.csv', 'w+') as f:
        for item in dirs:
            i += 1
            try:
                image = Image.open(os.path.join(path, item))
                if item.startswith("pic-"):
                    f.write('0')
                else:
                    f.write('1')
                width, height = image.size
                data = image.load()
                for y in range(height):
                    for x in range(width):
                        f.write(',' + str(data[x,y][0]))
                f.write('\n')
                succ += 1
                print(str(i) + ": " + str(item) + " successfully written.")
            except:
                print(str(i) + ": Error on " + str(item) + "!")
    print(csv_type + " data complete!")
    print(str(succ) + " successful data additions!")

CreateCSV("Training")
CreateCSV("Test")
