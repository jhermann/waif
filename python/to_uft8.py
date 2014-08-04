# -*- coding: utf-8 -*-

def to_utf8(text):
    """Convert given text to UTF-8 encoding (as far as possible)."""
    if not text:
        return text

    try: # unicode or pure ascii
        return text.encode("utf8")
    except UnicodeDecodeError:
        try: # successful UTF-8 decode means is pretty sure UTF-8 already
            text.decode("utf8")
            return text
        except UnicodeDecodeError:
            try: # get desperate; and yes, this has a western hemisphere bias
                return text.decode("cp1252").encode("utf8")
            except UnicodeDecodeError:
                pass

    return text # return unchanged, hope for the best>>> import to_uft8

if __name__ == '__main__':
    print(repr(to_utf8(None)))
    print(repr(to_utf8("")))
    print(repr(to_utf8("abc")))
    print(repr(to_utf8("abcäöü€")))
    print(repr(to_utf8(u"abcäöü€")))
    print(repr(to_utf8(u"abcäöü€".encode("cp1252"))))
