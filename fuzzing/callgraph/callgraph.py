from .pyan.visgraph import VisualGraph
from .pyan.analyzer import CallGraphVisitor
from glob import glob
import os


def dump_callgraph(repo_path: str):
    filenames = [fn for fn in glob(repo_path, recursive=True)]
    filenames = list(filter(lambda filename: (os.path.sep + 'tests' + os.path.sep) not in filename and (
                os.path.sep + 'testing' + os.path.sep) not in filename, filenames))
    visitor = CallGraphVisitor(filenames)
    graph = VisualGraph.dump_callgraph(visitor)
    return graph
