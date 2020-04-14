"""
    Current directory context manager.
"""
import os
from contextlib import contextmanager


@contextmanager
def pushd(path):
    """ A context that enters a given directory and restores the old state on exit.

        The original directory is returned as the context variable.
    """
    saved = os.getcwd()
    os.chdir(path)
    try:
        yield saved
    finally:
        os.chdir(saved)


if __name__ == "__main__":
    # Call via 'python3 python/pushd.py'
    cwd = os.getcwd()
    pydir = os.path.abspath(os.path.dirname(__file__))
    with pushd('python') as previous:
        print("changed to {!r} from {!r}".format(os.getcwd(), previous))
        assert previous == cwd
        assert os.getcwd() == pydir, "{!r} != {!r}".format(os.getcwd(), pydir)
    print("back in {!r}".format(os.getcwd()))
    assert os.getcwd() == cwd
