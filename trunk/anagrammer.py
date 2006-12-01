# Version 0.  That's just ugly.

##-----  Here begins the program  -----##
from anaNewNew import Input, Lexicon, Results
from string import ascii_lowercase
import re
from time import time
import psyco
psyco.full()
#psyco.profile()


# input object
class Input:
    def __init__(self, in_string):
        '''store input string -> self.input_string and self.original. Generate anti-input
        string -> self.foreign and generate a dictionary containing each letter
        (key) and it's repetitions in the string (value) -> self.input_count
        '''
        # store the lowercase version of in_string in the the Input object
        # and create a dictionary containing the count for each letter.
        self.input_string = [x for x in in_string.lower() if x != " "]
        self.original = self.input_string
        input_letters = {}
        
        for x in self.input_string:
            if input_letters.has_key(x):
                input_letters[x] += 1
            else:
                input_letters[x] = 1
        self.input_count = input_letters
        
        # list concatenation that checks whether or not a particular letter
        # of the alphabet is in the input string and then  returns the
        # letter if it is not.  Makes the foreign string in the format
        # '[adfguz]' so that it will work with regular expressions
        self.foreign = '['+''.join([x for x in ascii_lowercase if self.input_string.count(x) < 1])+']'
        
    def update(self, recent_result):
        '''take all letters of recent_result out of input.original and change input.foreign
        and input.input_string based on the removal
        '''
        
        input_list=[x for x in self.original]
        # print " input_list is", input_list
        for y in ''.join(recent_result):
            #print "removing", y
            input_list.remove(y)
        if len(input_list) > 0:
            self.input_string = ''.join(input_list)
        else:
            return True

        input_letters = {}
        for x in self.input_string:
            if input_letters.has_key(x):
                input_letters[x] += 1
            else:
                input_letters[x] = 1
        self.input_count = input_letters 

        self.foreign = '['+''.join([x for x in ascii_lowercase if self.input_string.count(x) < 1])+']'


# lexicon object
class Lexicon:
    # contains __init__ create and lengthIsZero methods.
    # contains .level .lexicon properties
    def __init__(self, input_object, dict):
        '''creates first lexicon Lexicon.lexicon[0].  use the create method to 
        generate every later lexicon.
        '''
        self.lexicon = [[]]

        # foreign letter checker
        foreign_re = re.compile(input_object.foreign)
        #returns foreign checked dictionary.
        temp_dict = [x for x in dict if not foreign_re.search(x)]
        
        
        # letter count, where wrd is the dictionary word and let is a selected letter.
        # returns true if there are more of 'let' in the dict wrd than in the input
        # string.
        letterCount = lambda wrd, let: wrd.count(let)>input_object.input_count[let]

        for b in temp_dict:
            for c in b:
                # if it doesn't have too many of any particular letter...
                letter_count = letterCount(b,c)
                if letter_count:
                    break
            # add it to the original lexicon located in the first position of the
            # lexicon collection.
            if not letter_count:
                self.lexicon[0].append(b)


    def create(self, input_object):
        '''generate lexicon word list self.lexicon from in_obj and dict
        '''
        pre_dict = self.lexicon[-1]

        # set the next item in the main lexicon list to be an empty list.  Its index
        # should be the same as next_level.
        self.lexicon.append([])


        # foreign letter checker
        foreign_re = re.compile(input_object.foreign)
        #returns foreign checked dictionary.
        temp_dict = [x for x in pre_dict if not foreign_re.search(x)]

        # letter count, where wrd is the dictionary word and let is a selected letter.
        # returns true if there lambda ltr: ltr != ' 'are more of 'let' in the dict wrd than in the input
        # string.
        letterCount = lambda wrd, let: wrd.count(let)>input_object.input_count[let]

        for b in temp_dict:
            for c in b:
                # if it doesn't have too many of any particular letter...
                letter_count = letterCount(b,c)

                if letter_count:
                    break
            # add it to the original lexicon
            if not letter_count:
                self.lexicon[-1].append(b)

    def empty(self):
        '''return answer to "is the lexicon empty?"
        '''
        if len(self.lexicon[-1]) == 0:
            return True
        else:
            return False

    def removeLast(self):
        '''here we're going to remove the most recent result from the second to last
        lexicon, because the last lexicon came back empty.  We will always only 
        need to know about the last and second to last lexicons, even if the last is
        the second and the second to last is the original.  There is no need for "levels"
        because we can always count from the end. 
        '''
        self.lexicon[-1].pop(0)

class Results:
    def __init__(self):
        self.temp = []
        self.final = []

    def addToTemp(self, word):
        self.temp.append(word)

    def removeLast(self):
        self.temp.pop()

    def finalize(self):
        self.final.append(self.temp)







i = Input("urinepoopanus")
#i = Input("profit")
dictionary = [x.strip() for x in open('dictionary.txt')]
#input = Input("iin")
#dictionary = ['i','n','in']                                 
L = Lexicon(i, dictionary)
R = Results()

## The main program loop
s = time()
x = 0
'''
    while len(L.lexicon)>0 and L.lexicon[0] != []:
        R.addToTemp(L.lexicon[0][0])
        emptyIn = i.update(R.temp)
        if emptyIn:
            print " ".join(R.temp)
            R.finalize()
            L.removeLast()
            R.removeLast()
        else:
            ## These two commands are used to end the loop at this point.
            #R.removeLast()
            #L.removeLast()
            L.create(i)        
            if L.empty():
                #print "lexicon 2 is empty!"
                del L.lexicon[-1]
                L.removeLast()
                R.removeLast()
            else:


'''
x = 0
while len(L.lexicon)>0 and L.lexicon[0] != []:
    R.addToTemp(L.lexicon[0][0])
    emptyIn = i.update(R.temp)
    if emptyIn:
        #print " ".join(R.temp)
        print ".",
        R.finalize()
        L.removeLast()
        R.removeLast()
    else:
        ## These two commands are used to end the loop at this point.
        #R.removeLast()
        #L.removeLast()
        L.create(i)        
        if L.empty():
            #print "lexicon 2 is empty!"
            del L.lexicon[-1]
            L.removeLast()
            R.removeLast()
        else:
            
            x = 1
            while len(L.lexicon)>1 and L.lexicon[1] != []:
                R.addToTemp(L.lexicon[1][0])
                emptyIn = i.update(R.temp)
                if emptyIn:
                    #print " ".join(R.temp)
                    print ".",
                    R.finalize()
                    L.removeLast()
                    R.removeLast()
                else:
                    ## These two commands are used to end the loop at this point.
                    #R.removeLast()
                    #L.removeLast()
                    L.create(i)        
                    if L.empty():
                        #print "lexicon 2 is empty!"
                        del L.lexicon[-1]
                        L.removeLast()
                        R.removeLast()
                    else:
                        x = 2
                        while len(L.lexicon)>2 and L.lexicon[2] != []:
                            R.addToTemp(L.lexicon[2][0])
                            emptyIn = i.update(R.temp)
                            if emptyIn:
                                #print " ".join(R.temp)
                                print ".",
                                R.finalize()
                                L.removeLast()
                                R.removeLast()
                            else:
                                ## These two commands are used to end the loop at this point.
                                #R.removeLast()
                                #L.removeLast()
                                L.create(i)        
                                if L.empty():
                                    #print "lexicon 2 is empty!"
                                    del L.lexicon[-1]
                                    L.removeLast()
                                    R.removeLast()
                                else:
                                    x = 3
                                    while len(L.lexicon)>3 and L.lexicon[3] != []:
                                        R.addToTemp(L.lexicon[3][0])
                                        emptyIn = i.update(R.temp)
                                        if emptyIn:
                                            #print " ".join(R.temp)
                                            print ".",
                                            R.finalize()
                                            L.removeLast()
                                            R.removeLast()
                                        else:
                                            ## These two commands are used to end the loop at this point.
                                            #R.removeLast()
                                            #L.removeLast()
                                            L.create(i)        
                                            if L.empty():
                                                #print "lexicon 2 is empty!"
                                                del L.lexicon[-1]
                                                L.removeLast()
                                                R.removeLast()
                                            else:
                                                x = 4
                                                while len(L.lexicon)>4 and L.lexicon[4] != []:
                                                    R.addToTemp(L.lexicon[4][0])
                                                    emptyIn = i.update(R.temp)
                                                    if emptyIn:
                                                        #print " ".join(R.temp)
                                                        print ".",
                                                        R.finalize()
                                                        L.removeLast()
                                                        R.removeLast()
                                                    else:
                                                        ## These two commands are used to end the loop at this point.
                                                        #R.removeLast()
                                                        #L.removeLast()
                                                        L.create(i)        
                                                        if L.empty():
                                                            #print "lexicon 2 is empty!"
                                                            del L.lexicon[-1]
                                                            L.removeLast()
                                                            R.removeLast()
                                                        else:
                                                            x = 5
                                                            while len(L.lexicon)>5 and L.lexicon[5] != []:
                                                                R.addToTemp(L.lexicon[5][0])
                                                                emptyIn = i.update(R.temp)
                                                                if emptyIn:
                                                                    #print " ".join(R.temp)
                                                                    print ".",
                                                                    R.finalize()
                                                                    L.removeLast()
                                                                    R.removeLast()
                                                                else:
                                                                    ## These two commands are used to end the loop at this point.
                                                                    #R.removeLast()
                                                                    #L.removeLast()
                                                                    L.create(i)        
                                                                    if L.empty():
                                                                        #print "lexicon 2 is empty!"
                                                                        del L.lexicon[-1]
                                                                        L.removeLast()
                                                                        R.removeLast()
                                                                    else:
                                                                        x = 6
                                                                        while len(L.lexicon)>6 and L.lexicon[6] != []:
                                                                            R.addToTemp(L.lexicon[6][0])
                                                                            emptyIn = i.update(R.temp)
                                                                            if emptyIn:
                                                                                #print " ".join(R.temp)
                                                                                print ".",
                                                                                R.finalize()
                                                                                L.removeLast()
                                                                                R.removeLast()
                                                                            else:
                                                                                ## These two commands are used to end the loop at this point.
                                                                                #R.removeLast()
                                                                                #L.removeLast()
                                                                                L.create(i)        
                                                                                if L.empty():
                                                                                    #print "lexicon 2 is empty!"
                                                                                    del L.lexicon[-1]
                                                                                    L.removeLast()
                                                                                    R.removeLast()
                                                                                else:
                                                                                    # INSERT NEXT LEVEL HERE                                                                         del L.lexicon[-1]
                                                                                    L.removeLast()
                                                                                    R.removeLast()
                                                                        del L.lexicon[-1]
                                                                        L.removeLast()
                                                                        R.removeLast()
                                                            del L.lexicon[-1]
                                                            L.removeLast()
                                                            R.removeLast()
                                                del L.lexicon[-1]
                                                L.removeLast()
                                                R.removeLast()
                                    del L.lexicon[-1]
                                    L.removeLast()
                                    R.removeLast()
                        del L.lexicon[-1]
                        L.removeLast()
                        R.removeLast()

            del L.lexicon[-1]
            L.removeLast()
            R.removeLast()
f = time()            
print f-s,"seconds used."
print len(R.final),"anagrams found."

#for x in R.final:
#    print " ".join(x)
