# Sentence

This will parse English language text and return a list of complete sentences.

The general assumption is that the given text is well formed English, where there
is some semblance of correct punctuation and syntax.

# Usage

```
    from sentence import Sentence

    text = """
        For an arbitrary collection of English word tokens
        the Sentence parse function will return a list of strings.
        Each string is a complete sentence.
    """
    sentences = Sentence.parse(text)
```
