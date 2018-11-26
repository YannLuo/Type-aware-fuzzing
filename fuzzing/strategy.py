from .callgraph.ICall import ICall
from .callgraph.callgraph import dump_callgraph


def sort_by_indegree(repo_path, reflect_dict_fuzz):
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
    for full_name, _ in reflect_dict_fuzz.items():
        if full_name in reflect_dict_callgraph:
            result.append(reflect_dict_callgraph[full_name])
    result = filter(lambda x: x.indeg == 0, result)
    return result
