# -*- coding: utf-8 -*-
import uuid
import matplotlib
matplotlib.use('Agg')
import qrcode
import iris
import iris.quickplot as qplt
import iris.plot as iplt
import matplotlib.pyplot as plt
import boto3
import urllib
from PIL import Image
import requests
from io import BytesIO
import numpy as np

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions

TEMP_IMAGE = '/tmp/image.png'
S3_BUCKET = 'informatics-pangeo-ar-plot'

class arplot(object):

    @classmethod
    def make_image(cls, cube):
        fig = plt.figure(figsize=(20, 15), frameon=False)
        iplt.pcolormesh(cube)
        plt.gca().coastlines('50m')
        plt.savefig(TEMP_IMAGE)
        img = Image.open(TEMP_IMAGE)
        area = (252, 372, 1799, 1140)
        cropped_img = img.crop(area)
        cropped_img.save(TEMP_IMAGE)

    @classmethod
    def upload_image(cls, key):
        s3 = boto3.resource('s3')
        s3.meta.client.upload_file(TEMP_IMAGE, S3_BUCKET, key, ExtraArgs={'ContentType': 'image/png'})

    @classmethod
    def make_url(cls):
        key = '{}.png'.format(str(uuid.uuid4()))
        return key, 'https://arplot.informaticslab.co.uk/' + key

    @classmethod
    def generate_qr_code(cls, url):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        url = 'https://arplot.informaticslab.co.uk/index.html?plot=' + urllib.parse.quote_plus(url)
        qr.add_data(url)
        qr.make(fit=True)

        return qr.make_image(fill_color="black", back_color="white")

    @classmethod
    def get_marker(cls):
        response = requests.get('https://arplot.informaticslab.co.uk/marker.jpg')
        return Image.open(BytesIO(response.content))

    @classmethod
    def plot(cls, cube):
        key, url = cls.make_url()
        cls.make_image(cube)
        cls.upload_image(key)
        images = [cls.generate_qr_code(url), cls.get_marker()]
        min_shape = sorted( [(np.sum(i.size), i.size ) for i in images])[0][1]
        return Image.fromarray(np.hstack([np.asarray(i.resize(min_shape).convert('RGB'))  for i in images]))

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions
