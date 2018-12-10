import os
import sys
from fuzzing import config
from fuzzing.generator import testcase_generator
from fuzzing.executor.testcase_analyzer import analyse_result_from_xml, dump_testcase, distinguish_succ_and_fail
from fuzzing.executor.fuzz_executor import create_fuzz_dir, fuzz_one_func
from fuzzing.strategy import sort_by_indegree
from fuzzing.callgraph.callgraph import dump_callgraph


def main():
    repo = 'astropy'
    src_dir = 'astropy'

    repo_path = os.path.join(config.REPOS_DIR, repo, src_dir, '**', '*.py')
    graph = dump_callgraph(repo_path)
    import json
    with open('tmp.json', mode='w', encoding='utf-8') as wf:
        wf.write(json.dumps(graph, default=lambda o: o.__dict__, indent=4))

    # mod_fn_args = testcase_generator.create_test_files(repo, src_dir)
    # mod_fn_results, succ, fail = analyse_result_from_xml(os.path.join(config.EXEC_DIR, repo, 'report.xml'))
    # sys.stderr.write(f'{succ} {fail}' + os.linesep)
    # result_dict = dump_testcase(mod_fn_args, mod_fn_results)
    # succ_dict, _ = distinguish_succ_and_fail(result_dict)
    # reflect_dict_fuzz = create_fuzz_dir(repo, succ_dict)
    #
    # repo_path = os.path.join(config.REPOS_DIR, repo, src_dir, '**', '*.py')
    # result = sort_by_indegree(repo_path, reflect_dict_fuzz)
    #
    # for r in result:
    #     sys.stdout.write(repr(r) + os.linesep)

    # with multiprocessing.Pool(processes=4) as pool:
    #     results = [pool.apply_async(func=fuzz_one_func, args=(repo, fn)) for fn in os.listdir(repo)[:8]]
    #     (result.get() for result in results)


if __name__ == '__main__':
    main()
