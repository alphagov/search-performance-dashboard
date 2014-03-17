import os
import sys
up = os.path.dirname
sys.path.insert(0, up(up(os.path.abspath(__file__))))


if __name__ == '__main__':
    from dashboard.serve import app
    if '--debug' in sys.argv[1:]:
        app.debug = True
    app.run(host='127.0.0.1', port=4001)
