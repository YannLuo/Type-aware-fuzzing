from .pyan.visgraph import VisualGraph
from .pyan.analyzer import CallGraphVisitor
from glob import glob
import os
import logging


def create_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.WARN)
    fh = logging.FileHandler('log.log', mode='w')
    fh.setLevel(logging.WARN)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    return logger


def dump_callgraph(repo_path: str):
    logger = create_logger()
    filenames = [fn for fn in glob(repo_path, recursive=True)]
    filenames = list(filter(lambda filename: (os.path.sep + 'tests' + os.path.sep) not in filename and (
                os.path.sep + 'testing' + os.path.sep) not in filename, filenames))
    # filenames = ['D:\\PycharmProjects\\Type-aware-fuzzing\\REPOS\\astropy\\astropy\\coordinates\\orbital_elements.py']
    visitor = CallGraphVisitor(filenames, logger=logger)
    graph = VisualGraph.dump_callgraph(visitor, logger=logger)
    return graph
