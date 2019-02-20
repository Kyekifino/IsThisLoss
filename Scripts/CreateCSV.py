# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Written using reference from James Kellas at https://www.quora.com/How-can-my-pixel-data-from-an-image-be-outputted-into-a-CSV-file-like-this-in-Python

from PIL import Image
import os, sys
import numpy as np

def CreateCSV():
    path = os.path.normpath(os.path.join(os.getcwd(), "..", "Data", "ConvolutionalColor"))
    dirs = os.listdir( path )
    i = 0
    succ = 0
    with open('DataCC.csv', 'w+') as f:
        for item in dirs:
            i += 1
            try:
                image = Image.open(os.path.join(path, item))
                print(str(i) + ": " + str(item) + " successfully written.")
                if item.startswith("pic-"):
                    f.write('0')
                else:
                    f.write('1')
                pic_data = np.array(image).flatten()
                for datum in pic_data:
                    f.write(',' + str(datum))
                f.write('\n')
                succ += 1
                print(str(i) + ": " + str(item) + " successfully written.")
            except Exception as err:
                print("Error {0}".format(str(err)))
                print(str(i) + ": Error on " + str(item) + "!")
                quit()
    print("Data complete!")
    print(str(succ) + " successful data additions!")

CreateCSV()
