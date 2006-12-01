##-----  Here begins the program  -----##
# An anagram generator using a recursive function.
# Created by: Adam Bachman
# Date: 2005

from string import ascii_lowercase
import re
import psyco
psyco.full()
#psyco.profile()

#####################  INPUT FUNCTION  #######################
# take the original input, and remove some letters from it.
def stringRemove(orig, remove):
    for let in remove:
        orig = orig.replace(let,'',1)
    return orig
#
#####################  LEXICON FUNCTION  #######################        
def createLexicon(lexi, input):
    '''generate lexicon'''
    # foreign letter checker
    # a RegularExpression-ized string of the letters NOT in the input string.
    foreign_re = re.compile('['+''.join([x for x in ascii_lowercase if input.count(x) == 0])+']')
    #returns foreign checked dictionary.
    temp_dict = [x for x in lexi if not foreign_re.search(x)]

    new_dict = []
    for word in temp_dict:
        bad = False
        for letter in word:
            # if it doesn't have too many of any particular letter...
            if word.count(letter) > input.count(letter):
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
        temp_rslt = (temp_rslt+' '+lexi[0]).strip()
        #update the input string
        new_inpt = stringRemove(inpt, lexi[0])
        
        if len(new_inpt) == 0:
            # Branch A
            # Empty new input, full old lexicon.  We've got a winner!  
            # Print it and add it to the results.
            print temp_rslt
            rslt.append(temp_rslt)
            #get rid of the word most recently used from old lexicon and temp_rslt.
            temp_rslt = temp_rslt[:-len(lexi.pop(0))-1]
        else:
            # Full new input, full old lexicon.  Make a new lexicon.
            temp_lexi = createLexicon(lexi, new_inpt)
            if len(temp_lexi) == 0:
                # Branch B
                # Full new input, empty new lexicon.                 
                #delete temp_lexi, repeat from the while.
                del temp_lexi
                #get rid of the word most recently used from old lexicon and temp_rslt.
                temp_rslt = temp_rslt[:-len(lexi.pop(0))-1]
            else:
                # Branch C
                # Full new input, full new lexicon.  Go down one level.
                MainLoop(temp_lexi, new_inpt, rslt, temp_rslt)
                #get rid of the word most recently used from old lexicon and temp_rslt.
                temp_rslt = temp_rslt[:-len(lexi.pop(0))-1]
    return


# Testing run or real run?
test = True

if test:
#    inpt = "urinepoopanus"
#    inpt = "into"
    inpt = raw_input("Enter the phrase to be anagrammed: ")
    inpt = ''.join([l for l in inpt.lower() if ascii_lowercase.count(l)>0])
    print inpt
    dictionary = createLexicon(['inn','into','to','i','n','t','o'],inpt)
    print dictionary
    print "DONE TESTING"

else:
    inpt = raw_input("Enter the phrase to be anagrammed: ")
    inpt = ''.join([l for l in inpt.lower() if ascii_lowercase.count(l)>0])
    LEXICON = createLexicon([x.strip() for x in open('dictionary.txt')], inpt)
    RESULTS = []
    if len(LEXICON) < 1:
        print "No lexicon, what a terrible input string!"
    else:
        print "GOING!"
        # Enter the recursive anagram finding function.
        MainLoop(LEXICON, inpt, RESULTS)
        # Once it's done, RESULTS contains all our results
        print "DONE!"
        print len(RESULTS), " anagrams found"
