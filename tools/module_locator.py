""" This code returns the path of the Python script executed. """
import os
import sys


def we_are_frozen():
    """ All of the modules are built-in to the interpreter, e.g., by py2exe """
    return hasattr(sys, "frozen")

def module_path():
    """ Return the path of the executed Python script. """
    encoding = sys.getfilesystemencoding()
    if we_are_frozen():
        return os.path.dirname(unicode(sys.executable, encoding))
    return os.path.dirname(unicode(__file__, encoding))
