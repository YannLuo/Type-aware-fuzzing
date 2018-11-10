import os
import sys
import json
import pickle
from collections import defaultdict
from fuzzing import config
from fuzzing.generator import testcase_generator
from fuzzing.executor.testcase_analyzer import analyse_result_from_xml, dump_testcase, distinguish_succ_and_fail
from fuzzing.executor.fuzz_executor import create_fuzz_dir, fuzz_one_func
import shutil
import multiprocessing


def main():
    repo = 'numpy'
    src_dir = 'numpy'
    mod_fn_args = testcase_generator.create_test_files(repo, src_dir)
    mod_fn_results, succ, fail = analyse_result_from_xml(os.path.join(config.EXEC_DIR, repo, 'report.xml'))
    print(succ, fail)
    result_dict = dump_testcase(mod_fn_args, mod_fn_results)
    succ_dict, _ = distinguish_succ_and_fail(result_dict)
    # c = 0
    # for k in succ_dict:
    #     c += len(succ_dict[k])
    # print(c)
    create_fuzz_dir(repo, succ_dict)
    # with multiprocessing.Pool(processes=4) as pool:
    #     results = [pool.apply_async(func=fuzz_one_func, args=(repo, fn)) for fn in os.listdir(repo)[:8]]
    #     (result.get() for result in results)


if __name__ == '__main__':
    main()
