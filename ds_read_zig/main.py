import json
import re
import sys
import hy
import antlr4
from argparse import ArgumentParser
from antlr4 import (FileStream, CommonTokenStream)
from hy.models import (Symbol, Expression)
from .ZigLexer import ZigLexer
from .ZigParser import ZigParser
from .ZigParserVisitor import ZigParserVisitor


def get_token_name_from_context(ctx, value):
    for name in dir(ctx.parser):
        if getattr(ctx.parser, name) == value:
            return name
    return 'UNK'


class Visitor(ZigParserVisitor):
    def __init__(self, debug=False):
        super().__init__()
        self.debug = debug
        
    def defaultResult(self, node=None):
        """Unused"""
        return None
    def aggregateResult(self, aggregate, nextResult):
        """Unused"""
        # return ([aggregate] if aggregate else []) + [nextResult]
        return nextResult

    def visitFnProto(self, ctx: ZigParser.FnProtoContext):
        name = Symbol(ctx.Ident().symbol.text)
        params = self.visitParamDeclList(ctx.paramDeclList())
        if ctx.AnyError():
            errorParts = [
                Symbol("zig:anyerror"),
                Symbol("zig:bang")]
        else:
            errorParts = []
        begin = self.visitTypeExpr(ctx.typeExpr())
        return Expression([
            Symbol("zig:fn"), name, params] +
                          errorParts + [begin])

    def visitStmt(self, ctx: ZigParser.StmtContext):
        if ctx.varDecl():
            # TODO add comptime
            return self.visitVarDecl(ctx.varDecl())
        elif ctx.assignExpr():
            return self.visitAssignExpr(ctx.assignExpr())
        else:
            return self.visitChildren(ctx)

    def visitIfStmt(self, ctx: ZigParser.IfStmtContext):
        def payload2lambda(pay, expr):
            print("P2L", repr(pay), repr(expr))
            results = []
            if pay:
                results.append(
                    Expression([
                        Symbol("lambda"),
                        [elsePayload],
                        elseExpr]))
            elif expr:
                results.append(expr)
            return results

        print(self, repr(ctx))
        condExpr, thenPayload = self.visitIfPrefix(ctx.ifPrefix())
        if ctx.assignExpr():
            thenExpr = self.visitAssignExpr(ctx.assignExpr())
        elif ctx.blockExpr():
            thenExpr = self.visitBlockExpr(ctx.blockExpr())
        else:
            raise ValueError

        if ctx.Else():
            if ctx.payload():
                elsePayload = self.visitPayload(ctx.payload())
            else:
                elsePayload = None
            elseExpr = self.visitElseStmt(ctx.elseStmt())
        else:
            elsePayload = None
            elseExpr = None

        return Expression(
            [Symbol("zig:if-stmt"), condExpr]
            + payload2lambda(thenPayload, thenExpr)
            + payload2lambda(elsePayload, elseExpr))

    def visitLabeledStmt(self, ctx: ZigParser.LabeledStmtContext):
        return self.visitChildren(ctx)

    def visitLoopStmt(self, ctx: ZigParser.LoopStmtContext):
        return self.visitChildren(ctx)

    def visitForStmt(self, ctx: ZigParser.ForStmtContext):
        return self.visitChildren(ctx)

    def visitWhileStmt(self, ctx: ZigParser.WhileStmtContext):
        return self.visitChildren(ctx)

    def visitBlockExprStmt(self, ctx: ZigParser.BlockExprStmtContext):
        if ctx.assignExpr():
            return self.visitAssignExpr(ctx.assignExpr())
        else:
            return self.visitChildren(ctx)

    def visitBlockExpr(self, ctx: ZigParser.BlockExprContext):
        # TODO handle label
        return self.visitBlock(ctx.block())

    def visitAssignExpr(self, ctx: ZigParser.AssignExprContext):
        # print("visitAssignExpr")
        if not ctx.assignOpExpr():
            return self.visitExpr(ctx.expr()[0])

        op = self.visitAssignOpExpr(ctx.assignOpExpr())
        results = [
            self.visitExpr(node)
            for node in ctx.expr()]
        return Expression([
            op] + results)

    def visitExpr(self, ctx: ZigParser.ExprContext):
        # print("EXPR", repr(ctx))
        return self.visitChildren(ctx)

    def visitBoolOrExpr(self, ctx: ZigParser.BoolOrExprContext):
        return self.visitChildren(ctx)

    def visitBoolAndExpr(self, ctx: ZigParser.BoolAndExprContext):
        return self.visitChildren(ctx)

    def visitCompareExpr(self, ctx: ZigParser.CompareExprContext):
        tokens = ctx.compareOpExpr()
        childResults = [
            self.visitBitwiseExpr(node)
            for node in ctx.bitwiseExpr()]
        if len(tokens) == 0:
            return childResults[0]
        token = tokens[0].children[0].symbol
        return Expression(
            [Symbol(token.text)] + childResults)
        return self.visitChildren(ctx)

    def visitBitwiseExpr(self, ctx: ZigParser.BitwiseExprContext):
        return self.visitChildren(ctx)

    def visitBitShiftExpr(self, ctx: ZigParser.BitShiftExprContext):
        tokens = ctx.BitShiftOp()
        childResults = [
            self.visitAdditionExpr(node)
            for node in ctx.additionExpr()]
        if len(tokens) == 0:
            return childResults[0]
        token = tokens[0].symbol
        return Expression(
            [Symbol(token.text)] + childResults)

    def visitAdditionExpr(self, ctx: ZigParser.AdditionExprContext):
        tokens = ctx.AdditionOp()
        childResults = [
            self.visitMultiplyExpr(node)
            for node in ctx.multiplyExpr()]
        if len(tokens) == 0:
            return childResults[0]
        token = tokens[0].symbol
        return Expression(
            [Symbol(token.text)] + childResults)

    def visitMultiplyExpr(self, ctx: ZigParser.MultiplyExprContext):
        tokens = ctx.MultiplyOp()
        childResults = [
            self.visitPrefixExpr(node)
            for node in ctx.prefixExpr()]
        if len(tokens) == 0:
            return childResults[0]
        token = tokens[0].symbol
        return Expression(
            [Symbol(token.text)] + childResults)

    def visitPrefixExpr(self, ctx: ZigParser.PrefixExprContext):
        return self.visitChildren(ctx)

    def visitPrimaryExpr(self, ctx: ZigParser.PrimaryExprContext):
        if ctx.Break():
            return Expression([Symbol("zig:break")] +
                              ([self.visitExpr(ctx.expr())]
                               if ctx.expr() else []))
        elif ctx.CompTime():
            pass
        elif ctx.NoSuspend():
            pass
        elif ctx.Continue():
            pass
        elif ctx.Resume():
            pass
        elif ctx.Return():
            return Expression([Symbol("zig:return")] +
                              ([self.visitExpr(ctx.expr())]
                               if ctx.expr() else []))
        elif ctx.loopExpr():
            pass
        else:
            return self.visitChildren(ctx)

    def visitIfExpr(self, ctx: ZigParser.IfExprContext):
        def payload2lambda(pay, expr):
            results = []
            if pay:
                results.append(
                    Expression([
                        Symbol("lambda"),
                        [elsePayload],
                        elseExpr]))
            elif expr:
                results.append(expr)
            return results

        condExpr, thenPayload = self.visitIfPrefix(ctx.ifPrefix())
        thenExpr = self.visitThenExpr(ctx.thenExpr())

        if ctx.Else():
            if ctx.payload():
                elsePayload = self.visitPayload(ctx.payload())
            else:
                elsePayload = None
            elseExpr = self.visitElseExpr(ctx.elseExpr())
        else:
            elsePayload = None
            elseExpr = None

        return Expression(
            [Symbol("if"), condExpr]
            + payload2lambda(thenPayload, thenExpr)
            + payload2lambda(elsePayload, elseExpr))

    def visitBlock(self, ctx: ZigParser.BlockContext):
        if len(ctx.stmt()) == 1:
            return self.visitStmt(ctx.stmt()[0])
        else:
            return Expression([Symbol("begin")] + [
                self.visitStmt(node)
                for node in ctx.stmt()])

    def visitLoopExpr(self, ctx: ZigParser.LoopExprContext):
        return self.visitChildren(ctx)

    def visitForExpr(self, ctx: ZigParser.ForExprContext):
        return self.visitChildren(ctx)

    def visitWhileExpr(self, ctx: ZigParser.WhileExprContext):
        return self.visitChildren(ctx)

    def visitCurlySuffixExpr(self, ctx: ZigParser.CurlySuffixExprContext):
        typeof = self.visitTypeExpr(ctx.typeExpr())
        if ctx.initList():
            value = self.visitInitList(ctx.initList())
            if not value:
                value = []
            return Expression([
                Symbol("zig:curlysuffix"),
                typeof] + value)
        else:
            return typeof

    def visitInitList(self, ctx: ZigParser.InitListContext):
        return self.visitChildren(ctx)

    def visitTypeExpr(self, ctx: ZigParser.TypeExprContext):
        result = self.visitErrorUnionExpr(ctx.errorUnionExpr())
        # TODO add this
        prefixes = [
            self.visitPrefixTypeOp(node)
            for node in ctx.prefixTypeOp()
        ]
        if len(prefixes):
            print(repr(prefixes))
            raise ValueError
        # for prefix in reverse(prefixes):
        #     result = Expression(
        #         Symbol(prefix.text), result)
        return result

    def visitDesignatorExpr(self, ctx: ZigParser.DesignatorExprContext):
        if ctx.suffixOp():
            return self.visitSuffixOp(ctx.suffixOp())
        elif ctx.fnCallArguments():
            return self.visitFnCallArguments(ctx.fnCallArguments())
        else:
            raise ValueError

    def visitErrorUnionExpr(self, ctx: ZigParser.ErrorUnionExprContext):
        result = self.visitSuffixExpr(ctx.suffixExpr())
        if ctx.typeExpr():
            typeof = self.visitTypeExpr(ctx.typeExpr())
            return Expression([
                Symbol("zig:errorunion:!"),
                result, typeof])
        return result

    def visitSuffixExpr(self, ctx: ZigParser.SuffixExprContext):
        # print("visitSuffixExpr")
        if ctx.Async():
            # print("visitSuffixExpr ASYNC!")
            raise ValueError
        else:
            primary = self.visitPrimaryTypeExpr(ctx.primaryTypeExpr())
            designators = [
                self.visitDesignatorExpr(node)
                for node in ctx.designatorExpr()]
            for designator in designators:
                primary = designator(primary)
            return primary
            # if len(ctx.children
            # if ctx.suffixOp():
            #     print("visitSuffixExpr SUFFIX!", ctx.suffixOp())
            #     raise ValueError
            # else:
            #     return self.visitPrimaryTypeExpr(ctx.primaryTypeExpr())

    def visitPrimaryBiCall(self, ctx: ZigParser.PrimaryBiCallContext):
        name = ctx.BuiltinIdent().symbol.text
        designator = self.visitFnCallArguments(ctx.fnCallArguments())
        return designator(Symbol(name))

    def visitIntegerLiteral(self, ctx: ZigParser.IntegerLiteralContext):
        token = ctx.Integer().symbol
        return int(token.text)

    def visitFloatingLiteral(self, ctx: ZigParser.FloatingLiteralContext):
        token = ctx.Float().symbol
        return float(token.text)

    def visitCharLiteral(self, ctx: ZigParser.CharLiteralContext):
        token = ctx.Char().symbol
        return str(token.text)

    def visitSingleStringLiteral(self, ctx: ZigParser.SingleStringLiteralContext):
        token = ctx.SingleString().symbol
        return str(json.loads(token.text))

    def visitLineStringLiteral(self, ctx: ZigParser.LineStringLiteralContext):
        token = ctx.LineString().symbol
        return str(token.text)

    def visitPrimaryTypeExpr(self, ctx: ZigParser.PrimaryTypeExprContext):
        if ctx.Dot():
            print("visitPrimaryTypeExpr.Dot")
        elif ctx.Error():
            print("visitPrimaryTypeExpr.Error")
        elif ctx.AnyFrame():
            print("visitPrimaryTypeExpr.AnyFrame")
        elif ctx.Unreachable():
            print("visitPrimaryTypeExpr.Unreachable")
        else:
            return self.visitChildren(ctx)

    def visitErrorSetDecl(self, ctx: ZigParser.ErrorSetDeclContext):
        return self.visitChildren(ctx)

    def visitGroupedExpr(self, ctx: ZigParser.GroupedExprContext):
        return self.visitExpr(ctx.expr())

    def visitIfTypeExpr(self, ctx: ZigParser.IfTypeExprContext):
        return self.visitChildren(ctx)

    def visitLabeledTypeExpr(self, ctx: ZigParser.LabeledTypeExprContext):
        return self.visitChildren(ctx)

    def visitLoopTypeExpr(self, ctx: ZigParser.LoopTypeExprContext):
        return self.visitChildren(ctx)

    def visitForTypeExpr(self, ctx: ZigParser.ForTypeExprContext):
        return self.visitChildren(ctx)

    def visitWhileTypeExpr(self, ctx: ZigParser.WhileTypeExprContext):
        return self.visitChildren(ctx)

    def visitSwitchExpr(self, ctx: ZigParser.SwitchExprContext):
        return self.visitChildren(ctx)

    def visitFieldInit(self, ctx: ZigParser.FieldInitContext):
        return self.visitChildren(ctx)

    def visitWhileContinueExpr(self, ctx: ZigParser.WhileContinueExprContext):
        return self.visitChildren(ctx)

    def visitLinkSection(self, ctx: ZigParser.LinkSectionContext):
        return self.visitChildren(ctx)

    def visitAddrSpace(self, ctx: ZigParser.AddrSpaceContext):
        return self.visitChildren(ctx)

    def visitCallConv(self, ctx: ZigParser.CallConvContext):
        return self.visitChildren(ctx)

    def visitParamDecl(self, ctx: ZigParser.ParamDeclContext):
        return self.visitChildren(ctx)

    def visitParamType(self, ctx: ZigParser.ParamTypeContext):
        return self.visitChildren(ctx)

    def visitIfPrefix(self, ctx: ZigParser.IfPrefixContext):
        return tuple([
            self.visitCondExpr(ctx.condExpr()),
            self.visitPtrPayload(ctx.ptrPayload())
            if ctx.ptrPayload() else None])

    def visitWhilePrefix(self, ctx: ZigParser.WhilePrefixContext):
        return self.visitChildren(ctx)

    def visitForPrefix(self, ctx: ZigParser.ForPrefixContext):
        return self.visitChildren(ctx)

    def visitPayload(self, ctx: ZigParser.PayloadContext):
        return Symbol(ctx.Ident().symbol.text)

    def visitPtrPayload(self, ctx: ZigParser.PtrPayloadContext):
        # TODO handle ptr
        return Symbol(ctx.Ident().symbol.text)

    def visitPtrIndexPayload(self, ctx: ZigParser.PtrIndexPayloadContext):
        return self.visitChildren(ctx)

    def visitPtrListPayload(self, ctx: ZigParser.PtrListPayloadContext):
        return self.visitChildren(ctx)

    def visitSwitchProng(self, ctx: ZigParser.SwitchProngContext):
        return self.visitChildren(ctx)

    def visitSwitchCase(self, ctx: ZigParser.SwitchCaseContext):
        return self.visitChildren(ctx)

    def visitSwitchItem(self, ctx: ZigParser.SwitchItemContext):
        return self.visitChildren(ctx)

    def visitForArgumentsList(self, ctx: ZigParser.ForArgumentsListContext):
        return self.visitChildren(ctx)

    def visitForItem(self, ctx: ZigParser.ForItemContext):
        return self.visitChildren(ctx)

    def visitAssignOpExpr(self, ctx: ZigParser.AssignOpExprContext):
        # print("visitAssignOpExpr", ctx.getText())
        return self.visitChildren(ctx)

    def visitCompareOpExpr(self, ctx: ZigParser.CompareOpExprContext):
        return self.visitChildren(ctx)

    def visitBitwiseOpExpr(self, ctx: ZigParser.BitwiseOpExprContext):
        return self.visitChildren(ctx)

    def visitBitwiseKwExpr(self, ctx: ZigParser.BitwiseKwExprContext):
        return self.visitChildren(ctx)

    def visitPrefixTypeOp(self, ctx: ZigParser.PrefixTypeOpContext):
        return self.visitChildren(ctx)

    def visitSliceTypeRest(self, ctx: ZigParser.SliceTypeRestContext):
        return self.visitChildren(ctx)

    def visitPtrTypeRest(self, ctx: ZigParser.PtrTypeRestContext):
        return self.visitChildren(ctx)

    def visitSuffixOp(self, ctx: ZigParser.SuffixOpContext):
        def advancedDot(name):
            def designator(prim):
                if isinstance(prim, tuple):
                    if str(prim[0]) == "zig:dot":
                        return Expression(
                            [Symbol("zig:dot")] + list(prim[1:]) +
                            [Symbol(name)])
                return Expression([
                    Symbol("zig:dot"),
                    prim, Symbol(name)])
            return designator
        if ctx.LBrack():
            exprs = [
                self.visitExpr(node)
                for node in ctx.expr()
            ]
            return (lambda prim:
                    Expression([
                        Symbol("zig:array-range"),
                        prim] + exprs))
        elif ctx.Dot():
            name = ctx.Ident().symbol.text
            return advancedDot(name)
        elif ctx.DotQue():
            return (lambda prim:
                    Expression([
                        Symbol("zig:dot-quest"),
                        prim]))
        elif ctx.DotStar():
            return (lambda prim:
                    Expression([
                        Symbol("zig:dot-star"),
                        prim]))
        else:
                        raise ValueError

        results = self.visitChildren(ctx)
        return results

    def visitFnCallArguments(self, ctx: ZigParser.FnCallArgumentsContext):
        results = self.visitExprList(ctx.exprList())
        return (lambda prim: Expression([prim] + results))

    def visitSliceTypeStart(self, ctx: ZigParser.SliceTypeStartContext):
        return self.visitChildren(ctx)

    def visitPtrTypeStart(self, ctx: ZigParser.PtrTypeStartContext):
        return self.visitChildren(ctx)

    def visitArrayTypeStart(self, ctx: ZigParser.ArrayTypeStartContext):
        return self.visitChildren(ctx)

    def visitDecl(self, ctx: ZigParser.DeclContext):
        if ctx.fnProto():
            proto = self.visitFnProto(ctx.fnProto())
            if ctx.block():
                block = self.visitBlock(ctx.block())
                return Expression(list(proto) + [block])
            else:
                return proto
        elif ctx.varDecl():
            return self.visitVarDecl(ctx.varDecl())
        else:
            expr = self.visitExpr(ctx.expr())
            return Expression(
                [Symbol("zig:using-namespace"), expr])

    def visitDeclAuto(self, ctx: ZigParser.DeclAutoContext):
        return self.visitChildren(ctx)

    def visitDeclType(self, ctx: ZigParser.DeclTypeContext):
        return self.visitChildren(ctx)

    def visitByteAlign(self, ctx: ZigParser.ByteAlignContext):
        return self.visitChildren(ctx)

    def visitIdentList(self, ctx: ZigParser.IdentListContext):
        return self.visitChildren(ctx)

    def visitSwitchProngList(self, ctx: ZigParser.SwitchProngListContext):
        return self.visitChildren(ctx)

    def visitStringList(self, ctx: ZigParser.StringListContext):
        return self.visitChildren(ctx)

    def visitParamDeclList(self, ctx: ZigParser.ParamDeclListContext):
        return self.visitChildren(ctx)

    def visitExprList(self, ctx: ZigParser.ExprListContext):
        return [
            self.visitExpr(node)
            for node in ctx.expr()]

    def visitFieldList(self, ctx: ZigParser.FieldListContext):
        return self.visitChildren(ctx)

    def visitTypeName(self, ctx: ZigParser.TypeNameContext):
        # print("visitTypeName", ctx.Ident().symbol.text)
        return Symbol(ctx.Ident().symbol.text)

    def visitFieldName(self, ctx: ZigParser.FieldNameContext):
        return Symbol(ctx.Ident().symbol.text)

    def visitMembers(self, ctx: ZigParser.MembersContext):
        if ctx.fieldList():
            fields = self.visitFieldList(ctx.fieldList())
        else:
            fields = []
        decls = [
            self.visitDeclaration(node)
            for node in ctx.declaration()
        ]
        return Expression([Symbol("zig:members")] +
                          list(fields) +
                          list(decls))


    # Visit a parse tree produced by ZigParser#varName.
    def visitVarName(self, ctx: ZigParser.VarNameContext):
        return Symbol(ctx.Ident().symbol.text)


    # Visit a parse tree produced by ZigParser#varDecl.
    def visitVarDecl(self, ctx: ZigParser.VarDeclContext):
        isConst = ctx.Const()
        isVar = ctx.Var()
        name = self.visitVarName(ctx.varName())
        if ctx.typeExpr():
            typeof = self.visitTypeExpr(ctx.typeExpr())
        else:
            typeof = None
        if ctx.expr():
            value = self.visitExpr(ctx.expr())
        else:
            value = None
        if isVar and isVar.symbol.text == "var":
            varDeclType = Symbol("zig:const")
        elif isConst and isConst.symbol.text == "const":
            varDeclType = Symbol("zig:var")
        else:
            raise ValueError
        return Expression([
            varDeclType, {}, name, typeof, value])


def convert(filename="/dev/stdin", start="start", debug=False):
    input_stream = FileStream(filename)
    lexer = ZigLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = ZigParser(stream)
    visitor = Visitor(debug=debug)
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
