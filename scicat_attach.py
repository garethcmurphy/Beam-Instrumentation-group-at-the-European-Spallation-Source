#!/usr/bin/env python3
"""attach image to scicat"""
import os
import urllib
import json

import base64
import requests


from get_api import GetApi


class ScicatAttach:
    """attach image to scicat"""
    api = ""
    url_fragment = "Datasets"
    thumbnail = ""
    file = "data/nicos_00000332.hdf"
    options = {}
    header = ""

    def __init__(self):
        api = GetApi()
        self.api = api.api
        self.token = ""

    def get_url(self):
        """get URL"""
        uri = self.api + self.url_fragment + "?access_token=" + self.token
        print(uri)
        return uri

    def get_access_token(self):
        """get access token"""
        username = "ingestor"
        with open("config.json") as json_file:
            data = json.load(json_file)
            username = data["username"]
            password = data["password"]

        token = ""

        login_url = self.api + "/Users/login"
        config = {
            "username": username,
            "password": password
        }
        print(password)
        response = requests.post(login_url, data=config)
        print(response.json())
        token = response.json()
        self.token = token["id"]

        return token["id"]

    def login(self):
        """login to scicat"""
        self.get_access_token()
        print("login")

    def base64encode(self, file):
        """base 64 encode a file"""
        file = "phs.png"
        if os.path.exists(file):
            pass
        else:
            return self.thumbnail
        self.header = "data:image/png;base64,"
        with open(file, 'rb') as image_file:
            data = image_file.read()
            image_bytes = base64.b64encode(data)
            image_str = image_bytes.decode('UTF-8')
            self.thumbnail = self.header + image_str
        return self.thumbnail

    def create_payload(self, pid, file, caption):
        """create payload"""
        encode = self.base64encode(file)
        assert isinstance(encode, str)
        payload = {
            "thumbnail": encode,
            "caption": caption,
            "datasetId": pid
        }
        # print(payload)
        return payload

    def attach(self, pid, file, caption):
        """attach image to scicat"""
        self.get_access_token()
        quote_pid = urllib.parse.quote_plus(pid)
        post_url = self.api + \
            "Datasets/" + quote_pid + "/attachments" + \
            "?access_token=" + self.token
        response = requests.delete(post_url)
        if os.path.exists(file):
            pass
        else:
            print("cannot find", file)
            return 0
        payload = self.create_payload(pid, file, caption)
        print("attach", post_url)
        response = requests.post(post_url, json=payload)
        print(response.json())


def main():
    """attach image to scicat"""
    attach = ScicatAttach()
    pid = "feji"
    file = "phs.png"
    attach.base64encode(file)
    attach.attach(pid, file)


if __name__ == "__main__":
    main()
