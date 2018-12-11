from .pyan.visgraph import VisualGraph
from .pyan.analyzer import CallGraphVisitor
from glob import glob
import os


def dump_callgraph(repo_path: str, logger=None):
    filenames = [fn for fn in glob(repo_path, recursive=True)]
    filenames = list(filter(lambda filename: (os.path.sep + 'tests' + os.path.sep) not in filename and (
                os.path.sep + 'testing' + os.path.sep) not in filename, filenames))
    # filenames = ['D:\\PycharmProjects\\Type-aware-fuzzing\\REPOS\\astropy\\astropy\\convolution\\convolve.py']
    visitor = CallGraphVisitor(filenames, logger=logger)
    graph = VisualGraph.dump_callgraph(visitor, logger=logger)
    return graph
