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

