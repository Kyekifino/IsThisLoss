# What is Loss?

![Loss](https://cad-comic.com/wp-content/uploads/2017/03/cad-20080602-358b1.x60343.jpg)

Loss is a 2008 comic strip from the comedy gaming webcomic, Ctrl+Alt+Del by Tim Buckley. Taking a short excursion from over the top gaming-related jokes, Loss features one of the cast's main characters suffering a miscarriage. Due to its unexpected, and tonally confusing nature, Loss has become infamous as one of the most incredulous moments in webcomic history, finding its way into public perception as an [internet meme.](https://knowyourmeme.com/memes/loss) It has become popular to make references to the comic, or to take other images and arrange them much like the initial comic. Variations on this form have been taken to both ridiculous and minimalistic levels, with many arguing that Loss can be distilled down to:

I II
II L

# What is IsThisLoss?

IsThisLoss is a machine learning based approach to decipher Loss memes, training a Deep Neural Network to classify images as Loss, or not Loss. It uses data gathered from the [/r/LossEdits](https://www.reddit.com/r/lossedits/) subreddit to provide training data for Loss memes, and data gathered from the [/r/ITookAPicture](https://www.reddit.com/r/itookapicture/) subreddit to provide training data for pictures that are not Loss. This data can be replaced and saved to the existing CSV files using the scripts in the Scripts folder.

# How can I use IsThisLoss?

IsThisLoss has been built to run on a GroupMe bot, which can be configured to run on any group using GroupMe's developer kit. Provided you have Python and the necessary libraries installed, the bot should be able to run. Before running, however, one must create their IsThisLossBotConfig.py file. I didn't include my own for security reasons, however the format is as follows:

```python
def request_params():
    return {'token': 'YOUR TOKEN GOES HERE'}

def group_id():
    return "YOUR GROUP'S GROUP ID GOES HERE"

def bot_id():
    return "YOUR BOT'S BOT ID GOES HERE"

```

# Licensing

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at

https://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

# Special Thanks

Images ripped from /r/lossedits using [ripme.](https://github.com/4pr0n/ripme)

Images resized using [script by John Ottenlips.](https://stackoverflow.com/questions/21517879/python-pil-resize-all-images-in-a-folder)

CSV Files generated with reference from [James Kellas.](https://www.quora.com/How-can-my-pixel-data-from-an-image-be-outputted-into-a-CSV-file-like-this-in-Python)

Machine Learning Python code created with [reference from Google's crash course.](http://developers.google.com/machine-learning/crash-course/)

GroupMe bot made with inspiration from Stephen Waddell.

GroupMe bot made with reference to [tutorial.](http://sweb.uky.edu/~jtba252/index.php/2017/09/13/how-to-write-a-groupme-bot-using-python/)
