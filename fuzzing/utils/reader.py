def read_file(fpath):
    with open(fpath, 'r', encoding='utf-8') as rf:
        content = rf.read()
    return content