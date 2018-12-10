from fuzzing.config import EXEC_DIR, REPOS_DIR
from subprocess import Popen
import os
import xml.dom.minidom
from collections import defaultdict


def copy_repo_to_execdir(repo):
    src = os.path.join(REPOS_DIR, repo)
    dst = os.path.join(EXEC_DIR, repo)
    if os.path.exists(dst):
        p = Popen(f'rm -rf {dst}', shell=True, encoding='utf-8')
        p.wait()
    p = Popen(f'cp -r {src} {dst}', shell=True, encoding='utf-8')
    p.wait()


def copy_tests_to_execdir(repo):
    src = f'{repo}_tests'
    dst = os.path.join(EXEC_DIR, repo, src)
    p = Popen(f'cp -r {src} {dst}', shell=True, encoding='utf-8')
    p.wait()
    p = Popen(f'rm -r {src}', shell=True, encoding='utf-8')
    p.wait()


def prepare_execdir(repo):
    copy_repo_to_execdir(repo)
    copy_tests_to_execdir(repo)


def run_testcases(repo):
    prepare_execdir(repo)
    os.chdir(os.path.join(EXEC_DIR, repo))
    cmd = f'pytest --junitxml=report.xml {repo}_tests'
    with open('/dev/null', mode='w', encoding='utf-8') as wf:
        p = Popen(cmd, shell=True, encoding='utf-8', stdout=wf, stderr=wf)
    p.wait()
    for _ in range(2):
        os.chdir('..')


def analyse_result_from_xml(report_xml_file):
    tree = xml.dom.minidom.parse(report_xml_file)
    collection = tree.documentElement
    testcase_list = collection.getElementsByTagName('testcase')
    succ = 0
    fail = 0
    mod_fn_results = defaultdict(lambda : defaultdict(list))
    d = defaultdict(lambda : 0)
    for testcase in testcase_list:
        name = testcase.getAttribute('name')
        try:
            idx = name.index('[')
        except ValueError:
            file = testcase.getAttribute('file')
            continue
        name = name[:idx]
        classname = testcase.getAttribute('classname')
        classname = '.'.join([classname.split('.')[0].split('_')[0]] + classname.split('.')[1:])
        result = (len(testcase.childNodes) == 0)
        if not result:
            d[testcase.childNodes[0].tagName] += 1
        mod_fn_results[classname][name].append(result)
        if result:
            succ += 1
        else:
            fail += 1
    return mod_fn_results, succ, fail


def dump_testcase(mod_fn_args:dict, mod_fn_results:dict):
    ret = defaultdict(lambda : defaultdict(lambda : None))
    for k in mod_fn_results.keys():
        mod = k.split('.')
        mod = '.'.join(mod[:-1] + [mod[-1][5:]])
        if mod in mod_fn_args:
            for kk in mod_fn_results[k].keys():
                if kk[5:] in mod_fn_args[mod]:
                    ret[mod][kk[5:]] = {
                        "args": mod_fn_args[mod][kk[5:]],
                        "results": mod_fn_results[k][kk]
                    }
    return ret


def distinguish_succ_and_fail(result_dict):
    succ_dict = defaultdict(lambda : defaultdict(list))
    fail_dict = defaultdict(lambda : defaultdict(list))
    for k in result_dict:
        for kk in result_dict[k]:
            for i in range(len(result_dict[k][kk]['results'])):
                arg = result_dict[k][kk]['args'][i]
                if result_dict[k][kk]['results'][i]:
                    succ_dict[k][kk].append(arg)
                else:
                    fail_dict[k][kk].append(arg)
    return succ_dict, fail_dict
