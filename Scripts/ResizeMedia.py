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

# Edited from code by John Ottenlips at https://stackoverflow.com/questions/21517879/python-pil-resize-all-images-in-a-folder

from PIL import Image
import os, sys

path = os.path.join("Media", "750RawPics")
dirs = os.listdir( path )
final_size = 100;

def resize():
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
                f, e = os.path.splitext(path+item)
                new_image_size = (final_size, final_size)
                im = im.resize(new_image_size, Image.ANTIALIAS)
                new_im = Image.new("RGB", (final_size, final_size))
                new_im.paste(im, ((final_size-new_image_size[0])//2, (final_size-new_image_size[1])//2))
                new_im.save(os.path.join("Media", "750ResizedPics", "pic-small-" + item), 'JPEG', quality=90)
                print(str(i) + ": " + str(item) + " successfully resized.")
                succ += 1
            except:
                print(str(i) + ": Error on item " + str(item))
                fail += 1
        else:
            print(str(i) + ": " + str(item) + " failed.")
            fail += 1
    print(str(succ) + " successfully resized images.")
    print(str(fail) + " not resized.")
resize()
