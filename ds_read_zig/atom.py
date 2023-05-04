import re
import json

def zig_char_literal(s):
    return s

def zig_line_string_literal(s):
    return s

def zig_single_string_literal(s):
    assert s.startswith('"') and s.endswith('"')

    # JSON handles most cases except Reverse_Solidus Apostrophe
    s = re.sub(r"\\'",
               r'\\u0027', s)

    # JSON handles most casaes except Reverse_Solidus x HexDigit{2}
    s = re.sub(r"\\x([\dA-Fa-f][\dA-Fa-f])",
               r'\\u00\1', s)

    # JSON handles most casaes except Reverse_Solidus u { HexDigit+ }
    s = re.sub(r"\\u\{[\dA-Fa-f]*([\dA-Fa-f][\dA-Fa-f][\dA-Fa-f][\dA-Fa-f])\}",
               r'\\u\1', s)

    # JSON handles most casaes except Reverse_Solidus u { HexDigit+ }
    s = re.sub(r"\\u\{([\dA-Fa-f][\dA-Fa-f][\dA-Fa-f])\}",
               r'\\u0\1', s)

    # JSON handles most casaes except Reverse_Solidus u { HexDigit+ }
    s = re.sub(r"\\u\{([\dA-Fa-f][\dA-Fa-f])\}",
               r'\\u00\1', s)

    # JSON handles most casaes except Reverse_Solidus u { HexDigit+ }
    s = re.sub(r"\\u\{([\dA-Fa-f])\}",
               r'\\u000\1', s)

    
    return json.loads(s)
