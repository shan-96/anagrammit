##-----  Here begins the program  -----##
# An anagram generator using a recursive function.
# Created by: Adam Bachman
# Date: October 2005
# Update: Oct-13-2005
#   -removed regular expressions from the lexicon builder.

from string import ascii_lowercase
from time import time
import psyco
import sys
 
psyco.full()
#psyco.log()
#psyco.profile()

createCount = 0

#####################  INPUT FUNCTION  #######################
# take the original input, and remove some letters from it.
def stringRemove(orig, remove):
    for let in remove:
        orig = orig.replace(let,'',1)
    return orig

#####################  LEXICON FUNCTION  #######################        
def createLexicon(lexi, input):
    global createCount 
    createCount += 1
    '''generate lexicon'''
    #foreign = stringRemove(ascii_lowercase, input) # string of all letters not in the input
    new_dict = []
    for word in lexi:
        bad = False
        for letter in word:
            # if it doesn't have too many of any particular letter and doesn't have any foreign letters...
            if letter not in input:
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
    count = -1
    for next_word in lexi:
        count += 1 # counter to remember where in the list we are.
        
        #append the first word in the lexicon to temp_rslt
        temp_rslt += ' '+next_word
        
        #update the input string
        new_inpt = stringRemove(inpt, next_word)
        if len(new_inpt) == 0:
            # Branch A
            # Empty new input, full old lexicon.  We've got a winner!  

#            print temp_rslt
#            sys.exit(1)
            
            rslt[0] += 1
            if rslt[0] % 100 == 0:
                print rslt[0]
            rslt.append(temp_rslt)
            #get rid of the word most recently used from old lexicon and temp_rslt.
            temp_rslt = temp_rslt[:-len(next_word)-1]
        else:
            # Full new input, full old lexicon.  Make a new lexicon.
            temp_lexi = createLexicon(lexi[count:], new_inpt)
            if len(temp_lexi) == 0:
                # Branch B
                # Full new input, empty new lexicon.                 
                #get rid of the word most recently used from old lexicon and temp_rslt.
                temp_rslt = temp_rslt[:-len(next_word)-1]
            else:
                # Branch C
                # Full new input, full new lexicon.  Go down one level.
                MainLoop(temp_lexi, new_inpt, rslt, temp_rslt)
                #get rid of the word most recently used from old lexicon and temp_rslt.
                temp_rslt = temp_rslt[:-len(next_word)-1]
                

if __name__=="__main__":    
    inpt = "testmeplease"
    #    inpt = "into"
    #res_file = file('onebig_results','w')
    #inpt = raw_input("Enter the phrase to be anagrammed: ")
    #inpt = ''.join([l for l in inpt.lower() if l.isalpha()])
    s = time()    
    result = [0]
    dictionary = createLexicon([x.strip() for x in open('dictionary.txt')],inpt)
    MainLoop(dictionary,inpt,result)
    f = time()
#    for x in result:
#        res_file.write("%s\n"%x)
    print "%f seconds used."%(f-s)
    print "DONE TESTING"
    print "%i results found"%result[0]
    #for x in result[0:10]: print x
    #for x in result[-10:]: print x      
#    res_file.close()
    
    print "createLexicon was run",createCount,"times."
                
            
