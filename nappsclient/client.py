# This file is part of kytos-utils.
#
# Copyright (c) 2016 by Kytos Team.
#
# Authors:
#    Beraldo Leal <beraldo AT ncc DOT unesp DOT br>
#
# kytos-utils is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# kytos-utils is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Foobar.  If not, see <http://www.gnu.org/licenses/>.
#

from urllib.parse import urljoin

import json
import requests
import sys
import os

class KytosClient():
    def __init__(self, api_uri, debug=False):
        self.api_uri = api_uri
        self.debug = debug

        if self.debug:
            self.set_debug()

    def set_debug(self):
        self.debug = sys.stderr

    def request_token(self, username, password):
        endpoint = urljoin(self.api_uri, '/api/auth/')
        request = requests.post(endpoint, auth=(username, password))
        if request.status_code != 201:
            print("ERROR: %d: %s" % (request.status_code, request.reason))
            sys.exit()

        json = request.json()
        token = json['hash']
        self.set_token(token)
        return token

    def set_token(self, token):
        self.token = token

    def upload_napp(self, *args):
        endpoint = urljoin(self.api_uri, '/api/napps/')
        filename = 'kytos.json'

        if not os.path.isfile(filename):
            print("ERROR: Could not access kytos.json file.")
            sys.exit(1)
 
        with open(filename) as json_file:
            metadata = json.load(json_file)
            metadata['token'] = self.token

        print(metadata)
        request = requests.post(endpoint, json=metadata)
        if request.status_code != 201:
            print("ERROR: %d: %s" % (request.status_code, request.reason))
            sys.exit()