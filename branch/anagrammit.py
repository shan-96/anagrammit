""" anagrammit.py
An anagram generator using a recursive function.
Created by: Adam Bachman
Current: 1 December 2006
Project notes at [bachman.infogami.com](http://bachman.infogami.com/anagrammer)

### Types Used

**Letter frequency dict** a dictionary containing all the letters along with their
associated letter counts.

"""

from time import time, sleep
import sys
import threading
import Queue

try:
    import psyco
    psyco.full()
except ImportError:
    pass # Sorry, no optimizations for you.

WORD_CHECK = 0
LEX_GEN = 0 

#################### Lexicon Functions ######################

def letterFrequency(instr):
    """ Create a letter frequency dictionary for a given word. """
    d = {}
    for l in instr:
        d[l]=instr.count(l)
    return d

def gen_initial_lexicon(lexi,inpt):
    """ generate initial lexicon """
    new_dict = []
    for word in lexi:
        bad = False
        for letter in word:
            if letter not in inpt:
                bad = True
                break
            elif word.count(letter) > inpt[letter]:
                bad = True
                break
        if not bad:
            new_dict.append((word, letterFrequency(word)))
    return new_dict

def word_check(word, inpt):
    """ Can inpt spell word? """
    #global WORD_CHECK
    #WORD_CHECK += 1
    for l in word[0]:
        if inpt[l] < word[1][l]:
            return False
    return True

## def gen_lexicon(lexi, inpt):
##     """Generate new lexicon."""
##     #global LEX_GEN
##     #LEX_GEN += 1
##     new_lex = [w for w in lexi]
##     lexwrd = len(lexi) - 1
##     while lexwrd >= 0:
##         if not word_check(lexi[lexwrd], inpt):
##             new_lex.pop(lexwrd)
##         lexwrd -= 1
##     return new_lex


def gen_lexicon(lexi, inpt):
   '''generate lexicon'''
   global WORD_CHECK, LEX_GEN
   LEX_GEN += 1
   new_dict = []
   for word in lexi:
       WORD_CHECK += 1
       bad = False
       for l in word[0]: 
           if inpt[l] == 0:
               bad = True
               break
           elif word[1][l] > inpt[l]:
               bad = True
               break
       if not bad:
           new_dict.append(word)
   return new_dict

#####################  MAIN FUNCTION  #######################        
## The main program loop, it calls itself once for every new word in
## an anagram.  That means if a particular anagram has eight words, 
## our max recursion depth is eight.
def mainloop(lexi, inpt, rslt, temp_rslt=[]):
    count = 0 # to remember where in the list we are.
    for next_word in lexi:
        count += 1 

        temp_rslt.append(next_word[0])

        for x in next_word[1]:
            inpt[x] -= next_word[1][x]

        if sum(inpt.values()) == 0:
            ## Branch A
            ## Empty new input, full old lexicon.  We've got a winner!  
            rslt[0] += 1
            if rslt[0] % 1000 == 0:
                print rslt[0] #, temp_rslt
            rslt.append(' '.join(temp_rslt))
            for l in temp_rslt.pop():
                inpt[l] += 1
        else:
            temp_lexi = gen_lexicon(lexi[count:], inpt)
            if len(temp_lexi) == 0:
                ## Branch B
                ## Full new input, empty new lexicon.                 
                for l in temp_rslt.pop():
                    inpt[l] += 1
            else:
                ## Branch C
                ## Full new input, full new lexicon. Go down one level
                mainloop(temp_lexi, inpt, rslt, temp_rslt)
                for l in temp_rslt.pop():
                    inpt[l] += 1
    return rslt

###
## Standard driver
###

def main(pre_inpt):
    inpt = letterFrequency(pre_inpt)
    dictionary = gen_initial_lexicon(
                  [x.strip() for x in open('dictionary.txt')],inpt)
    return mainloop(dictionary,inpt,[0])

###
## Threaded
###

def make_main():
    """ Mainloop using message queues to send and recieve messages during processing.

    Possible messages are:
        exit - stop where you are and return.
        prog - put the current progress (results so far) in the response queue.

    """
    class Messenger:
        def __init__(self):
            self._in = Queue.Queue()
            self._out = Queue.Queue()
            self.results = None

        def progress(self):
            if self.isAlive():
                self._in.put('prog')
                return self._out.get()
            elif not self.results is None:
                return str(self.results[0]) + "  Done!" 
            
        def stop(self):
            if self.isAlive():
                self._in.put('exit')
                return self._out.get()
            elif not self.results is None:
                return self.results
            
        def isAlive(self):
            return threading.currentThread().isAlive()

    messenger = Messenger()
    m_queue = messenger._in
    r_queue = messenger._out
    
    def mainloop(lexi, inpt, rslt, temp_rslt, constraints=None):
        count = 0 # to remember where in the list we are.

        try:
            if messenger.results == None:
                messenger.results = rslt
        
            message = m_queue.get(block=False)
            if message.startswith('exit'):
                if not message.endswith('0'):
                    print "Quitting, %i results total" % rslt[0]
                    r_queue.put(rslt)
                m_queue.put('exit0')
                return
            elif message == 'prog':
                r_queue.put(rslt[0])
        except:
            pass
        
        for next_word in lexi:
            count += 1 
            temp_rslt.append(next_word[0])
            for x in next_word[1]:
                inpt[x] -= next_word[1][x]
            if sum(inpt.values()) == 0:
                ## Branch A
                ## Empty new input, full old lexicon.  We've got a winner!  
                
                rslt[0] += 1
                rslt.append(' '.join(temp_rslt))
                #if rslt[0] % 1000 == 0:
                #    print rslt[0]

                # Exit before restoring input
                for l in temp_rslt.pop():
                    inpt[l] += 1
            else:
                temp_lexi = gen_lexicon(lexi[count:], inpt)
                if len(temp_lexi) == 0:
                    ## Branch B
                    ## Full new input, empty new lexicon.                 
                    for l in temp_rslt.pop():
                        inpt[l] += 1
                else:
                    ## Branch C
                    ## Full new input, full new lexicon. Go down one level
                    mainloop(temp_lexi, inpt, rslt, temp_rslt)
                    for l in temp_rslt.pop():
                        inpt[l] += 1
        return rslt
    return mainloop, messenger

def monitored(pre_inpt):
    """ Start mainloop in another thread. """
    inpt = letterFrequency(pre_inpt)
    
    dictionary = gen_initial_lexicon([x.strip() for x in open('dictionary.txt')],inpt)

    mainloop, messenger = make_main()
    
    ml = threading.Thread(target=mainloop, args=(dictionary, inpt, [0], []))
    ml.setDaemon(True)
    ml.start()
    return messenger, ml

###
## Sample Use
###

def sample_singlethreaded():
    # Prompt for input
    #inpt = raw_input("Enter the phrase to be anagrammed: ")
    #inpt = ''.join([l for l in inpt.lower() if l.isalpha()])

    # Or run straight away
    inpt = "puresoapunion"

    # Time the run
    start = time()
    #r_quant, results = monitored(inpt)
    res = main(inpt)
    r_quant, results = res[0], res[1:]
    finish = time()
    total = finish - start
    
    # Display stats
    print "   ", "-" * 20
    print "    input = %s" % inpt
    print "    results = %i" % r_quant
    print "    lexicon generations = %i" % LEX_GEN
    print "    word checks = %i" % WORD_CHECK
    print "    running time = %f" % total
    print "    "
    print "    res / sec = %f" % (r_quant / total)
    print "    lexgen / res = %i" % (r_quant != 0 and (LEX_GEN / r_quant) or 0)
    print "    wdchk / res = %i" % (r_quant != 0 and (WORD_CHECK / r_quant) or 0)
    print "   ", "-" * 20
        
    # Save to file
    print "Saving to '%s_results.txt'" % inpt
    f = file("%s_results.txt" % inpt, 'w')
    for res in results:
        print >> f, res

    f.write("%s seconds used." % total)
    f.write("%i results found" % r_quant)
    f.close()

def sample_multithreaded():
    inpt = "wellpunchmeintheface"
    com = monitored(inpt)
    sleep(2)    
    print com.progress(), '(monitored)'
    sleep(2)
    results = com.stop()
    print "final: %i" % results[0]
    for r in results[1:11]:
        print r

if __name__=="__main__":
    sample_multithreaded()
##     sample_singlethreaded()
    
    
