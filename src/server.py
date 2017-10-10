#!/usr/bin/python
# -*- coding: utf-8 -*-


# server.py
# Copyright 2017
#     Fábio Beranizo (fabio.beranizo@gmail.com)
#     Guilherme Folego (gfolego@gmail.com)
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



# Definitions
HOST='0.0.0.0'
PORT=5000


import sys
import argparse
from api import app


def parse_args(argv):
    parser = argparse.ArgumentParser(
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-H', '--host', type=str, default=HOST,
                            help='input server host')
    parser.add_argument('-P', '--port', type=int, default=PORT,
                            help='input server port')
    parser.add_argument('-d', '--debug', action='store_true',
                            help='activate debug mode')

    args = parser.parse_args(args=argv)
    return args


# Main
def main(argv):

    # Parse arguments
    args = parse_args(argv)
    if args.debug: print(args)

    app.run(host=args.host, port=args.port,
            debug=args.debug)

if __name__ == "__main__":
    main(sys.argv[1:])

