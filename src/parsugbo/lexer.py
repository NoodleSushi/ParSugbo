from cebdict import dictionary
from cebstemmer import stemmer
from .tokens import *
from .literals import *

###############################################################################
#                                                                             #
#  LEXER                                                                      #
#                                                                             #
###############################################################################

class Token(object):
    def __init__(self, type: list[str], value: str | int):
        self.type = type
        self.value = value

    def __str__(self):
        """String representation of the class instance.
        Examples:
            Token(NUMBER, 3)
            Token(PLUS, '+')
            Token(MUL, '*')
        """
        return "Token({type}, {value})".format(type=self.type, value=repr(self.value))

    def __repr__(self):
        return self.__str__()

RESERVED_WORDS = {
    "MGA": Token([TOKEN_MGA], "mga"),
    "NGA": Token([TOKEN_NGA], "nga"),
    "IKA-": Token([TOKEN_IKA], "ika-"),
    "NIAGING": Token([TOKEN_NIAGING], "niaging"),
    "SUNOD": Token([TOKEN_SUNOD], "sunod"),
    "KARONG": Token([TOKEN_KARONG], "karong"),
}

class Lexer(object):
    def __init__(self, text: str):
        # client string input, e.g. "4 + 2 * 3 - 6 / 2"
        self.text = text
        # self.pos is an index into self.text
        self.pos = 0
        self.current_char: str | None = self.text[self.pos]

    def error(self):
        raise Exception("Invalid character")

    def advance(self):
        """Advance the `pos` pointer and set the `current_char` variable."""
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None  # Indicates end of input
        else:
            self.current_char = self.text[self.pos]

    def peek(self, add=0):
        peek_pos = self.pos + 1 + add
        if peek_pos > len(self.text) - 1:
            return None
        else:
            return self.text[peek_pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def number(self):
        """Return a (multidigit) integer or float consumed from the input."""
        result = ""
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()

        return Token([TOKEN_NUM], int(result))

    def general(self, given: str):
        ret = []
        if given in LITERALS_MONTHS:
            ret += [TOKEN_MONTH]
        if given in LITERALS_HOURS:
            ret += [TOKEN_HOUR]
        if given in LITERALS_TIMES_OF_DAY:
            ret += [TOKEN_TIME_OF_DAY]
        if given in LITERALS_DETS:
            ret += [TOKEN_DET]
        if given in LITERALS_INTER:
            ret += [TOKEN_INT]
        if given in LITERALS_PREPS:
            ret += [TOKEN_PREP]
        if given in LITERALS_TIME_NOUNS:
            ret += [TOKEN_TIME_NOUN]
        if given in LITERALS_POS_LINKS:
            ret += [TOKEN_POS_LINK]
        if given in LITERALS_TIME_NOUNS_A:
            ret += [TOKEN_TIME_NOUN_A]
        if given in LITERALS_TIMES:
            ret += [TOKEN_TIME]
        if given in LITERALS_PRON_DEMS:
            ret += [TOKEN_PRON_DEM]
        if given in LITERALS_ADV_SPECS:
            ret += [TOKEN_ADV_SPE]
        if given in LITERALS_PLURAL_DETS:
            ret += [TOKEN_DET_PLURAL]
        if given in LITERALS_PRON_PER_SINGS:
            ret += [TOKEN_PRON_PER]
        if given in LITERALS_PRON_PER_PLURALS:
            ret += [TOKEN_PRON_PER_PLURAL]
        if given in LITERALS_PRON_POS_SINGS:
            ret += [TOKEN_PRON_POS]
        if given in LITERALS_PRON_POS_PLURALS:
            ret += [TOKEN_PRON_POS_PLURAL]
        if given in LITERALS_PRON_POS_N_SINGS:
            ret += [TOKEN_PRON_POS_N]
        if given in LITERALS_PRON_POS_N_PLURALS:
            ret += [TOKEN_PRON_POS_PLURAL_N]
        if given in LITERALS_PRON_POS_SINGS_NG:
            ret += [TOKEN_PRON_POS_NG]
        if given in LITERALS_PRON_POS_PLURALS_NG:
            ret += [TOKEN_PRON_POS_PLURAL_NG]
        picked = stemmer.stem_word(given, as_object=True).root
        types = dictionary.search(picked)
        if types == None:
            types = [TOKEN_NOUN]
        ret += types
        return Token(ret, given)

    def word(self):
        """Handle words, reserved or not"""
        result = ""
        while self.current_char is not None and (
            self.current_char.isalpha() or self.current_char == "-"
        ):
            result += self.current_char
            self.advance()
        return RESERVED_WORDS.get(result.upper(), self.general(result))

    def get_next_token(self):
        """Lexical analyzer (also known as scanner or tokenizer)
        This method is responsible for breaking a sentence
        apart into tokens. One token at a time.
        """
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isalpha():
                return self.word()

            if self.current_char.isdigit():
                return self.number()

            if self.current_char == ",":
                self.advance()
                return Token([TOKEN_COMMA], ",")

            if self.current_char == "'" and self.peek() == "y":
                self.advance()
                self.advance()
                return Token([TOKEN_CLIT_Y], "'y")

            if self.current_char == "'" and self.peek() == "n" and self.peek(1) == "g":
                self.advance()
                self.advance()
                self.advance()
                return Token([TOKEN_CLIT_NG], "'ng")

            self.error()

        return Token([TOKEN_EOF], None)