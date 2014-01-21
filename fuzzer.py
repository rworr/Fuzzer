# Python script to generate random valid programs for a given language specification

import random, sys
from os import listdir, getcwd
from os.path import isfile, join, splitext

global ofile, ext, doingbad, didbad
print sys.argv
random.seed();
ext = ""
ws = [" ", "\t", "\n"]
grammar = []

    
class Rule:
    def __init__(self, name, rule):
        self.name = name
        self.rule = rule

    def __str__(self):
        return '[' + self.name + ', ' + self.rule + ']'

    def expand(self):
        expand(self.rule)

# Write out a random whitespace character
# using the whitespace defined in the array ws
def whitespace():
    num = random.randint(0, len(ws) - 1)
    ofile.write(ws[num])

# Lookup within the grammar array by name to retrieve a rule
def Grammar(name):
    for r in grammar:
        if r.name == name:
           return r
    return None

# Expand a literal symbol, handling a possible range
# TODO: Should use [] as in regex, not as literal (use "" as literal)
def expandLiteral(rule):
    if '-' in rule:
        num = random.randint(ord(rule[0]), ord(rule[2]))
        ofile.write(chr(num))
    else:
        ofile.write(rule)

# Remove the first sub-rule from the rule
def poprule(rule):
    rules = []
    cidx = 0
    pidx = 0
    while cidx < len(rule):
        if rule[cidx] == '-':
            rules.append(rule[pidx:cidx])
            rules.append(rule[cidx + 1:])
            cidx = len(rule)
        elif rule[cidx] == '(':
            lb = 1
            rb = 0
            while lb != rb:
                cidx += 1
                if rule[cidx] == '(':
                    lb += 1
                elif rule[cidx] == ')':
                    rb += 1
            cidx += 2
            rules.append(rule[pidx:cidx])
        elif rule[cidx] == '[':
            lb = 1
            rb = 0
            while lb != rb:
                cidx += 1
                if rule[cidx] == '[':
                    lb += 1
                elif rule[cidx] == ']':
                    rb += 1
            cidx += 1
            rules.append(rule[pidx:cidx])
        elif rule[cidx] == '{':
            lb = 1
            rb = 0
            while lb != rb:
                cidx += 1
                if rule[cidx] == '{':
                    lb += 1
                elif rule[cidx] == '}':
                    rb += 1
            split = rule[pidx+1:cidx].split('|')
            idx = random.randint(0, len(split) - 1)
            rules.append(split[idx])
            cidx += 1
        else:
            cidx += 1

        if len(rules) == 1:
            if cidx < len(rule) and rule[cidx] == '-':
            	rules.append(rule[cidx + 1:])
            cidx = len(rule)

    if len(rules) == 0:
        rules.append(rule)
    return rules

# Expands a given rule
# Begins by splitting the rule into a list of rules by examining
# characters such as '-', '()', '[]', and '{}', which organize the rule
# Then iterates over the resulting list of rules and output each rule
def expand(rule):
    rules = poprule(rule)
    exprule = rules[0]
    if exprule == '\s':
        whitespace()
    elif exprule[0] == '(':
        iters = 0
        if exprule[-1] == "*":
            iters = random.randint(0, 20)
        elif exprule[-1] == "+":
            iters = random.randint(1, 20)
        else:
            print "ERROR"
        body = exprule[1:-2]
        for i in range(0, iters):
            expand(body)
    elif exprule[0] == '[':
        expandLiteral(exprule[1:-1])
    elif Grammar(exprule) != None:
        expand(Grammar(exprule).rule)
    else:
        expand(exprule)

    if len(rules) == 2:
        expand(rules[1])
        
# Return the name of the rule from the beginning of the line
def getname(line):
    cidx = 0
    while cidx < len(line) and line[cidx] != "=" and line[cidx] not in ws:
        cidx += 1
    return [line[cidx:].lstrip().rstrip(), line[:cidx].lstrip().rstrip()]

# Create the array grammar, containing Rule objects, by reading
# each line of the specification file
def constructGrammar(grammarSpec):
    global ext
    print "Generating grammar for strings..."
    ifile = open(grammarSpec)
    first = True
    for line in ifile:
        cur = line.lstrip()
        if cur != "" and cur[0] != "#" and cur[0] != '@':
            [cur, name] = getname(cur)
            if cur == "" or cur[0:2] != "=>":
                print "ERROR: INVALID SYNTAX NEAR " + line
                return
            rule = cur[2:].lstrip().rstrip()
            grammar.append(Rule(name, rule))

# Determine which language specification is to be used
def getSpec():
    print "Scanning for languages..."
    cdir = getcwd()
    langs = [f for f in listdir(cdir) 
               if isfile(join(cdir, f)) and splitext(f)[1] == ".lang"]
    print "ID\t\tLanguage"
    for l in langs:
        print "[" + str(langs.index(l)) + "]\t\t", splitext(l)[0]
    return langs[int(raw_input("Enter language ID to generate files: "))]

# Initialize the needed global variables
def init():
    global fileSpec, ext, giter, biter
    if "-l" in sys.argv:
        fileSpec = sys.argv[sys.argv.index("-l") + 1]
    else:
        fileSpec = getSpec()

    if "-x" in sys.argv:
        ext = sys.argv[sys.argv.index("-x") + 1]
    else:
        ext = splitext(fileSpec)[0]

    constructGrammar(fileSpec)
    giter = int(raw_input("How many good files to produce?: "))
    biter = int(raw_input("How many bad files to produce?: "))

init()
print "Generating random programs..."
for i in range(0, giter):
    ofile = open('fuzz' + str(i) + '.' + ext, 'w')
    Grammar("Program").expand()

ext = "bad" + ext
for i in range(0, biter):
    ofile = open('fuzz' + str(i) + '.' + ext, 'w')
    doingbad = True
    didbad = False
    //Grammar("Program").expand()
