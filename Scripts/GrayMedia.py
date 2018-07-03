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
