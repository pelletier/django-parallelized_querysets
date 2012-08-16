__version_tuple__ = (0, 0, 3)
__version__ = ".".join(map(str, __version_tuple__))



def parallelized_multiple_querysets(querysets, *args, **kwargs):
    from parallelized_querysets.core import parallelized_multiple_querysets
    return parallelized_multiple_querysets(querysets, *args, **kwargs)


def parallelized_queryset(queryset, *args, **kwargs):
    return parallelized_multiple_querysets([queryset], *args, **kwargs)
