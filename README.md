# threadify.py = Threadification of ANY function!

### @summary 

Threading made easy! Wraps any function so that it can be run in parallel threads. Calls the wrapped function with each of the given arguments, and returns all results, once all threads have finished. Core code is very short, and easy to understand. Good examples are given. 

### @details

    resultsList = threadify.getThreaded ( identifierArgs, myFunc, **kwargs )
    
automatically **creates threads** with 

    myFunc ( arg, **kwargs )

for each 'arg' in 'identifierArgs' by threadifying it = Exceptions are caught (returned back as a result) ... and if no exception was thrown, the function result is returned back. 

'identifierArg' must be a list, the elements do not need to be unique.

'myFunc' must take exactly one argument. More arguments can be given as **kwargs.

@results 

When all threads have finished, the resulting LIST contains **tuples (identifier arg, myFunc result OR exception thrown)** with len(resultList) == len(identifierArgs).

The **'helper functions' in 'threadified.py'** extract sublists depending on success. 

@examples

**Examples in 'threadify_examples.py'** show many details how to use this.

The **first real world application** is included: an **async webpage downloader**.

- - -

@contact:  python (at) AndreasKrueger (dot) de
@since:    7 Jan 2015

@license:  Never remove my name, nor the examples - and send me job offers.
@todo:     I am poor, send bitcoins: 1CV2YwBeATZfYHVZgjrgupgw5zxf1Q36CU Thx! 

@requires: threadify_examples.py, threadified.py   
@note:     tested on Python 2.7.5

@call:      results = getThreaded ( identifierArgs, myFunc, **kwargs )
@return:    list of tuples (arg, result OR exception)

