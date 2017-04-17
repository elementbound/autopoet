import time

def interval(rest):
    """
    Returns True if <rest> has passed since interval's last call
    """

    if time.clock() - interval.t_start > rest:
        interval.t_start = time.clock()
        return True
    else:
        return False

def interval_start():
    """
    Reset interval()'s counter; i.e. the next call of interval will return True no matter what
    """

    interval.t_start = -1

interval_start()

def diff(a, b):
    """
    Return similarity between two strings on a scale from [0,1]
    """

    import difflib

    sq = difflib.SequenceMatcher(a=a, b=b)
    return sq.ratio()

def clear():
    """
    Clear console.

    Currently works on Windows and Linux, throws NotImplementedError otherwise
    """

    import platform
    import os

    if platform.system() == 'Windows':
        os.system('cls')
    elif platform.system() == 'Linux':
        os.system('clear')
    else:
        raise NotImplementedError()

def readline():
    """
    Read a line from the console.

    Similar to input(), except I'm still trying to fix some error here
    """

    try:
        return input()
    except EOFError:
        return '???'

# Asyncutils?
import threading
import time

def progressbar(percent, width=80, do_print=True, endl='\r'):
    s = [' '] * width
    pstr = ' {0}% '.format(int(percent*100))

    s[0]  = '['

    plen = int((width-2) * percent)
    end = 1+plen
    s[1:end] = '=' * plen
    s[end] = '>'

    s[-1] = ']'

    pstart = int((width-len(pstr))/2)
    for i in range(0, len(pstr)):
        s[pstart+i] = pstr[i]

    s = ''.join(s)

    if do_print:
        print(s, end=endl)

    return s

def do_async(fn, callback, args=[], kwargs={}, cb_args=[], cb_kwds={}, interval=0.05):
    """
    Launch a new task to run fn(*args, **kwargs), while calling callback(*cb_args, **cb_kwds)
    repeatedly.

    Once the callback returns false, the function will wait for fn to finish
    """

    thread = threading.Thread(target=fn, args=args, kwargs=kwargs)
    thread.start()

    time.sleep(interval)
    while callback(*cb_args, **cb_kwds):
        time.sleep(interval)

    thread.join()

def async_crawl(crawler, url, callback, cb_args=[], cb_kwds={}, interval=0.05):
    """
    Shorthand to do something while the crawler is running.
    """

    cb_args.insert(0, crawler)
    cb_args.insert(1, url)

    def _run():
        crawler.crawl(url)

    return do_async(_run, callback=callback, cb_args=cb_args, cb_kwds=cb_kwds, interval=interval)

def async_crawl_progress(crawler, url, interval=0.05):
    # TODO: Crashes without *args, figure out why
    def _callback(crawler, url, *args):
        progressbar(crawler.progress)

        if crawler.busy:
            return True
        else:
            return False

    return async_crawl(crawler, url, _callback, interval=interval)

def gather_with_progress(crawler, sources, interval=0.05):
    for idx, source in enumerate(sources):
        print('[{0:<2}/{1:<2}]'.format(idx+1, len(sources)), 'Crawling', source)
        async_crawl_progress(crawler, source, interval=interval)
        print('')

    return '\n\n'.join(crawler.paragraphs)
