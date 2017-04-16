# Patch sys.path for autopoet includes
from pathlib import Path
import sys

_autopoet_path = Path('.').absolute().parent
sys.path.append(str(_autopoet_path))

import flask
import autopoet
import autopoet.poetcrawler as poetcrawler
import random

app = flask.Flask(__name__)

@app.route('/')
def index():
    # Prepare data
    poets = poetcrawler.available_poets
    poets = [(poet_id, poetcrawler.poet_name(poet_id)) for poet_id in poets]
    poets = sorted(poets, key=lambda x: x[1])

    data = {
        'poets': poets,
        'current_poet': random.choice(poets)
    }

    return flask.render_template('index.html', **data)

# Static content
@app.route('/js/<path:path>')
def serve_js(path):
    return flask.send_from_directory('js', path)

@app.route('/css/<path:path>')
def serve_css(path):
    return flask.send_from_directory('css', path)

@app.route('/fonts/<path:path>')
def serve_font(path):
    return flask.send_from_directory('fonts', path)

# Simplified run
if __name__ == '__main__':
    import sys
    import os
    import subprocess

    if 'run' in sys.argv:
        env = os.environ.copy()
        env['FLASK_APP'] = str(Path(__file__).resolve())
        print('FLASK_APP', '=', env['FLASK_APP'])

        if 'debug' in sys.argv:
            env['FLASK_DEBUG'] = 'True'

        subprocess.run(['flask', 'run'], env=env)
