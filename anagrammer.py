##-----  Here begins the program  -----##
# An anagram generator using a recursive function.
# Created by: Adam Bachman
# Date: October 2005
# Update: Oct-13-2005
#   -removed regular expressions from the lexicon builder.
# Update: Nov-12-2005
#   -change from lists to deques (from collections module)

from string import ascii_lowercase
from time import time
from collections import deque
#import psyco
#psyco.full()

#####################  INPUT FUNCTION  #######################
# take the original input, and remove some letters from it.
def stringRemove(orig, remove):
    for let in remove:
        orig = orig.replace(let,'',1)
    return orig

#####################  LEXICON FUNCTIONS  #######################        
def createLexicon(lexi, input):
    '''generate lexicon'''
    foreign = stringRemove(ascii_lowercase, input) # string of all letters not in the input
    new_dict = deque()
    for word in lexi:
        bad = False
        for letter in word:
            # if it doesn't have too many of any particular letter and doesn't have any foreign letters...
            if foreign.count(letter):
                bad = True
                break
            elif word.count(letter) > input.count(letter):
                bad = True
                break
        # add it to the original lexicon
        if not bad:
            new_dict.append(word)
    return new_dict


#####################  MAIN FUNCTION  #######################        
## The main program loop, it calls itself once for every new word in
## an anagram.  That means if a particular anagram has eight words, our max
## recursion depth is eight.
def MainLoop(lexi, inpt, rslt, temp_rslt=''):
    while len(lexi) > 0:
        #append the first word in the lexicon to temp_rslt
        temp_rslt += ' '+lexi[0]
        
        #update the input string
        new_inpt = stringRemove(inpt, lexi[0])
        if len(new_inpt) == 0:
            # Branch A
            # Empty new input, full old lexicon.  We've got a winner!  
            # Print it and add it to the results.
            #print temp_rslt
            #rslt.append(temp_rslt)
            rslt[0] += 1
            if rslt[0] % 100 == 0:
                print rslt[0]
            rslt.append(temp_rslt)
            #print temp_rslt
            #get rid of the word most recently used from old lexicon and temp_rslt.
            temp_rslt = temp_rslt[:-len(lexi.popleft())-1]
        else:
            # Full new input, full old lexicon.  Make a new lexicon.
            temp_lexi = createLexicon(lexi, new_inpt)
            if len(temp_lexi) == 0:
                # Branch B
                # Full new input, empty new lexicon.                 
                #get rid of the word most recently used from old lexicon and temp_rslt.
                temp_rslt = temp_rslt[:-len(lexi.popleft())-1]
            else:
                # Branch C
                # Full new input, full new lexicon.  Go down one level.
                MainLoop(temp_lexi, new_inpt, rslt, temp_rslt)
                #get rid of the word most recently used from old lexicon and temp_rslt.
                temp_rslt = temp_rslt[:-len(lexi.popleft())-1]
    #return

if __name__=="__main__":
    # Testing run or real run?
    inpt = "urinepoopanus"
    #inpt = raw_input("Enter the phrase to be anagrammed: ")
    #inpt = ''.join([l for l in inpt.lower() if ascii_lowercase.count(l)>0])
    start = time()
    print "Initial Lex..."
    LEXICON = createLexicon([x.strip() for x in open('dictionary.txt')], inpt)
    print "GOING!"
    RESULTS = deque([0])
    MainLoop(LEXICON, inpt, RESULTS)
    # Once it's done, RESULTS contains all our results
    finish = time()
    total = finish - start
    print "DONE!"
    print RESULTS[0], "anagrams found."
    print total, "seconds used."
    

            
                
            
