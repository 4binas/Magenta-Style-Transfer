import base64
import functools
import io
import os
import uuid
from io import BytesIO

import tensorflow as tf
import tensorflow_hub as hub
from PIL import Image
import numpy as np
import re


class StyleTransfer:
  hub_handle = 'https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2'
  hub_module = hub.load(hub_handle)

  def crop_center(self, image):
    """Returns a cropped square image."""
    shape = image.shape
    new_shape = min(shape[1], shape[2])
    offset_y = max(shape[1] - shape[2], 0) // 2
    offset_x = max(shape[2] - shape[1], 0) // 2
    image = tf.image.crop_to_bounding_box(
      image, offset_y, offset_x, new_shape, new_shape)
    return image

  def load_image(self, image_url, image_size=(256, 256), preserve_aspect_ratio=True):
    image_path = re.sub('^data:image/.+;base64,', '', image_url)
    image = Image.open(BytesIO(base64.b64decode(image_path)))
    buf = io.BytesIO()
    image.save(buf, format='PNG')
    img = tf.io.decode_image(
      buf.getvalue(),
      channels=3, dtype=tf.float32)[tf.newaxis, ...]
    img = self.crop_center(img)
    img = tf.image.resize(img, image_size, preserve_aspect_ratio=True)
    return img

  def create(self, content_image_url, style_image_url):
    output_image_size = 384
    content_img_size = (output_image_size, output_image_size)
    style_img_size = (256, 256)  # Recommended to keep it at 256.

    content_image = self.load_image(content_image_url, content_img_size)
    style_image = self.load_image(style_image_url, style_img_size)
    style_image = tf.nn.avg_pool(style_image, ksize=[3, 3], strides=[1, 1], padding='SAME')

    outputs = self.hub_module(tf.constant(content_image), tf.constant(style_image))
    id = uuid.uuid4()
    path = f'./outputImages/{id}.png'
    tf.keras.preprocessing.image.save_img(path, outputs[0][0])
    return id
