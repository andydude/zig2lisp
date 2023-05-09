from antlr4 import (InputStream, CommonTokenStream)
from hy.models import Expression
from .ZigLexer import ZigLexer
from .ZigParser import ZigParser
from .lisp_visitor import LispVisitor


def read_zig(s: str, start="start") -> Expression:
    input_stream = InputStream(s)
    lexer = ZigLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = ZigParser(stream)
    visitor = LispVisitor()
    tree = getattr(parser, start)()
    exp = tree.accept(visitor)
    return exp
