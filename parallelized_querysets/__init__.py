__version_tuple__ = (0, 0, 1)
__version__ = ".".join(map(str, __version_tuple__))



def parallelized_multiple_querysets(querysets, processes=None, function=None):
    from .core import parallelized_multiple_querysets
    return parallelized_multiple_querysets(querysets, processes, function)


def parallelized_queryset(queryset, processes=None, function=None):
    return parallelized_multiple_querysets([queryset], processes, function)
