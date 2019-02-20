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

import requests
import IsThisLossBotConfig as conf
import time
import os
import IsThisLossV2 as loss
import numpy as np
from PIL import Image
from io import BytesIO

print("Loading bot...")

classifier, accuracy = loss.getIsThisLossModel()

request_params = conf.request_params()

#Get to the latest message
response = response = requests.get('https://api.groupme.com/v3/groups/' + conf.group_id() + '/messages', params = request_params)
if response.status_code == 200:
    response_messages = response.json()['response']['messages']
request_params['after_id'] = response_messages[0]['id']

response = response = requests.get('https://api.groupme.com/v3/groups/' + conf.group_id() + '/messages', params = request_params)

print("Ready to run!")

accuracy_string = "{:.2f}".format(accuracy)
intro_text = ("Hey there, my name is IsThisLossBotV2!\n"
              "I\'ll butt into the conversation if I think I see a Loss meme.\n"
              "Today I am " + accuracy_string + "% accurate.")
post_params = { 'bot_id' : conf.bot_id(), 'text': intro_text }
requests.post('https://api.groupme.com/v3/bots/post', params = post_params)

while True:
    response = requests.get('https://api.groupme.com/v3/groups/' + conf.group_id() + '/messages', params = request_params)
    if response.status_code == 200:
        response_messages = response.json()['response']['messages']

        for message in response_messages:
            for attachment in message['attachments']:
                if (attachment['type'] == "image"):
                    print(attachment['url'])
                    pic_response = requests.get(attachment['url'])
                    img = Image.open(BytesIO(pic_response.content))
                    # Resize image to 100x100
                    final_size = 100
                    new_image_size = (final_size, final_size)
                    img = img.resize(new_image_size, Image.ANTIALIAS)
                    new_im = Image.new("RGB", (final_size, final_size))
                    new_im.paste(img, (0, 0))
                    img = new_im
                    # Create array of image info
                    data = (np.array(img) / 255)
                    data = data.reshape(1, 100, 100, 3)
                    predicted_classes = classifier.predict(data)
                    for c in predicted_classes:
                        print(c)
                        if c[1] >= 0.5:
                            text = "Is this loss?"
                            post_params = { 'bot_id' : conf.bot_id(), 'text': text }
                            requests.post('https://api.groupme.com/v3/bots/post', params = post_params)
            request_params['after_id'] = message['id']

    time.sleep(1)
