import os
import sys
import json
import pickle
from collections import defaultdict
from fuzzing import config
from fuzzing.generator import testcase_generator
from fuzzing.executor.testcase_executor import analyse_result_from_xml, dump_testcase, distinguish_succ_and_fail
from fuzzing.executor.fuzz_executor import fuzz_one_func
import shutil
from fuzzing.config import DRIVER_TEMP
import multiprocessing


def main():
    repo = 'numpy'
    src_dir = 'numpy'
    mod_fn_args = testcase_generator.create_test_files(repo, src_dir)
    mod_fn_results, succ, fail = analyse_result_from_xml(os.path.join(config.EXEC_DIR, repo, 'report.xml'))
    print(succ, fail)
    result_dict = dump_testcase(mod_fn_args, mod_fn_results)
    succ_dict, _ = distinguish_succ_and_fail(result_dict)
    with open('record.json', mode='w', encoding='utf-8') as wf:
        wf.write(json.dumps(succ_dict))
    c = 0
    for k in succ_dict:
        c += len(succ_dict[k])
    print(c)
    if not os.path.exists(repo):
        os.mkdir(repo)
    os.chdir(repo)
    for mod in succ_dict:
        for fn in succ_dict[mod]:
            if not os.path.exists(fn):
                os.mkdir(fn)
            os.chdir(fn)
            if not os.path.exists('inputs'):
                os.mkdir('inputs')
            os.chdir('inputs')
            for i, args in enumerate(succ_dict[mod][fn]):
                with open(f'input_{i:03}.txt', mode='w', encoding='utf-8') as wf:
                    for arg in args:
                        wf.write(f'{arg}\n')
            os.chdir('..')
            if not os.path.exists('driver.py'):
                with open('driver.py', 'w', encoding='utf-8') as wf:
                    wf.write(DRIVER_TEMP % {"mod":mod, "func":fn})
            os.chdir('..')
    os.chdir('..')

    print(os.listdir(repo)[:8])
    with multiprocessing.Pool(processes=4) as pool:
        results = [pool.apply_async(func=fuzz_one_func, args=(repo, fn)) for fn in os.listdir(repo)[:8]]
        for i in range(len(results)):
            results[i].get()


if __name__ == '__main__':
    main()
