from collections import namedtuple
from itertools import repeat

import gzip
import os
import io
import json
import re
import string
import sys
import multiprocessing as mp

##############################################################################
############### Run through all folders ######################################
##############################################################################

def run_all(path, condition, key="text", strip=True, key_out="None"):
    """This will allow to run all the directories from a path"""
    for root, dirs, files in os.walk(path):
        for i in dirs:
            fanout_gzworker(os.path.join(root, i), condition, key, strip, key_out)

##############################################################################
###################### Fanout Function #######################################
##############################################################################

def fanout_gzworker(path, condition, key="text", strip=True, key_out="None"):
    """Create pool to extract .gz giles
    and create a file where all the filtered tweets will be in JSON format,
    separated by a newline"""
    my_files = []
    big_buffer = []
    for root, dirs, files in os.walk(path):
        for i in files:
            if i.endswith(".gz"):
                my_files.append(os.path.join(root, i))

    pool = mp.Pool(min(mp.cpu_count(), len(my_files)))
    big_buffer = (pool.starmap(gzworker, zip(my_files, repeat(condition),
                                             repeat(key), repeat(strip)),
                               chunksize=1))
    pool.close()
    saveInfo(big_buffer, 'Dump/' + os.path.basename(path) + '.txt', key_out)

##############################################################################
###################### Worker Function #######################################
##############################################################################

def gzworker(fullpath, condition, key="text", strip="True"):
    """Worker opens one .gz file"""
    print('Opening {}'.format(fullpath))
    buffer = []
    with gzip.open(fullpath, 'rb') as infile:
        decoded = io.TextIOWrapper(infile, encoding='utf8')
        for _line in decoded:
            if _line.strip() != "":
                json_data = _line.split('|', 1)[1][:-1]
                result = tweet_filter(json.loads(json_data), condition,
                                      key, strip)
                if result:
                    buffer.append(result)
    print('Closing {}'.format(fullpath))
    return buffer

##############################################################################
###################### Filter Function #######################################
##############################################################################

def tweet_filter(tweet_obj, condition, key="text", strip="True"):
    """Will return the tweet object if the conditions are met (in the text only)"""

    if key in tweet_obj:
        if strip:
            text = strip_all_entities(strip_links(tweet_obj[key]))
        else:
            text = tweet_obj[key]
    else:
        print("Not a valid key (" + key + ")")
        sys.exit(1)

    if evaluate_condition(text, parse_condition(tokenize_condition(condition))):
        return tweet_obj
    else:
        return None

##############################################################################
############### Function to remove url/#/@ from text for filter ##############
##############################################################################

def strip_links(text):
    """Will remove the links from the text"""
    link_regex = re.compile('((https?):((//)|(\\\\))+([\w\d:#@%/;'
                            '$()~_?\+-=\\\.&](#!)?)*)', re.DOTALL)
    links = re.findall(link_regex, text)
    for link in links:
        text = text.replace(link[0], ', ')
    return text

def strip_all_entities(text):
    """Will remove the tags and hashtags from the text"""
    entity_prefixes = ['@', '#']
    for separator in string.punctuation:
        if separator not in entity_prefixes:
            text = text.replace(separator, ' ')
    words = []
    for word in text.split():
        word = word.strip()
        if word:
            if word[0] not in entity_prefixes:
                words.append(word)
    return ' '.join(words)

##############################################################################
############### Function to save whatever we want from the tweet #############
##############################################################################

#TODO Function that will save whatever we want from the tweet
def saveInfo(big_buffer, path="Dump/save.txt", key_out="None"):
    """Will save the selected output key in the selected path in the selected
    type output"""
    if key_out=="None":
        with open(path, 'w') as _file:
            for i in big_buffer:
                for j in i:
                    json.dump(j, _file)
                    _file.write('\n')
    else:
        with open(path, 'w') as _file:
            for i in big_buffer:
                for j in i:
                    json.dump(j[key_out], _file)
                    _file.write('\n')

##############################################################################
###################### Tokenizer #############################################
##############################################################################

# Regular expression matching a token (group 1) or an error (group 2).
_TOKEN_RE = re.compile(r'\s*(?:([()*]|\w+\b)|(\S))')

# Token representing the end of the input.
TOKEN_END = '<end of input>'

def tokenize_condition(_condition):
    """Generate the tokens in the _condition .

    >>> list(tokenize_condition("((dog OR cat) AND *Horse*)"))
    ['(', '(', 'dog', 'OR', 'cat', ')', 'AND', '*', 'Horse', '*', ')', '<end of input>']

    """
    for token, error in _TOKEN_RE.findall(_condition):
        if error:
            raise SyntaxError("unexpected character {!r}".format(error))
        yield token
    yield TOKEN_END

##############################################################################
###################### Parser ################################################
##############################################################################

# Binary operation with left operand, operator and right operand.
BinOp = namedtuple('BinOp', 'left op right')

# Ignore case when matching against body.
IgnoreCase = namedtuple('IgnoreCase', 'body')

def parse_condition(tokens):
    """Parse a condition given by an iterator of tokens, and return a
    parse tree.

    >>> tokens = tokenize_condition("((dog OR cat) AND *Horse*)")
    >>> parse_condition(tokens)
    BinOp(left=BinOp(left='dog', op='OR', right='cat'), op='AND', right=IgnoreCase(body='Horse'))

    """
    token = next(tokens)           # The current token.

    def error(expected):
        """Current token failed to match, so raise syntax error."""
        raise SyntaxError("Expected {} but found {!r}"
                          .format(expected, token))

    def match(*valid_tokens):
        """If the current token is found in valid_tokens, consume it
        and return True. Otherwise, return False."""
        nonlocal token
        if token in valid_tokens:
            token = next(tokens)
            return True
        else:
            return False

    def term():
        """term ::= ( binop ) | * binop * | WORD"""
        if match('('):
            tree = binop()
            if match(')'):
                return tree
            else:
                error("')'")
        elif match('*'):
            tree = binop()
            if match('*'):
                return IgnoreCase(tree)
            else:
                error("'*'")
        elif token in (')', 'AND', 'OR'):
            error("term")
        else:
            tok = token
            match(token)
            return tok

    def binop():
        """binop ::= term | term OR term | term AND term"""
        left = term()
        _op = token
        if match('AND', 'OR'):
            right = term()
            return BinOp(left, _op, right)
        else:
            return left

    tree = binop()
    if token != TOKEN_END:
        error("end of input")
    return tree

##############################################################################
###################### Evaluation ############################################
##############################################################################


def evaluate_condition(text, tree):
    """Return true if the expression given by the parse tree matches the text.

    >>> tokens = tokenize_condition("((dog OR cat) AND *Horse*)")
    >>> tree = parse_condition(tokens)
    >>> evaluate_condition("horse", tree)
    False
    >>> evaluate_condition("cat on a horse", tree)
    True
    >>> evaluate_condition("horse with a dog", tree)
    True

    """
    if isinstance(tree, str):
        return bool(re.search(tree, text))
        # search for tree in text, ignoring case if ignorecase=True
    elif isinstance(tree, BinOp):
        left = evaluate_condition(text, tree.left)
        right = evaluate_condition(text, tree.right)
        if tree.op == "OR":
            return left or right
        elif tree.op == "AND":
            return left and right
        # evaluate tree.left (and maybe tree.right) recursively; apply op
    elif isinstance(tree, IgnoreCase):
        return bool(re.search(tree.body, text, re.IGNORECASE))
        # evaluate tree.body, passing ignorecase=True
    else:
        raise SyntaxError("Something went wrong bra")
        # raise an error
