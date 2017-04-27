# Autopoet #

*Autocorrect, now with poetry!*

Autopoet is in part a series of web crawler classes that crawl certain sites for freely available
literature, grouped by author. Since literature might come from different sites, multiple types
of crawler classes are available.  
See ``autopoet.poetcrawler``.

The second step is to 'read' all the accumulated text, and try to give reasonable guesses about
which word follows which. This is done by creating a graph from unique words. The graph's edges
( or, as the source alls it, links ) are built from word-pair occurences in the input text.
These edges also have weights - for more common word-pairs, the links are stronger.  
See ``autopoet.graph`` and ``autopoet.graphutils``.

The third stage is to present this as a user interface. This is done by running a small web
server with Flask on the user's machine. The website uses AJAX to load data from the server.
As the user is typing, the server is constantly queried for suggestions on what the next word
could be. To make this process a bit more performant, graphs are cached for each author. There
is certainly room for improvement here.  
See the ``site`` directory.

## Dependencies ##

The only dependency is [Flask](http://flask.pocoo.org/). You can get it through pip:

``pip install flask``

## Running ##

### Live demo ###

If you just want to see Autopoet in action, try [this](http://elementbound.pythonanywhere.com/).

Hosted by [pythonanywhere](https://www.pythonanywhere.com).

### Demos ###

Autopoet includes a few demos to show off each stage. The demos can be run by executing
the autopoet module:

```
$ py autopoet
usage: autopoet [-h] [-p {kosztolányi,radnóti,petőfi,örkény,tóth}]
                {wordstats,autosuggest}
autopoet: error: the following arguments are required: demo
```

**Windows users:** Before running, make sure to set your codepage to Unicode (65001), otherwise
some demos can and will crash. The code will warn about it, and try to set the codepage, but
it is still prone to crashing. Just exit and run the demo again.

### Site ###

The site is a Flask app, so if you know how to run that, you are set.

However, it can also be run through the script itself. From the site's directory, say:

```
$ py main.py run
FLASK_APP = D:\dev\python\autopoet\site\main.py
 * Serving Flask app "main"
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

## Language ##

Currently, only a few Hungarian authors are included. Attempts have been made to include English
literature too, but I have failed to find some easy to crawl sources. All suggestions are welcome!

## License ##

Autopoet is licensed under the GNU GPL v3 license. See [LICENSE](LICENSE) for more details.
