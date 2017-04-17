# Patch sys.path for autopoet includes
from pathlib import Path
import sys

_autopoet_path = Path('.').absolute().parent
sys.path.append(str(_autopoet_path))

import flask
import autopoet
import autopoet.poetcrawler as poetcrawler
import autopoet.graphutils as graphutils
import autopoet.utils as utils
import random
import json

# TODO: Use JSON instead of pickle
import pickle

app = flask.Flask(__name__)

def cache_autocomplete(poet_id, cache_file):
    if cache_file.exists():
        return False
    else:
        # Load
        d = poetcrawler.get_poet(poet_id)
        text = poetcrawler.gather(*d)

        words = text.split()
        words = [word.lower() for word in words if word.isalpha()]

        graph = graphutils.graph_from_words(words)
        graph.normalize_weights()

        with cache_file.open('wb') as f:
            pickle.dump(graph, f)

        return True

def load_autocomplete(poet_id):
    cache_dir = Path('cache', 'poets')
    cache_dir.mkdir(parents=True, exist_ok=True)

    cache_file = Path(cache_dir, poet_id).with_suffix('.poet')

    cache_autocomplete(poet_id, cache_file)

    with cache_file.open('rb') as f:
        return pickle.load(f)

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

@app.route('/autocomplete/<poet>/<word>')
def autocomplete(poet, word):
    graph = load_autocomplete(poet)
    print('Looking for', word)

    if word not in graph.nodes:
        # Fuzzy search
        ratios = {w: utils.diff(w, word) for w in graph.nodes}

        ratios = [(k, ratios[k]) for k in sorted(ratios.keys(), key=ratios.get, reverse=True)]
        best_word, best_ratio = ratios[0]

        if best_ratio < 0.25:
            print('Unknown word:', word)
            print('Closest match is', best_word, 'at {0}%'.format(int(best_ratio*100)))
            return json.dumps({'error': 'word not found'}, indent=4)

        word = best_word
        print('Got closest match', word, 'at', best_ratio)

    links = graph.links_from(word)
    data = []

    for link in sorted(links, key=lambda x: x.weight, reverse=True):
        data.append({
            'word': link.to_node,
            'weight': link.weight
        })

    return json.dumps(data, indent=4)

@app.route('/load/<poet>')
def load(poet):
    load_autocomplete(poet)
    return json.dumps({'success': True}, indent=4)

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
