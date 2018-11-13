import os


def read_file(fpath):
    with open(fpath, 'r', encoding='utf-8') as rf:
        content = rf.read()
    return content


def read_pyfiles(dir_path):
    
    def _read_pyfiles(path):
        if os.path.isdir(path):
            files = os.listdir(path)
            for file in files:
                new_path = os.path.join(path, file)
                _read_pyfiles(new_path)
        elif os.path.isfile(path) and path.endswith('.py'):
            ret.add(path)
    
    ret = set()
    _read_pyfiles(dir_path)
    return ret
