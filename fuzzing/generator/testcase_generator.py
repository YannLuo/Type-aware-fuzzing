import os
import ast
import sys
import astor
import shutil
from ..config import REPOS_DIR
from .input_generator import _gen_args_list


new_tests_dir = '%s_tests'


def _read_py_files_from_repo(repo):
    def _travel(cur_path):
        if os.path.isdir(cur_path):
            files = os.listdir(cur_path)
            for file in files:
                if not file.startswith('_') and file != 'conftest.py' and file != 'setup.py' and 'setup_' not in file and \
                    'example' not in file and 'test' not in file:
                    path = os.path.join(cur_path, file)
                    _travel(path)
        elif os.path.isfile(cur_path) and cur_path.endswith('.py') and 'examples' + os.path.sep not in cur_path and \
                'tests' + os.path.sep not in cur_path and 'test_' not in cur_path and 'testing' + os.path.sep not in cur_path:
            py_file_list.append(cur_path)

    py_file_list = []
    repo_src_dir = os.path.join(REPOS_DIR, repo)
    _travel(repo_src_dir)
    return py_file_list


def create_test_file(fpath):
    def _get_funcdef(node):
        funcdef_list = []
        for n in node.body:
            if isinstance(n, ast.FunctionDef):
                if not n.name.startswith('_'):
                    args_len = len(n.args.args)
                    if args_len == 0 or args_len > 1:
                        continue
                    funcdef_list.append(n)
        return funcdef_list

    def _to_entry(param):
        if isinstance(param, int):
            return ast.Num(param)
        if isinstance(param, float):
            return ast.Num(param)
        if isinstance(param, bool):
            return ast.NameConstant(value=param)
        if isinstance(param, str):
            return ast.Str(s=param)
        if isinstance(param, bytes):
            return ast.Bytes(s=param)
        if isinstance(param, list):
            return ast.parse(str(param)).body[0].value
        if isinstance(param, dict):
            return ast.parse(str(param)).body[0].value
        if isinstance(param, tuple):
            return ast.parse(str(param)).body[0].value
        if isinstance(param, set):
            return ast.parse(str(param)).body[0].value

    def _gen_import(module_name):
        return ast.Import(names=[ast.alias(name=module_name, asname=None)])

    def _gen_import_from(module_name, func_name_list):
        return ast.ImportFrom(module=module_name, names=[ast.alias(name=func_name, asname=None) for func_name in func_name_list], level=0)

    def _gen_test_case(func_name):
        return ast.FunctionDef(
            name=f'test_{func_name}',
            args=ast.arguments(
                args=[ast.arg(arg=argn, annotation=None) for argn in args_names],
                vararg=None, kwonlyargs=[], kw_defaults=[], kwarg=None, defaults=[]
            ),
            body=[
                ast.Expr(ast.Call(
                    func=ast.Name(id=func_name, ctx=ast.Load()),
                    args=[ast.arg(arg=argn, annotation=None) for argn in args_names], keywords=[]))
            ],
            decorator_list=[
                ast.Call(func=ast.Attribute(value=ast.Attribute(value=ast.Name(id='pytest', ctx=ast.Load()),
                                                                attr='mark', ctx=ast.Load()),
                                            attr='parametrize', ctx=ast.Load()),
                         args=[
                             ast.Str(s=','.join(args_names)),
                             ast.List(
                                 elts=[(_to_entry(args[0]) if len(list(args)) == 1 else ast.Tuple(elts=[_to_entry(arg) for arg in args], ctx=ast.Load())) for args in args_list],
                                 ctx=ast.Load()
                             )],
                         keywords=[]
                         )],
            returns=None
        )

    root = astor.parse_file(fpath)
    funcdef_list = _get_funcdef(root)
    ret_dict = {}
    if funcdef_list:
        module = ast.Module()
        module.body = []
        module.body.append(_gen_import('pytest'))
        sep_fpath = fpath[:-3].split(os.path.sep)
        module_path = '.'.join(sep_fpath[2:])
        module.body.append(_gen_import_from(module_path, [funcdef.name for funcdef in funcdef_list]))
        for funcdef in funcdef_list:
            args = funcdef.args.args
            args_len = len(args)
            args_names = tuple(arg.arg for arg in args)
            args_list = _gen_args_list(args_len)
            module.body.append(_gen_test_case(funcdef.name))
            ret_dict[funcdef.name] = args_list
        sep_fpath = fpath[:-3].split(os.path.sep)
        test_file_name = sep_fpath[-1]
        with open(os.path.join(new_tests_dir, *(sep_fpath[3:-1]), f'test_{test_file_name}.py'), 'w', encoding='utf-8') as wf:
            wf.write(astor.to_source(module))
    return ret_dict


def create_test_files(repo, src_dir):
    global new_tests_dir
    
    def _create_new_test_dir(src_path):
        if os.path.isdir(src_path):
            sep_src_path = src_path.split(os.path.sep)[3:]
            test_subdir = os.path.join(*([new_tests_dir] + sep_src_path))
            if os.path.exists(test_subdir):
                shutil.rmtree(test_subdir)
            os.mkdir(test_subdir)
            with open(os.path.join(test_subdir, '__init__.py'), 'w', encoding='utf-8') as wf:
                wf.write('\n')
            files = os.listdir(src_path)
            for f in files:
                if not f.startswith('_') and f != 'tests' and f != 'testing':
                    new_src_path = os.path.join(src_path, f)
                    _create_new_test_dir(new_src_path)

    new_tests_dir = new_tests_dir % (src_dir, )
    src_dir_path = os.path.join(repo, src_dir)
    py_files = _read_py_files_from_repo(src_dir_path)
    _create_new_test_dir(os.path.join(REPOS_DIR, repo, src_dir))
    mod_fn_args = {}
    for f in py_files:
        sys.stderr.write(f + os.linesep)
        fn_args = create_test_file(f)
        sep_fpath = f[:-3].split(os.path.sep)
        mod = '.'.join(sep_fpath[2:])
        mod_fn_args[mod] = fn_args
    return mod_fn_args
