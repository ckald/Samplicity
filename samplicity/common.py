import os


def pad_name(name, length, pad=' ', dir='right'):
    if dir == 'right':
        return (name + pad * length)[:length]
    else:
        return (name + pad * length)[-length:]


def wrap(text, width=80):
    """
    A word-wrap function that preserves existing line breaks
    and most spaces in the text. Expects that existing line
    breaks are posix newlines (\n).
    """
    print reduce(
        lambda line, word, width=width: '%s%s%s' % (
            line,
            ' \n'[(len(line) - line.rfind('\n') - 1 + len(word.split('\n', 1)[0]) >= width)],
            word
        ), text.split(' ')
    )


def path_insensitive(path):
    """
    Get a case-insensitive path for use on a case sensitive system.

    >>> path_insensitive('/Home')
    '/home'
    >>> path_insensitive('/Home/chris')
    '/home/chris'
    >>> path_insensitive('/HoME/CHris/')
    '/home/chris/'
    >>> path_insensitive('/home/CHRIS')
    '/home/chris'
    >>> path_insensitive('/Home/CHRIS/.gtk-bookmarks')
    '/home/chris/.gtk-bookmarks'
    >>> path_insensitive('/home/chris/.GTK-bookmarks')
    '/home/chris/.gtk-bookmarks'
    >>> path_insensitive('/HOME/Chris/.GTK-bookmarks')
    '/home/chris/.gtk-bookmarks'
    >>> path_insensitive("/HOME/Chris/I HOPE this doesn't exist")
    "/HOME/Chris/I HOPE this doesn't exist"
    """

    def _path_insensitive(path):
        """
        Recursive part of path_insensitive to do the work.
        """

        if path == '' or os.path.exists(path):
            return path

        base = os.path.basename(path)  # may be a directory or a file
        dirname = os.path.dirname(path)

        suffix = ''
        if not base:  # dir ends with a slash?
            if len(dirname) < len(path):
                suffix = path[:len(path) - len(dirname)]

            base = os.path.basename(dirname)
            dirname = os.path.dirname(dirname)

        if not os.path.exists(dirname):
            dirname = _path_insensitive(dirname)
            if not dirname:
                return

        # at this point, the directory exists but not the file

        try:  # we are expecting dirname to be a directory, but it could be a file
            files = os.listdir(dirname)
        except OSError:
            return

        baselow = base.lower()
        try:
            basefinal = next(fl for fl in files if fl.lower() == baselow)
        except StopIteration:
            return

        if basefinal:
            return os.path.join(dirname, basefinal) + suffix
        else:
            return

    return _path_insensitive(path) or path
