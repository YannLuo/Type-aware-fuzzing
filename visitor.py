import ast
import os
import astor
import sys

from fuzzing.utils.reader import read_file, read_pyfiles
from fuzzing.config import REPOS_DIR


def collect_callees(node):

    class CalleeVisitor(ast.NodeVisitor):
        
        def visit_Call(self, node):
            if isinstance(node.func, ast.Name):
                callees.add(node.func.id)
                ast.NodeVisitor.generic_visit(self, node)
    
    if isinstance(node, ast.FunctionDef):
        callees = set()
        for n in node.body:
            cle_visitor = CalleeVisitor()
            cle_visitor.visit(n)
        return callees
    else:
        raise Exception(f'Node type is {type(node.body[0])} rather than ast.FunctionDef.')


def main():
    repo = 'numpy'
    src_dir = 'numpy'
    pyfiles = read_pyfiles(os.path.join(REPOS_DIR, repo, src_dir))
    for file in pyfiles:
        root = astor.parse_file(os.path.join('repos', 'numpy', 'numpy', 'polynomial', 'polynomial.py'))
    # root = astor.parse_file('test.py')
    # for node in root.body:
    #     if isinstance(node, ast.FunctionDef):
    #         callees = collect_callees(node)
    #         print(node.name, callees)

if __name__ == '__main__':
    main()
