import flask
import jsonpickle
import re
import string
from flask_injector import inject
from api.suggestion_response import SuggestionResponse
from services.spellcheck_dictionary import SpellCheckDictionary


class SpellChecker(object):
    def __init__(self, *args, **kwargs):
            return super().__init__(*args, **kwargs)

    def spellcheck(self, word, spellcheck_dictionary: SpellCheckDictionary):
        # return 500 if an empty word parameter is passed
        if(word == ""):
            flask.Response("Must provide word to check.", status=500)

        # check if original is found
        if(word.lower() in spellcheck_dictionary.words):
            return self.ok(jsonpickle.encode(SuggestionResponse(True, []),
                           unpicklable=False))

        # standardize capitalization
        standarizedWord = self.standardize_word(word)

        # get word suggestions
        spellingSuggestions = []
        spellingSuggestions = self.get_spelling_suggestions_for_word(standarizedWord, spellcheck_dictionary)

        # get 2nd depth word suggestions
        spellingSuggestions = self.get_spelling_suggestions(spellingSuggestions, spellcheck_dictionary)
        spellingSuggestions = list(set(spellingSuggestions))

        if(not spellingSuggestions):
            return self.not_found("")

        # return list of hits
        resp = SuggestionResponse(False, spellingSuggestions)
        return self.ok(jsonpickle.encode(resp, unpicklable=False))
    
    # returns HTTP 200 with specified body
    @staticmethod
    def ok(body):
        return flask.Response(body,
                              status=200,
                              mimetype="application/json")

    # returns HTTP 404 with specified body
    @staticmethod
    def not_found(body):
        return flask.Response(body,
                              status=404,
                              mimetype="application/json")
    
    # standardizes the word by removing uppercasing and letter sequences > 3
    @staticmethod
    def standardize_word(word):
        # standardize capitalization
        standardizeWord = word.lower()

        # standardize any patterns of 3 or more characters to 2 of the same
        standardizeWord = re.sub(r"((\w)\2{2,})", r'\2\2', standardizeWord)

        return standardizeWord
    
    # gets suggestions for a list of words
    @classmethod
    def get_spelling_suggestions(cls, words, spellcheck_dictionary: SpellCheckDictionary):
        suggestions = []
        for word in words:
            suggestions = suggestions + cls.get_spelling_suggestions_for_word(word, spellcheck_dictionary)
        
        return suggestions

    # gets spelling suggestions for a word
    @classmethod
    def get_spelling_suggestions_for_word(cls, word, spellcheck_dictionary: SpellCheckDictionary):
        suggestions = []
        # get words that contain characters removed
        removedWords = cls.get_removed_words(word)

        # get words that where a letter is flipped
        flippedWords = cls.get_flipped_words(word)

        # get words that a letter is replaced
        replacedWords = cls.get_replaced_words(word)

        # get word where a letter is inserted
        insertedWords = cls.get_inserted_words(word)

        suggestions = removedWords + flippedWords + replacedWords + insertedWords
        distinctSuggestions = list(set(suggestions))

        # check dictionary for hits   
        finalSuggestions = []
        for distinctSuggestion in distinctSuggestions:
            if(distinctSuggestion in spellcheck_dictionary.words):
                finalSuggestions.append(distinctSuggestion)

        return finalSuggestions

    # returns a list of candidate words with one character removed
    @staticmethod
    def get_removed_words(word):
        removedWords = []
        if(len(word) > 0):
            for i in range(len(word) + 1):
                removedWord = word[:i] + word[i+1:]
                removedWords.append(removedWord)

        return removedWords

    # returns a list of candidate words with one character flipped
    @staticmethod
    def get_flipped_words(word):
        splitWords = []
        flippedWords = []
        if(len(word) > 0):
            for i in range(len(word) + 1):
                splitWords.append((word[:i], word[i:]))
            for splitLeft, splitRight in splitWords:
                if(len(splitRight) > 1):
                    flippedWord = splitLeft + splitRight[1] + splitRight[0] + splitRight[2:]
                    flippedWords.append(flippedWord) 

        return flippedWords

    # returns a list of candidate words with one character replaced
    @staticmethod
    def get_replaced_words(word):
        splitWords = []
        replacementWords = []
        alphabet = string.ascii_lowercase
        if(len(word) > 0):
            for i in range(len(word) + 1):
                splitWords.append((word[:i], word[i:]))
            for splitLeft, splitRight in splitWords:
                if(splitRight):
                    for letter in alphabet:
                        replacedWord = splitLeft + letter + splitRight[1:]
                        replacementWords.append(replacedWord)

        return replacementWords

    # returns a list of candidate words with one character inserted
    @staticmethod
    def get_inserted_words(word):
        splitWords = []
        insertedWords = []
        alphabet = string.ascii_lowercase
        if(len(word) > 0):
            for i in range(len(word) + 1):
                splitWords.append((word[:i], word[i:]))
            for splitLeft, splitRight in splitWords:
                for letter in alphabet:
                        insertedWord = splitLeft + letter + splitRight
                        insertedWords.append(insertedWord)

        return insertedWords        

class_instance = SpellChecker()
