# django-parallelized_querysets

Handle large Django QuerySets by spreading their execution on multiple cores
and keeping the memory usage low.

[![Build Status](https://travis-ci.org/pelletier/django-parallelized_querysets.png?branch=master)](https://travis-ci.org/pelletier/django-parallelized_querysets)


## Installation

    pip install django-parallelized_querysets


## Usage

### `parallelized_queryset(queryset, processes=None, function=None)`

Process the given `queryset` and return the result as a list.

**`proceses`**

Number of processes to create. Defaults to the number returned by
`multiprocessing.cpu_count()`.

**`function`**

Apply a function the each result. Does not apply any function by default.
The first argument is the `Process` which is calling it, and the second is the
row.

You can also pass two hooks (function that will be executed by the process at
defined times):

**`init_hook`**

Give it a function taking the `Process` as argument and it will be executed at
soon as it's created.

**`end_hook`**

Give it a function taking the `Process` as argument and it will be execute right
before the `Process` exits. If it returns a non-`None` value, it will be
appended to the results queue.

> **Note**
> 
> Each time your function returns `None`, the value won't be in the resulting
> list.


> **Note**
> 
> The order in the QuerySet won't be respected!

#### Example

Return all the `Article` objects:

    >>> from parallelized_querysets import parallelized_queryset
    >>> qs = Article.objects.all()
    >>> parallelized_queryset(qs)

Add all `Article` objects to a Redis index (assuming `Article` has
a `append_to_redis` method):

    >>> from parallelized_querysets import parallelized_queryset
    >>> qs = Article.objects.all()
    >>> parallelized_queryset(qs, function=lambda p, x: x.append_to_redis())


Do the same but on 6 processes:

    >>> from parallelized_querysets import parallelized_queryset
    >>> qs = Article.objects.all()
    >>> parallelized_queryset(qs, processes=6,
                                  function=lambda p, x: x.append_to_redis())


### `parallelized_multiple_querysets(querysets, processes=None, function=None)`

Same as `parallelized_queryset` but `querysets` is a list of QuerySets.


## Testing

    ./tests/sample/manage.py test sample


## About `Exception AssertionError: AssertionError()`

You may see the following line (multiple times) on the standard error:

    Exception AssertionError: AssertionError() in <Finalize object, dead> ignored

This is a bug in Python's garbage collector (running right after a fork), which
has been fixed in
[Python 3.3.0 alpha4](http://hg.python.org/cpython/file/59567c117b0e/Misc/NEWS#l47).

See http://bugs.python.org/issue14548 for more information on that bug.

## License

MIT (see LICENSE).
