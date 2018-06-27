import requests
import IsThisLossHelper as helper
import IsThisLossBotConfig as conf
import time
import os
import IsThisLossV1 as loss
import tensorflow as tf
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

while True:
    response = requests.get('https://api.groupme.com/v3/groups/' + conf.group_id() + '/messages', params = request_params)
    if response.status_code == 200:
        response_messages = response.json()['response']['messages']

        for message in response_messages:
            pics = 0
            if ("@IsThisLossBot" in message['text']):
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
                        # Make image grayscale
                        img = img.convert('LA')
                        # Create array of image info
                        pic_array = []
                        width, height = img.size
                        data = img.load()
                        for y in range(height):
                            for x in range(width):
                                pic_array.append(data[x,y][0])
                        # TODO: Feed in picture, and make it actually predict.
                        new_sample = np.array(pic_array, dtype=np.float32)
                        predict_input_fn = tf.estimator.inputs.numpy_input_fn(
                            x={"pixels": new_sample},
                            num_epochs=1,
                            shuffle=False)
                        predictions = list(classifier.predict(input_fn=predict_input_fn))
                        predicted_classes = [p["classes"] for p in predictions]
                        for c in predicted_classes:
                            print(c)
                            post_params = { 'bot_id' : conf.bot_id(), 'text': "Cute" }
                            requests.post('https://api.groupme.com/v3/bots/post', params = post_params)
                        pics += 1
                if pics == 0:
                    text = "There aren't any pictures in your message..."
                    post_params = { 'bot_id' : conf.bot_id(), 'text': text }
                    requests.post('https://api.groupme.com/v3/bots/post', params = post_params)
            request_params['after_id'] = message['id']


    time.sleep(1)
