import re
from .Code import Code


class PhpCode(Code("php")):
    """Line of PHP Code. (extends str)
    Takes a string representing a portion of PHP code.

    >>> code = PhpCode('<? phpinfo() ?>')
    >>> code()
    'phpinfo();'
    >>> print(code)
    '<?php phpinfo(); ?>'

    """
    def __new__(cls, string):
        # disable check if code is multiline
        string = string.strip()
        if len(string.splitlines()) == 1:
            pattern = (r"^(?:<\?(?:[pP][hH][pP])?\s+)?\s*("
                       r"[^\<\s].{4,}?)\s*;?\s*(?:\?\>)?$")
            try:
                # regex validates and parses the string
                string = re.match(pattern, string)[1]
            except:
                raise ValueError(f'«{string}» is not PHP code')

        return super().__new__(cls, string)

    def _code_value(self):
        return f"<?php {self.__call__()}; ?>"
