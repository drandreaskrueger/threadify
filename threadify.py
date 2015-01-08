'''
threadify.py - Threadification of ANY function!

@contact:  python (at) AndreasKrueger (dot) de
@since:    7 Jan 2015

@license:  Never remove my name, nor the examples - and send me job offers.
@todo:     I am poor, send bitcoins: 1CV2YwBeATZfYHVZgjrgupgw5zxf1Q36CU Thx! 

@requires: threadify_examples.py, threadified.py   

@call:      results = getThreaded(identifierArgs, myFunc, **kwargs)
@return:    list of tuples (arg, result OR exception)

@summary 

calls myFunc(arg,**kwargs) for each arg in identifierArgs by 
threadifying it: Exceptions are caught (returned back as a result),
and if no exception was thrown, the function result is returned back.

identifierArg must be a list, the elements do not need to be unique.

myFunc must take exactly one argument. 
More arguments can be given as **kwargs.

When all threads have finished, the resulting LIST  
contains tuples (identifier arg, myFunc result OR exception thrown).

The 'helper functions' in 'threadified.py' give sublists depending on success.
Examples in 'threadify_examples.py' show many details how to use this.
'''
    
# for easier import:
# from threadify import *
__all__ = ["threadify", "getThreaded", "tc"]

import threading

def threadify(resultsList, myFunc, arg, **kwargs):
    """Wraps any 'myFunc' into a threadable version.
       It calls 'myFunc(arg, **kwargs)', catching all exceptions, and 
       appends to resultsList the tuple (arg, result OR exception).
       N.B.: The function 'myFunc' must take exactly one argument, 
       which is then used in the resultsList as identifier.
       Any number of more arguments can be given as **kwargs."""
    try: 
        answer = myFunc(arg, **kwargs)
    except Exception as e:
        answer = e
    resultsList.append ((arg, answer))
        

def getThreaded(identifierArgs, myFunc, **kwargs):
    """For each arg in identifierArgs, start one thread of threadify, 
    which is then calling 'myFunc(arg, **kwargs)'.
    The identifierArgs do not need to be unique.
    If myFunc needs additional arguments, give them as **kwargs.
    Returns LIST of tuples (identifierArg, result OR exception)
    when ALL threads have finished. N.B.: Use timeouts in 'myFunc'! 
    """
    results, threads = [],[]

    for arg in identifierArgs:
        t = threading.Thread(target = threadify,
                             args   = (results, myFunc, arg), 
                             kwargs = kwargs)
        t.start()
        threads.append(t)
    
    for t in threads: t.join() # waits until all threads are finished
    return results


def tc():
    "Only an observer. Total number of active threads in this process."
    return threading.active_count()


if __name__ == "__main__":
    print "See 'threadify_examples.py' for how this works."
    print "'threadified.py' has helper functions for the results."
