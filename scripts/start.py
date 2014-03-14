from dashboard.serve import app
import sys


if __name__ == '__main__':
    if '--debug' in sys.argv[1:]:
        app.debug = True
    app.run(host='0.0.0.0', port=4001)
