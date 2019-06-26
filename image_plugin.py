import os
import json
import sys
from bs4 import BeautifulSoup
import mimetypes
from loguru import logger
import uuid
import sys
import requests
import shutil

mimetypes.init()

logger.add("file_{time}.log")

class Extractor(object):

    def __init__(self):

        self.links = []
        self.images = []
        self.image_dict = {}

        self.links_file = 'links.json'
        self.images_file = 'images.json'
        self.image_dict_file = 'image_dict.json'
        
        self.rootdir = '.'
        self.types = []
        self.get_image_types()

    def get_extensions_for_type(self,general_type):
        for ext in mimetypes.types_map:
            if mimetypes.types_map[ext].split('/')[0] == general_type:
                yield ext

    def get_image_types(self):
        self.types = list(self.get_extensions_for_type('image'))
        return self

    def extract(self,content):
        soup = BeautifulSoup(content, 'lxml')
        for tag in soup.find_all('a', href=True):
            try:
                self.links.append([tag['href'], str(tag.contents[0])])
            except:
                self.links.append([tag['href'], ' '])
        return self

    def walk(self):
        for root, subdirs, files in os.walk(self.rootdir):
            for fname in files:
                if 'html' in fname:
                    with open(root + '/' + fname, 'r') as f:
                        content = f.read()
                        self.extract(content)
        return self

    def clean(self):
        for l in self.links:
            for t in self.types:
                if t in l[0]:
                    self.images.append(l)
                    break
        for i in self.images:
            print(i)
            self.image_dict[i[0]] = i[1]
        return self

    def to_json(self):
        with open(self.links_file, 'w+') as f:
            json.dump(self.links, f)
        
        with open(self.images_file, 'w+') as f:
            json.dump(self.images, f)

        with open(self.image_dict_file,'w+') as f:
            json.dump(self.image_dict, f)

        return self


class Downloader(object):

    def __init__(self, path='./', prefix=True):
        self.prefix = prefix
        self.path = path

    def download(self, url):
        try:
            response = requests.get(url, stream=True)
            if self.prefix == True:
                pre = str(uuid.uuid4()) + '_'
            elif self.prefix == False:
                pre = ''
            else:
                pre = self.prefix
            name = pre + url.split('/')[-1]
            with open(self.path + name, 'wb') as out_file:
                shutil.copyfileobj(response.raw, out_file)
            del response
        except Exception as e:
            logger.debug(str(e))
            logger.debug(url)

if __name__ == '__main__':

    # get all the links in all html files under the current folder and subfolders
    e = Extractor()
    e.walk().clean()

    # links.json : all links
    # images.json : all image links and image descriptions
    # image_dict.json : image links and image descriptions as key-value pairs
    e.to_json()

    # download all images
    # failed download attempts will be registered to the log file, if any
    d = Downloader(path='./')
    for url in e.image_dict.keys():
        d.download(url)