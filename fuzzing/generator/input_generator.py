from faker import Faker
import random
import sys
from fuzzing.config import REPOS_DIR, BASIC_TYPES, INFO_FORMAT, DATE_FORMAT, EXEC_DIR
import ast
from copy import deepcopy


fake = Faker()
new_tests_path = None


def _gen_arg(type_: str):
    global fake
    type_ = type_.lower()
    if type_ == 'dict':
        return fake.pydict(10, True, int)
    if type_ == 'str':
        return fake.pystr()
    if type_ == 'int':
        return fake.pyint()
    if type_ == 'float':
        return random.uniform(-sys.maxsize - 1, sys.maxsize)
    if type_ == 'list':
        return fake.pylist(10, True, int)
    if type_ == 'bool':
        return fake.pybool()
    if type_ == 'bytes':
        return fake.pystr().encode('utf-8')
    if type_ == 'tuple':
        return fake.pytuple(10, True, int)
    if type_ == 'set':
        return fake.pyset(10, True, int)


def _gen_args_type(cur_args, cur_len, args_len):
    if cur_len >= args_len:
        yield tuple(cur_args)
        return
    else:
        for bt in BASIC_TYPES:
            new_args = deepcopy(cur_args)
            new_args.append(bt)
            yield from _gen_args_type(new_args, cur_len + 1, args_len)


def _gen_args(args_types):
    return tuple(_gen_arg(type_) for type_ in args_types)


def _gen_args_list(args_len):
    args_list = []
    args_types_list = list(_gen_args_type([], 0, args_len))
    for args_types in args_types_list:
        args_list.append(_gen_args(args_types))
    return args_list


def main():
    pass


if __name__ == '__main__':
    main()
