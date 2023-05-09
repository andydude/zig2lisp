#!/bin/sh

antlr4 -Dlanguage=Python3 ZigParser.g4 ZigLexer.g4 -visitor -no-listener
