'''
threadified.py - Helper functions, and real world uses of
                 threadify.py = Threadification of ANY function! 

@contact:  python (at) AndreasKrueger (dot) de
@since:    8 Jan 2015

@license:  Never remove my name, nor the examples - and send me job offers.
@todo:     I am poor, send bitcoins: 1CV2YwBeATZfYHVZgjrgupgw5zxf1Q36CU Thx!

@requires: threadify.py,  threadify_examples.py   

@summary 

1) asyncDownload(urls, **kwargs) 
   is the first real world application. See below.
   
2) 'helper functions' give sublists of the 'threadify.py' results 
   depending on success / exception. 

Examples in 'threadify_examples.py' show many details how to use this.
'''

# for easier import:
# from threadified import *
__all__ = ["asyncDownload", 
           "dropArgs", 
           "argsWhichSuceeded", "argsWhichFailed ", 
           "dropSomeExceptions", "dropAllExceptions", "keepOnlyExceptions", 
           "dropArgs_ReturnExceptionTypes_unique"]

import threadify

import exceptions, sets
try: import urllib.request as urllib2 # for compatibility with python 3
except: import urllib2

# async URL downloader.
# 1st real life application.

def asyncDownload(urls, **kwargs):
    """Opens all urls in parallel, threaded. Finishes when all done. 
       Returns list of tuples (url, htmlpage OR exception).
       I suggest to give   timeout=10   as a kwarg.
       See urllib2, and threadify.py for details,
       and threadify_examples.py for usage."""

    def urllib2UrlopenReadClose (url, **kwargs):
        """Downloads one page, see urllib2.urlopen for more info.  
          Unfortunately urllib2 mixes not well with the 'with' statement 
          in python 2.7.5, so less pythonic than desirable. But correct.
        """
        f = urllib2.urlopen(url, **kwargs) 
        html = f.read()
        f.close()
        return html

    return threadify.getThreaded (urls, urllib2UrlopenReadClose, **kwargs)

 
# results helpers:
# extract sub-lists of the results, and arguments; 
# depending on if they threw an exception

def dropArgs (results):
    "only the results, without the identifierArgs"
    return [res for _,res in results] 

def argsWhichSuceeded (results):
    "which args lead to successful processing without throwing exception"
    return [arg for arg,res in results 
            if not isinstance(res, exceptions.Exception)]

def argsWhichFailed (results):
    "which args made the function throw an exception"
    return [arg for arg,res in results 
            if isinstance(res, exceptions.Exception)]

def dropSomeExceptions (results, exception):
    "all (arg,result) tuples omitting the exceptions of given type"
    return [(arg,res) for arg,res in results 
            if not type(res)==type(exception)]

def dropAllExceptions (results):
    "all (arg,result) tuples omitting all exceptions"
    return [(arg,res) for arg,res in results 
            if not isinstance(res, exceptions.Exception)]

def keepOnlyExceptions (results):
    "all (arg,result) tuples for all the exceptions that were thrown"
    return [(arg,res) for arg,res in results 
            if isinstance(res, exceptions.Exception)]

def dropArgs_ReturnExceptionTypes_unique (results):
    "all exception types that were thrown. Unique, each type only once."
    return list(sets.Set( [type(res) for _,res in results
                           if isinstance(res, exceptions.Exception)] ))

if __name__ == "__main__":
    print "See 'threadify_examples.py' for how this works."
    