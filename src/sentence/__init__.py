import re
from dictd import Dictd
from babyname import BabyName
from lastname import LastName


class Sentence:

    CommonAbbr = [
        'mr',
        'mrs',
        'dr',
        'p',
        'n',
        'e',
        's',
        'v',
        'vs',
        'w',
    ]

    EndOfSentenceChars = [ '!', '?', '.', '...', '....', '\u2026' ]

    Quotes = {
        '\u0022': '\u0022',
        '\u0022': '\u0022',
        "\u0027": "\u0027",
        '\u00AB': '\u00BB',
        '\u00E2': '\u00E2',
        '\u2018': '\u2019',
        '\u201C': '\u201D',
        '\u201E': '\u201C',
        '\u201F': '\u201E',
        '\u2039': '\u203A',
        '\u275B': '\u275C',
        '\u275D': '\u275E',
        '\u276E': '\u276F',
        '\u301D': '\u301E',
    }

    Brackets = {
        '(': ')',
        '[': ']',
        '<': '>',
        '{': '}',
    }

    BalancedPunctuation = {
        **Quotes,
        **Brackets,
    }


    @classmethod
    def _is_abbreviation_(cls, word):
        return word.lower() in cls.CommonAbbr


    @classmethod
    def _is_name_(cls, word):
        name = BabyName().lookup(word)
        if name is None:
            name = LastName().lookup(word)
        return name is not None


    @classmethod
    def _is_acronym_(cls, word):
        word = re.sub(r'\W+$', "", word)
        if not word.isupper():
            return False
        result = Dictd.lookup(word)
        if result is None:
            return False
        if 'vera' in result:
            return True
        return False


    @classmethod
    def _is_english_word_(cls, word):
        word = re.sub(r'\W+$', "", word)
        result = Dictd.lookup(word)
        return result is not None


    @classmethod
    def _has_unbalanced_punctuation_(cls, tokens):
        n = 0
        for token in tokens:
            for left_p, right_p in cls.BalancedPunctuation.items():
                n = token.count(left_p)
                n -= token.count(right_p)
        return n != 0


    @classmethod
    def _is_eos_str_(cls, token):
        for left_q, right_q in cls.Quotes.items():
            token = token.rstrip(left_q).rstrip(right_q)
        token = token.rstrip('_')
        if not any(map(lambda eos: token.endswith(eos), cls.EndOfSentenceChars)):
            return False
        return True


    @classmethod
    def _format_acronyms_(cls, text):
        acronyms = re.findall(r'([_\s]([A-Z])[.]([_\s]*([A-Z])[.][_]?)+)', text)
        for acronym in [a[0] for a in acronyms]:
            end = acronym[-1] if acronym[-1] != '.' else ""
            revised_mid = re.sub(r'(\w)[._\s]+', r'\1', acronym) + end
            revised_eot = re.sub(r'_[.]$', '._', revised_mid + '.')
            acronym_re = re.sub(r'(\W)', r'[\1]', acronym)
            regex_mid = re.compile(acronym_re)
            regex_eot = re.compile(f'{acronym_re}$')
            text = re.sub(regex_eot, revised_eot, text)
            text = re.sub(regex_mid, revised_mid, text)

        return text

    @classmethod
    def _cleanup_(cls, text):
        text = text.replace('[', ' [')
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'[.][ ][.]', '..', text)
        text = re.sub(r'[.]{3,}', '...', text)
        text = cls._format_acronyms_(text.strip())
        return text.strip()


    @classmethod
    def _tokenize_(cls, text):
        text = cls._cleanup_(text)
        for token in re.split(r'\s+', text):
            if len(token) > 0:
                yield token


    @classmethod
    def is_sentence(cls, queue, next_token=None):

        if len(queue) == 0:
            return False

        last_token = queue[-1]

        if not cls._is_eos_str_(last_token):
            return False

        if cls._has_unbalanced_punctuation_(queue):
            return False

        if next_token is None:
            return True

        if next_token[0:1].islower():
            return False

        for left_q, right_q in cls.Quotes.items():
            last_token = last_token.rstrip(left_q).rstrip(right_q)

        if last_token.endswith('.'):

            last_token = last_token.rstrip('.')

            if last_token.isnumeric():
                return True

            if cls._is_abbreviation_(last_token):
                return False

            if len(last_token) == 1 and last_token.isupper():
                if cls._is_name_(next_token):
                    return False
                if not cls._is_english_word_(next_token):
                    return False

        return True


    @classmethod
    def parse(cls, text):
        queue = []
        tokens = list(cls._tokenize_(text))
        for n, token in enumerate(tokens):
            next_token = tokens[n + 1] if n + 1 < len(tokens) else None
            queue.append(token)
            if cls.is_sentence(queue, next_token):
                queue[0] = queue[0][0:1].upper() + queue[0][1:]
                yield ' '.join(queue)
                queue = []
        if len(queue) > 0:
            if cls.is_sentence(queue, next_token):
                yield ' '.join(queue)

