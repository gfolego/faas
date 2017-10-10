#!/usr/bin/python


# web.py
# Copyright 2017 Fábio Beranizo (fabio.beranizo@gmail.com)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.



import optparse
from faas import app

default_host = '0.0.0.0'
default_port = '5000'
parser = optparse.OptionParser()
parser.add_option('-H', '--host',
                  help='The hostname of the app. [default %s]' % default_host,
                  default=default_host)
parser.add_option('-P', '--port',
                  help='Port for the app. [default %s]' % default_port,
                  default=default_port)
parser.add_option('-d', '--debug', action='store_true', dest='debug')
options, _ = parser.parse_args()

app.run(debug=options.debug,
        host=options.host,
        port=int(options.port))

