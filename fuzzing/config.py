REPOS_DIR = 'repos'
BASIC_TYPES = ['Dict', 'str', 'int', 'float', 'bool', 'List', 'bytes', 'Tuple', 'set'][:-3]
INFO_FORMAT = '[%(levelname)s][%(asctime)s][%(pathname)s] %(message)s'
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
EXEC_DIR = 'exec_env'
DRIVER_TEMP = """
import afl, os, sys
from %(mod)s import %(func)s


def parse_input_str(input_str):
    ret = []
    for input in input_str.strip().split('\\n'):
        try:
            entry = eval(input)
        except:
            entry = input
        ret.append(entry)
    return ret


afl.init()
sys.stdin.seek(0)
input_str = sys.stdin.read()
input = parse_input_str(input_str)
%(func)s(*input)

os._exit(0)

"""