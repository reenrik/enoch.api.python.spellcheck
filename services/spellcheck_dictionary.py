import urllib
from conf.settings import settings


class SpellCheckDictionary(object):
    words = []

    def __init__(self):
        return super(SpellCheckDictionary, self).__init__()

    @classmethod
    def fromUrl(cls, dictionaryUrl: str):
        with urllib.request.urlopen(dictionaryUrl) as f:
            word_stream = f.read()

        # split on line endings
        wordList = word_stream.decode("utf-8").splitlines()

        # convert to lowercase for standarization
        for word in wordList:
            word = word.lower().strip()

        cls.words = wordList

    @classmethod
    def fromList(cls, wordList: []):
        cls.words = wordList

    @classmethod
    def get(cls):
        return cls.words

