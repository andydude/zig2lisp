#!/usr/bin/env python3
import hy
from argparse import ArgumentParser
from antlr4 import (FileStream, CommonTokenStream)
from .ZigLexer import ZigLexer
from .ZigParser import ZigParser
from .lisp_visitor import LispVisitor



def convert(filename="/dev/stdin", start="start", debug=False):
    input_stream = FileStream(filename, "utf-8")
    lexer = ZigLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = ZigParser(stream)
    visitor = LispVisitor(debug=debug)
    tree = getattr(parser, start)()
    output = tree.accept(visitor)
    print(hy.repr(output))


def add_arguments(parser):
    parser.add_argument("filename", default="/dev/stdin")
    parser.add_argument("--start", default="start")
    parser.add_argument("--debug", action="store_true", default=False)
    return parser


def main():
    parser = add_arguments(ArgumentParser())
    convert(**vars(parser.parse_args()))


if __name__ == '__main__':
    main()
