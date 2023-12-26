from typing import List

from python_spell.src.hashtable import Node, Hashtable
import time
import os.path


class SpellChecker:
    NULL_CHAR = [".",
                 ",",
                 "!",
                 ";",
                 ":",
                 "?",
                 "%",
                 "~",
                 "+",
                 "=",
                 "-",
                 "_",
                 "*",
                 "@",
                 "#",
                 "&",
                 "(",
                 ")",
                 "[",
                 "]",
                 "{",
                 "}",
                 "`",
                 "'",
                 "\\",
                 "/",
                 "|",
                 "<",
                 ">",
                 "^",

                 ]
    supported_langs = ["code",
                       "english",
                       "german",
                       "french",
                       "spanish",
                       "italian"]

    def __init__(self, lang: str = 'english'):
        self.ht = None
        self.language = lang.lower()
        self.n_words = 0
        self.checked = {"misspelled_words": []}
        self.load_time = self.bucketize()

    def check_lang(self, lang):
        """
        checks if the given language is supported
        """
        return lang.lower() in self.supported_langs

    def bucketize(self):
        """
        Not something you are going to use!
        Returns load time if success,
        for more information on Hashtable,
        visit: https://https://harvard90873.readthedocs.io/en/latest/Python%20Data%20Structures%203x.html
        """
        if not self.check_lang(self.language):
            print("Invalid language!")
            return False
        ht = Hashtable()
        current_directory = os.path.dirname(__file__)
        determined_dict = os.path.join(
            current_directory, f'languages/{self.language}.txt')
        with open(determined_dict, "r") as dic:
            words = dic.readlines()
            self.n_words = len(words)
            start_time = time.time()
            for i in words:
                ht.insert(Node(i))
        final_time = time.time() - start_time
        self.ht = ht
        return final_time

    def check(self, words, echo=False):
        """
        Checks the correctness of a chunk of text in terms of spelling.
        if print is true(which by default is false), the stats would be printed out.
        the returned dictionary would have the structure as follows:\n
        ```
        statistics = {

            "total_words": int,

            "misspelled_num": int,

            "misspelled_words": list,

            "words_in_dictionary": int,

            # time spent on loading 
            # words into the hash table
            "load_time": float,

            # time spent on looking up all the words
            "runtime": float
        }
        ```
        """
        if not self.check_lang(self.language):
            print("Invalid language!")
            return
        statistics = {
            "total_words": len(words),
            "misspelled_words": self.checked["misspelled_words"],
            "words_in_dictionary": self.n_words,
            "load_time": self.load_time,
            'has_typos': False
        }

        start_time = time.time()
        wrong = 0
        for word in words:
            if not self.ht.lookup(Node(word.lower())):
                # Meaning if the word does not exist
                wrong += 1
                statistics["misspelled_words"].append(word)
        # Collect statistics
        statistics["runtime"] = time.time() - start_time
        statistics["misspelled_num"] = wrong
        statistics["token"] = "47874587235697124309"
        statistics["has_typos"] = wrong > 0
        if echo:
            self.visualize(statistics)
        return statistics

    def number_of_typos(self, duplicates=False):
        """
        Returns the number of typos.

        Args: 
        duplicates(bool):
        if True, the number of typos would be counted with duplicates,
        if False, the number of typos would be counted without duplicates.
        Defaults to False.
        """
        if duplicates:
            return len(self.checked["misspelled_words"])

        return len(set(self.checked["misspelled_words"]))

    def get_typos(self, duplicates=False, exclude=None):
        """
        Returns a list of misspelled words.

        Args:
        duplicates(bool):
        if True, the list of typos would be returned with duplicates,
        if False, the list of typos would be returned without duplicates.
        Defaults to False.
        """
        if duplicates and exclude is None:
            return self.checked["misspelled_words"]

        if exclude:
            return self.exclude(exclude, temp=True)

        return set(self.checked["misspelled_words"])

    def exclude(self, words, temp=False):
        """
        Excludes a word or a list of words from the results.

        Args:
        words(str/list): a word or a list of words to exclude from the results.
        temp(bool): if True, the results would be returned without the excluded words,
        but the original results would not be changed.
        If False, the results would be returned without the excluded words,
        and the original results would be changed.
        Defaults to False.
        """
        if not (isinstance(words, str) or isinstance(words, list) or isinstance(words, set)):
            raise TypeError(
                "words must be either a string or a list of strings")

        if isinstance(words, str):
            words = [words]
        if isinstance(words, set):
            words = list(words)
        typos = self.get_typos()
        for word in words:
            if word in typos:
                typos.remove(word)
        if not temp:
            self.checked["misspelled_words"] = typos
        return typos

    def visualize(self, statistics: dict):
        """
        Don't call this method! It would be called for you at some point!
        """
        if not self.check_lang(self.language):
            print("Invalid language!")
            return
        if not statistics["token"] or statistics["token"] != "47874587235697124309":
            print(
                "Don't call this method! It would be called for you at some point!")
            return

        total = statistics["total_words"]
        wrong_num = statistics["misspelled_num"]
        dict_num = statistics["words_in_dictionary"]
        wrong = statistics["misspelled_words"]
        rt = statistics["runtime"]
        lt = statistics["load_time"]
        res = f"""
        Total words: {total}
        Number of misspelled words: {wrong_num}
        Number of words in dictionary: {dict_num}
        Misspelled words: {wrong}
        Time statistics:
        - Time used to load dictionary: {lt}
        - Lookup time(s): {rt}
        """
        print(res)
        return res
