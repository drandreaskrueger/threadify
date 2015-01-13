'''
threadify_examples.py - application of, and examples for 
                        threadify.py = Threadification of ANY function! 

@contact:  python (at) AndreasKrueger (dot) de
@since:    8 Jan 2015

@license:  Never remove my name, nor the examples - and send me job offers.
@todo:     I am poor, send bitcoins: 1CV2YwBeATZfYHVZgjrgupgw5zxf1Q36CU Thx!

@requires: threadified.py,  threadify.py   

@call:     python threadify_examples.py 
@return:   stdout (print)

@summary
           Self-explaining examples:
           1) Download many webpages in parallel. Useful!
           2) Watch threads working. While they sleep.
           
See my github For feature requests, ideas, suggestions, appraisal, criticism:
@issues https://github.com/drandreaskrueger/threadify/issues
@wiki https://github.com/drandreaskrueger/threadify/wiki 
'''

import threadify, threadified
import threading, exceptions

try: import urllib.request as urllib2 # for compatibility with python 3
except: import urllib2
import time, timeit, random

# Async Webpages Downloader
# Example 1 for how to use threadify
#
# part 1: 4 web page requests, 2 of them failing
# part 2: 100 parallel requests - compared with loading one after the other
#
# purposes: Show real life application threadified.asyncDownload()
#           and illustrate some of the 'results helper' functions

urls = ["http://duckduckgo.com",  "http://www.google.com", 
        "http://ggggggggggggggggggggle.com", "http://www.google.com/zeitgeister" ]

def cleaner(s):
    "strip whitespaces and newlines from htmlpage"
    return s.strip().replace("\n","")
    
def testAsyncDownload_resultHelpers(urls, **kwargs):
    """
    Tests with threadified webpage downloader.
    First part: illustrating some of the 'results helpers' functions.
    """

    results = threadified.asyncDownload(urls, **kwargs) # HIWT magic happens
    
    # results helper functions:
    print "The threads with these urls succeeded: " , 
    print threadified.argsWhichSuceeded (results)
    print "These urls failed: "                     , 
    print threadified.argsWhichFailed (results)
    
    print "\nThe failing urls ...            ... threw these exceptions:"
    print "\n".join( ["%33s = %s" % argres for argres 
                      in threadified.keepOnlyExceptions(results)] )
     
    print "\nThe successful urls ...", 
    results = threadified.dropAllExceptions(results)
    
    if len(results) == 0:
        print "were none. Your internet is broken?"
    else:
        print "resulted in page downloads",
        print "with these lengths, and first 80 characters:"
        print "\n".join(  ["%s (len=%5d): %s  ..." % (arg, len(res), cleaner(res)[:80]  ) 
                           for arg, res in results])
        

def testAsyncDownload_speedComparison(urls, **kwargs):
    """
    Tests with threadified webpage downloader.
    Second part: comparing speed of async (threaded) version 
                 with classical (blocking) version.
    """
    urls = urls * 6
    
    print "\nFor %d page download attempts" % len(urls), 
    s1 = t() 
    results    = threadified.asyncDownload(urls, **kwargs) 
    exceptions = threadified.keepOnlyExceptions(results)
    s1 = t() - s1
    print "(of which %d threw exceptions)" % len(exceptions)
    print "a threaded version needs %.3f seconds,"  % s1,
    
    print "while a blocking version",
    s2 = t(); counter = 0
    for url in urls:
        try:
            # classical way: blocking until retrieval done 
            f = urllib2.urlopen(url, **kwargs) 
            _ = f.read() # throw away result.
            f.close()
        except:
            counter += 1 # but ignore all problems
    print "\n(which threw %d exceptions)" % counter,
    s2 = t() - s2
    print "needs %.3f seconds." % s2
    print "That is %.1f times slower." % (s2/s1)


def testGetPagesAndAnalyze(**kwargs):
    "Tests with threadified webpage downloader."
    
    print "\n************ Example 1: WebPages Downloader ************\n"
    testAsyncDownload_resultHelpers(urls, **kwargs)
    testAsyncDownload_speedComparison(urls, **kwargs)

# End of example 1



# 6 sleepers in one room, 4 of them snoring.
# Example 2 for how to use threadify.
#
# purposes: Look into the threads while they work, and 
#           illustrate more 'results helper' functions.
#           And understand how the **kwargs work.

def r(): return random.random()
def t(): return timeit.default_timer()

def testSleepAction(arg, sleeplong=1, yell = " "):
    """Three sleep phases, together 'sleeplong' seconds, 
       interrupted by two snores at random moments.
       Throws an exception if arg==0 or arg=2.
       Returns tuple (sleep duration, good morning message).
       This is the function that will get 'threadified'."""

    createExceptions = 1/arg, 1/(arg-2)
    
    seconds = t()
    
    # two random moments for snoring:
    snores = [r(), r()]; snores.sort()
    
    time.sleep(sleeplong * snores[0] )
    print "chrrrr(%d)..." % arg,
    
    time.sleep(sleeplong * (snores[1] - snores[0]))
    print "puehhh(%d)..." % arg,
    
    time.sleep(sleeplong * (1 - snores[1]))
    wakeupMsg = "Good Morning%ssays %s" % \
                (yell, threading.current_thread().getName())
                
    seconds = t() - seconds

    # returns duration, and message:    
    return round(seconds,4), wakeupMsg


def testStartAndAnalyzeSleepThreads(numberOfSleepers, **kwargs):
    """Call 'getThreaded' to threadify 
       our 'testSleepAction',  
       creating 'numberOfSleepers' threads.
       When all ready, report the results."""
   
    # create the threads = put them all to "sleep":    
    seconds = t()
    identifierArgs = range(numberOfSleepers)
    results = threadify.getThreaded(identifierArgs,testSleepAction,**kwargs)
    print 
    seconds = t() - seconds

    # analyze the sleepers:
    
    # listen what they have to say:
    print results # a list in order of waking up, the earlybired first.
    
    # for counting the exceptions:
    E  = threadified.keepOnlyExceptions(results)
    # all TYPES of Exceptions that appeared, unique = each only once:
    ET = threadified.dropArgs_ReturnExceptionTypes_unique(results) 
    print "%d sleeper(s) could not sleep because of: %s" % \
          (len(E), ([et for et in ET])) 
     
    # throw away results of threads which threw a 'ZeroDivision' exception:
    results = threadified.dropSomeExceptions(results, 
                                             exceptions.ZeroDivisionError())
    # is a second way, easiest for omitting EVERY exception
    results = threadified.dropAllExceptions(results)
    
    # throw away the args 
    results = threadified.dropArgs (results)     
    # throw away the goodmorning message            
    sleeptimes = [res[0] for res in results]     
    # --> keep only the measured sleeptimes  
    
    print "The others' single sleeptimes were",
    print " %s seconds." % ( sleeptimes )
    print "The sum was %.4f seconds,"  % sum(sleeptimes),
    print "the maximum %.4f seconds." % max(sleeptimes)
      
    print "The whole room was awake after %.4f seconds." % ( seconds )
    
    
def testGetThreaded(numberOfSleepers = 5):
    "Two calls - once without kwargs, once with kwargs (keyword args)."
    
    print "\n************ Example 2: See threads at work. While they sleep."
    
    print "\ndefault kwargs (sleeplong=1)"
    testStartAndAnalyzeSleepThreads(numberOfSleepers) 
    
    print "\npass kwargs into each thread (sleeplong=7)"
    testStartAndAnalyzeSleepThreads(numberOfSleepers, 
                                    sleeplong=7, yell=" Vietnam ")

# End of example 2
 
def run_examples():
    print "\n************ threadify.py = Threadification of ANY function!"
    
    testGetPagesAndAnalyze()
    # testGetPagesAndAnalyze(timeout=0.01) # try this out!!
    time.sleep (5)
    
    testGetThreaded (numberOfSleepers = 6)
       
    print "\n************ The end. ************************************\n"
    print "Please send me your success stories with threadify. Enjoy your day :-)\n"
 

if __name__ == "__main__":
    run_examples()