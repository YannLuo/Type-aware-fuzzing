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
from fuzzing.callgraph.callgraph import dump_callgraph
from fuzzing.callgraph.ICall import ICall
import sys


def main():
    repo = 'numpy'
    src_dir = 'numpy'
    mod_fn_args = testcase_generator.create_test_files(repo, src_dir)
    mod_fn_results, succ, fail = analyse_result_from_xml(os.path.join(config.EXEC_DIR, repo, 'report.xml'))
    sys.stderr.write(f'{succ} {fail}' + os.linesep)
    result_dict = dump_testcase(mod_fn_args, mod_fn_results)
    succ_dict, _ = distinguish_succ_and_fail(result_dict)
    reflect_dict_fuzz = create_fuzz_dir(repo, succ_dict)

    repo_path = os.path.join(config.REPOS_DIR, repo, src_dir, '**', '*.py')
    graph = dump_callgraph(repo_path)
    reflect_dict_callgraph = {}
    for k in graph:
        namespace, name = k.split()
        caller = reflect_dict_callgraph.setdefault(k, ICall(namespace, name, ''))
        caller.outdeg += 1
        for callee in graph[k]:
            callee = reflect_dict_callgraph.setdefault(str(callee), ICall(callee.namespace, callee.name, ''))
            callee.indeg += 1

    result = []
    for full_name, entry in reflect_dict_fuzz.items():
        if full_name in reflect_dict_callgraph:
            result.append(reflect_dict_callgraph[full_name])
    result = filter(lambda x: x.indeg == 0, result)
    for r in result:
        sys.stdout.write(repr(r) + os.linesep)

    # with multiprocessing.Pool(processes=4) as pool:
    #     results = [pool.apply_async(func=fuzz_one_func, args=(repo, fn)) for fn in os.listdir(repo)[:8]]
    #     (result.get() for result in results)


if __name__ == '__main__':
    main()
