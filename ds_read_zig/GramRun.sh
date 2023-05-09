#!/bin/sh

antlr4-parse ZigParser.g4 ZigLexer.g4 start "$@"
