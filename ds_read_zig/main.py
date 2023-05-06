#!/usr/bin/env python3
import json
import re
import sys
import hy
from argparse import ArgumentParser
from antlr4 import (FileStream, CommonTokenStream)
from hy.models import (Symbol, Expression)
from .ZigLexer import ZigLexer
from .ZigParser import ZigParser
from .ZigParserVisitor import ZigParserVisitor
from . import atom
from . import keywords
from .models import ZigAtSymbol

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

    #
    # END HACKS
    #

    # System.CodeDom.CodeBinaryOperatorType.Add
    # System.CodeDom.CodeBinaryOperatorType.Subtract
    # System.Linq.Expression.ExpressionType.Add
    # System.Linq.Expression.ExpressionType.AddChecked
    # System.Linq.Expression.ExpressionType.Subtract
    # System.Linq.Expression.ExpressionType.SubtractChecked
    def visitAdditionExpression(self, ctx: ZigParser.AdditionExpressionContext):
        tokens = ctx.AdditionOp()
        childResults = [
            self.visitMultiplyExpression(node)
            for node in ctx.multiplyExpression()]
        if len(tokens) == 0:
            return childResults[0]
        token = tokens[0].symbol
        return Expression(
            [Symbol(token.text)] + childResults)

    def visitAddrSpace(self, ctx: ZigParser.AddrSpaceContext):
        return self.visitChildren(ctx)

    def visitArrayTypeStart(self, ctx: ZigParser.ArrayTypeStartContext):
        return self.visitChildren(ctx)

    # System.CodeDom.CodeBinaryOperatorType.Assign
    # System.CodeDom.CodeAssignStatement{left: CodeExpr, right: CodeExpr}
    def visitAssignExpression(self, ctx: ZigParser.AssignExpressionContext):
        # print("visitAssignExpression")
        if not ctx.assignOpExpression():
            return self.visitExpression(ctx.expression()[0])

        op = self.visitAssignOpExpression(ctx.assignOpExpression())
        results = [
            self.visitExpression(node)
            for node in ctx.expression()]
        return Expression([
            op] + results)

    def visitAssignOpExpression(self, ctx: ZigParser.AssignOpExpressionContext):
        return self.visitChildren(ctx)

    def visitBitShiftExpression(self, ctx: ZigParser.BitShiftExpressionContext):
        tokens = ctx.BitShiftOp()
        childResults = [
            self.visitAdditionExpression(node)
            for node in ctx.additionExpression()]
        if len(tokens) == 0:
            return childResults[0]
        token = tokens[0].symbol
        return Expression(
            [Symbol(token.text)] + childResults)

    # System.CodeDom.CodeBinaryOperatorType.BitwiseOr
    # System.CodeDom.CodeBinaryOperatorType.BitwiseAnd
    # System.Linq.Expression.ExpressionType.And		// BitwiseAnd
    # System.Linq.Expression.ExpressionType.Or		// BitwiseOr
    # System.Linq.Expression.ExpressionType.ExclusiveOr	// BitwiseXor
    def visitBitwiseExpression(self, ctx: ZigParser.BitwiseExpressionContext):
        return self.visitChildren(ctx)

    def visitBitwiseOpExpression(self, ctx: ZigParser.BitwiseOpExpressionContext):
        return self.visitChildren(ctx)

    def visitBitwiseKwExpression(self, ctx: ZigParser.BitwiseKwExpressionContext):
        return self.visitChildren(ctx)

    def visitBlockExpression(self, ctx: ZigParser.BlockExpressionContext):
        # TODO handle label
        return self.visitBlock(ctx.block())

    def visitBlockExpressionStatement(self, ctx: ZigParser.BlockExpressionStatementContext):
        if ctx.assignExpression():
            return self.visitAssignExpression(ctx.assignExpression())
        else:
            return self.visitChildren(ctx)





    def visitFnProtoDeclaration(self, ctx: ZigParser.FnProtoDeclarationContext):
        name = Symbol(ctx.Ident().symbol.text)
        # if len(ctx.Ident()) == 2:
        #     errorParts = [
        #         keywords.SYM_ANYERROR,
        #         keywords.SYM_BANG]
        # elif  len(ctx.Ident()) == 1:
        errorParts = []
        params = self.visitParameterDeclarationList(ctx.parameterDeclarationList())
        begin = self.visitTypeExpression(ctx.typeExpression())
        return Expression([
            keywords.SYM_FN, name, params] +
                          errorParts + [begin])

    def visitStatement(self, ctx: ZigParser.StatementContext):
        if ctx.expressionStatement():
            return self.visitExpressionStatement(ctx.expressionStatement())
        elif ctx.primaryBlockStatement():
            return self.visitPrimaryBlockStatement(ctx.primaryBlockStatement())
        else:
            return self.visitChildren(ctx)

    def visitExpressionStatement(self, ctx: ZigParser.ExpressionStatementContext):
        if ctx.varDeclaration():
            # TODO add comptime
            return self.visitVarDeclaration(ctx.varDeclaration())
        elif ctx.assignExpression():
            return self.visitAssignExpression(ctx.assignExpression())
        else:
            return self.visitChildren(ctx)

    def visitSelectionStatement(self, ctx: ZigParser.SelectionStatementContext):
        if ctx.ifStatement():
            return self.visitIfStatement(ctx.ifStatement())
        elif ctx.switchExpression():
            return self.visitSwitchExpression(ctx.switchExpression())
        else:
            return self.visitChildren(ctx)

    # CodeConditionStatement {
    #	Condition: CodeExpr,
    #	TrueStatements: []CodeStmt,
    #	TalseStatements: []CodeStmt,
    # }
    def visitIfStatement(self, ctx: ZigParser.IfStatementContext):
        def payload2lambda(pay, expr):
            results = []
            if pay:
                results.append(
                    Expression([
                        keywords.SYM_PAYLOAD,
                        [elsePayload],
                        elseExpression]))
            elif expr:
                results.append(expr)
            return results

        # print(self, repr(ctx))
        condExpression, thenPayload = self.visitIfPrefix(ctx.ifPrefix())
        if ctx.assignExpression():
            thenExpression = self.visitAssignExpression(ctx.assignExpression())
        elif ctx.blockExpression():
            thenExpression = self.visitBlockExpression(ctx.blockExpression())
        else:
            raise ValueError

        if ctx.Else():
            if ctx.payload():
                elsePayload = self.visitPayload(ctx.payload())
            else:
                elsePayload = None
            elseExpression = self.visitElseStatement(ctx.elseStatement())
        else:
            elsePayload = None
            elseExpression = None

        return Expression(
            [keywords.SYM_IF_STMT, condExpression]
            + payload2lambda(thenPayload, thenExpression)
            + payload2lambda(elsePayload, elseExpression))

    # CodeConditionStatement {
    #	Condition: CodeExpr,
    #	TrueStatements: []CodeStatement,  // Expr
    #	FalseStatements: []CodeStatement, // Expr
    # }
    def visitIfExpression(self, ctx: ZigParser.IfExpressionContext):
        def payload2lambda(pay, expr):
            results = []
            if pay:
                results.append(
                    Expression([
                        keywords.SYM_PAYLOAD,
                        [elsePayload],
                        elseExpression]))
            elif expr:
                results.append(expr)
            return results

        condExpression, thenPayload = self.visitIfPrefix(ctx.ifPrefix())
        thenExpression = self.visitThenExpression(ctx.thenExpression())

        if ctx.Else():
            if ctx.payload():
                elsePayload = self.visitPayload(ctx.payload())
            else:
                elsePayload = None
            elseExpression = self.visitElseExpression(ctx.elseExpression())
        else:
            elsePayload = None
            elseExpression = None

        return Expression(
            [keywords.SYM_IF_EXPR, condExpression]
            + payload2lambda(thenPayload, thenExpression)
            + payload2lambda(elsePayload, elseExpression))

    # CodeConditionStatement {
    #	Condition: CodeExpr,
    #	TrueStatements: []CodeStatement,  // TypeExpr
    #	FalseStatements: []CodeStatement, // TypeExpr
    # }
    def visitIfTypeExpression(self, ctx: ZigParser.IfTypeExpressionContext):
        return self.visitChildren(ctx)

    # CodeLabeledStatement {
    #	Label: string,
    #	Statement: CodeStatement,
    # }
    def visitLabeledStatement(self, ctx: ZigParser.LabeledStatementContext):
        return self.visitChildren(ctx)

    def visitLoopStatement(self, ctx: ZigParser.LoopStatementContext):
        return self.visitChildren(ctx)

    # CodeIterationStatement(
    #	InitStatement: CodeStatement,
    #	TestExpression: CodeExpression,
    #	IncrementStatement: CodeStatement,
    #	Statements: []CodeStatement)
    def visitForStatement(self, ctx: ZigParser.ForStatementContext):
        return self.visitChildren(ctx)
    def visitForExpression(self, ctx: ZigParser.ForExpressionContext):
        return self.visitChildren(ctx)
    def visitForTypeExpression(self, ctx: ZigParser.ForTypeExpressionContext):
        return self.visitChildren(ctx)

    def visitWhileStatement(self, ctx: ZigParser.WhileStatementContext):
        return self.visitChildren(ctx)

    # CodeBinaryOperatorExpression {
    #	left: CodeExpression,
    #	op: CodeBinaryOperatorType,
    #	right: CodeExpression,
    # }
    def visitExpression(self, ctx: ZigParser.ExpressionContext):
        # print("EXPR", repr(ctx))
        return self.visitChildren(ctx)

    # System.CodeDom.CodeBinaryOperatorType.BooleanOr	// LogicalOr
    # System.Linq.Expression.ExpressionType.OrElse	// LogicalOr
    def visitBoolOrExpression(self, ctx: ZigParser.BoolOrExpressionContext):
        return self.visitChildren(ctx)

    # System.CodeDom.CodeBinaryOperatorType.BooleanAnd	// LogicalAnd
    # System.Linq.Expression.ExpressionType.AndAlso	// LogicalAnd
    def visitBoolAndExpression(self, ctx: ZigParser.BoolAndExpressionContext):
        return self.visitChildren(ctx)

    # CodeBinaryOperatorType.LessThan
    # CodeBinaryOperatorType.LessThanOrEqual
    # CodeBinaryOperatorType.GreaterThan
    # CodeBinaryOperatorType.GreaterThanOrEqual
    def visitCompareExpression(self, ctx: ZigParser.CompareExpressionContext):
        tokens = ctx.compareOpExpression()
        childResults = [
            self.visitBitwiseExpression(node)
            for node in ctx.bitwiseExpression()]
        if len(tokens) == 0:
            return childResults[0]
        token = tokens[0].children[0].symbol
        return Expression(
            [Symbol(token.text)] + childResults)
        return self.visitChildren(ctx)

    # CodeBinaryOperatorType.Multiply
    # CodeBinaryOperatorType.Divide
    # CodeBinaryOperatorType.Modulus
    def visitMultiplyExpression(self, ctx: ZigParser.MultiplyExpressionContext):
        tokens = ctx.MultiplyOp()
        childResults = [
            self.visitPrefixExpression(node)
            for node in ctx.prefixExpression()]
        if len(tokens) == 0:
            return childResults[0]
        token = tokens[0].symbol
        return Expression(
            [Symbol(token.text)] + childResults)

    def visitPrefixExpression(self, ctx: ZigParser.PrefixExpressionContext):
        result = self.visitPrimaryExpression(ctx.primaryExpression())
        return result

    def visitPrimaryExpression(self, ctx: ZigParser.PrimaryExpressionContext):
        print(repr(ctx))
        if ctx.asmExpression():
            return self.visitAsmExpression(ctx.asmExpression())
        elif ctx.primaryBlockExpression():
            return self.visitPrimaryBlockExpression(
                ctx.primaryBlockExpression())
        if ctx.compoundLiteral():
            return self.visitCompoundLiteral(ctx.compoundLiteral())
        if ctx.loopExpression():
            pass

    def visitPrimaryBlockStatement(self, ctx: ZigParser.PrimaryBlockStatementContext):
        if ctx.compoundStatement():
            return self.visitCompoundStatement(
                ctx.compoundStatement())
        elif ctx.selectionStatement():
            return self.visitSelectionStatement(
                ctx.selectionStatement())
        elif ctx.iterationStatement():
            return self.visitIterationStatement(
                ctx.iterationStatement())
        else:
            raise ValueError

    def visitPrimaryBlockExpression(self, ctx: ZigParser.PrimaryBlockExpressionContext):
        if ctx.compoundExpression():
            return self.visitCompoundExpression(
                ctx.compoundExpression())
        elif ctx.selectionExpression():
            return self.visitSelectionExpression(
                ctx.selectionExpression())
        elif ctx.iterationExpression():
            return self.visitIterationExpression(
                ctx.iterationExpression())
        else:
            raise ValueError

    def visitPrimaryTypeExpression(self, ctx: ZigParser.PrimaryTypeExpressionContext):
        if ctx.AnyFrame():
            print("visitPrimaryTypeExpression.AnyFrame")
        elif ctx.Unreachable():
            print("visitPrimaryTypeExpression.Unreachable")
        elif ctx.typeName():
            return self.visitTypeName(ctx.typeName())
        elif ctx.constantExpression():
            return self.visitConstantExpression(ctx.constantExpression())
        elif ctx.groupedExpression():
            return self.visitGroupedExpression(ctx.groupedExpression())
        elif ctx.primaryTypeStatement():
            return self.visitPrimaryTypeStatement(ctx.primaryTypeStatement())
        elif ctx.primaryTypeDeclaration():
            return self.visitPrimaryTypeDeclaration(ctx.primaryTypeDeclaration())
        else:
            raise ValueError

    def visitPrimaryTypeStatement(self, ctx: ZigParser.PrimaryTypeStatementContext):
        if ctx.compoundTypeExpression():
            return self.visitCompoundTypeExpression(
                ctx.compoundTypeExpression())
        elif ctx.selectionTypeExpression():
            return self.visitSelectionTypeExpression(
                ctx.selectionTypeExpression())
        elif ctx.iterationTypeExpression():
            return self.visitIterationTypeExpression(
                ctx.iterationTypeExpression())
        else:
            raise ValueError

    def visitPrimaryTypeDeclaration(self, ctx: ZigParser.PrimaryTypeDeclarationContext):
        if ctx.containerDeclaration():
            return self.visitContainerDeclaration(
                ctx.containerDeclarat())
        elif ctx.errorSetDeclaration():
            return self.visitErrorSetDeclaration(
                ctx.errorSetDeclaration())
        elif ctx.fnProtoDeclaration():
            return self.visitFnProtoDeclaration(
                ctx.fnProtoDeclaration())
        else:
            raise ValueError

    def visitStructOrUnionSpecifier(self, ctx: ZigParser.StructOrUnionSpecifierContext):
            return self.visitChildren(ctx)
    def visitTestDeclaration(self, ctx: ZigParser.TestDeclarationContext):
            return self.visitChildren(ctx)
    def visitThenExpression(self, ctx: ZigParser.ThenExpressionContext):
            return self.visitChildren(ctx)
    def visitVarDeclarationEx(self, ctx: ZigParser.VarDeclarationExContext):
            return self.visitChildren(ctx)
    def visitVarDeclarationSpecifiers(self, ctx: ZigParser.VarDeclarationSpecifiersContext):
            return self.visitChildren(ctx)
    def visitSelectionTypeExpression(self, ctx: ZigParser.SelectionTypeExpressionContext):
            return self.visitChildren(ctx)
    def visitSelectionExpression(self, ctx: ZigParser.SelectionExpressionContext):
            return self.visitChildren(ctx)
    def visitParameterDeclarationSpecifier(self, ctx: ZigParser.ParameterDeclarationSpecifierContext):
            return self.visitChildren(ctx)
    def visitIterationExpression(self, ctx: ZigParser.IterationExpressionContext):
            return self.visitChildren(ctx)
    def visitIterationStatement(self, ctx: ZigParser.IterationStatementContext):
            return self.visitChildren(ctx)
    def visitIterationTypeExpression(self, ctx: ZigParser.IterationTypeExpressionContext):
            return self.visitChildren(ctx)
    def visitLabeledExpression(self, ctx: ZigParser.LabeledExpressionContext):
            return self.visitChildren(ctx)
    def visitFnProtoDeclarationEx(self, ctx: ZigParser.FnProtoDeclarationExContext):
            return self.visitChildren(ctx)
    def visitFnProtoDeclarationSpecifiers(self, ctx: ZigParser.FnProtoDeclarationSpecifiersContext):
            return self.visitChildren(ctx)
    def visitField(self, ctx: ZigParser.FieldContext):
            return self.visitChildren(ctx)
    def visitFieldDeclarationSpecifiers(self, ctx: ZigParser.FieldDeclarationSpecifiersContext):
            return self.visitChildren(ctx)
    def visitElseExpression(self, ctx: ZigParser.ElseExpressionContext):
            return self.visitChildren(ctx)
    def visitElseStatement(self, ctx: ZigParser.ElseStatementContext):
            return self.visitChildren(ctx)
    def visitEnumSpecifier(self, ctx: ZigParser.EnumSpecifierContext):
            return self.visitChildren(ctx)
    def visitContainerUnit(self, ctx: ZigParser.ContainerUnitContext):
        return self.visitContainerMembers(ctx.containerMembers())
    def visitCompoundStatement(self, ctx: ZigParser.CompoundStatementContext):
            return self.visitChildren(ctx)
    def visitCompTimeDeclaration(self, ctx: ZigParser.CompTimeDeclarationContext):
            return self.visitChildren(ctx)
    def visitCondExpression(self, ctx: ZigParser.CondExpressionContext):
            return self.visitChildren(ctx)

    # RustAST: Lit
    # CodePrimitiveExpression(object value)
    def visitConstantExpression(self, ctx: ZigParser.ConstantExpressionContext):
            return self.visitChildren(ctx)

    def visitBreakLabel(self, ctx: ZigParser.BreakLabelContext):
            return self.visitChildren(ctx)
    def visitBlockLabel(self, ctx: ZigParser.BlockLabelContext):
            return self.visitChildren(ctx)

    def visitAsmClobbers(self, ctx: ZigParser.AsmClobbersContext):
            return self.visitChildren(ctx)
    def visitAsmExpression(self, ctx: ZigParser.AsmExpressionContext):
            return self.visitChildren(ctx)
    def visitAsmInputItem(self, ctx: ZigParser.AsmInputItemContext):
            return self.visitChildren(ctx)
    def visitAsmInputList(self, ctx: ZigParser.AsmInputListContext):
        return list(map(
            self.visitAsmInputItem,
            ctx.asmInputItem()))
    def visitAsmInput(self, ctx: ZigParser.AsmInputContext):
            return self.visitChildren(ctx)
    def visitAsmOutputItem(self, ctx: ZigParser.AsmOutputItemContext):
        name = ctx.Ident()[0].symbol.text
        name2 = ctx.SingleString().symbol.text
        typeEx = ctx.typeExpression()
        name3 = ctx.Ident()[1].symbol.text
        return [name, name2, name3, typeEx]

    def visitAsmOutputList(self, ctx: ZigParser.AsmOutputListContext):
        return list(map(
            self.visitAsmOutputItem,
            ctx.asmOutputItem()))
    def visitAsmOutput(self, ctx: ZigParser.AsmOutputContext):
        outList = self.visitAsmOutputList(
            ctx.asmOutputList())
        inQ = self.visitAsmInput(ctx.asmInput()) \
            if ctx.asmInput() else []
        return [outList, inQ]

    def visitCompoundExpression(self, ctx: ZigParser.CompoundExpressionContext):
        if ctx.Break():
            # System.CodeDom.CodeGotoStatement(string label)
            # System.Linq.Expression.ExpressionType.Goto
            return Expression(
                [keywords.SYM_BREAK] +
                (self.visitBreakLabel(ctx.breakLabel())
                 if ctx.breakLabel() else []) +
                (self.visitExpression(ctx.expression())
                 if ctx.expression() else []))
        elif ctx.CompTime():
            pass
        elif ctx.NoSuspend():
            # CodeGotoStatement(string label)
            pass
        elif ctx.Continue():
            # CodeGotoStatement(string label)
            return Expression(
                [keywords.SYM_CONTINUE] +
                (self.visitBreakLabel(ctx.breakLabel())
                 if ctx.breakLabel() else []))
        elif ctx.Resume():
            # CodeGotoStatement(string label)
            pass
        elif ctx.Return():
            # CodeMethodReturnStatement(CodeExpression expression)
            return Expression(
                [keywords.SYM_RETURN] +
                ([self.visitExpression(ctx.expression())]
                 if ctx.expression() else []))
        elif ctx.block():
            return self.visitBlock(ctx.block())
        else:
            raise ValueError

    def visitBlock(self, ctx: ZigParser.BlockContext):
        if len(ctx.statement()) == 1:
            return self.visitStatement(ctx.statement()[0])
        else:
            return Expression([keywords.SYM_BLOCK] + [
                self.visitStatement(node)
                for node in ctx.statement()])

    def visitLoopExpression(self, ctx: ZigParser.LoopExpressionContext):
        return self.visitChildren(ctx)

    def visitWhileExpression(self, ctx: ZigParser.WhileExpressionContext):
        return self.visitChildren(ctx)

    def visitCompoundLiteral(self, ctx: ZigParser.CompoundLiteralContext):
        typeof = self.visitTypeExpression(ctx.typeExpression())
        if ctx.initList():
            results = self.visitInitList(ctx.initList())
            if not results:
                results = None
            return Expression([
                keywords.SYM_MAKE,
                typeof, results])
        else:
            return typeof

    def visitInitList(self, ctx: ZigParser.InitListContext):
        if ctx.fieldInit():
            results = [
                self.visitFieldInit(node)
                for node in ctx.fieldInit()]
            results = dict(sum([
                list(result.items())
                for result in results
            ], []))
            print(repr(results))
            return results
            # return Expression(
            #     [Expression(
            #         [keywords.SYM_INIT_LIST] +
            #         list(results))])
        elif ctx.expression():
            results = [
                self.visitExpression(node)
                for node in ctx.expression()]
            results = tuple(results)
            return results
            # return Expression(
            #     [Expression(
            #         [keywords.SYM_INIT_LIST] +
            #         list(results))])
        else:
            return tuple([])
        return self.visitChildren(ctx)

    def visitTypeExpression(self, ctx: ZigParser.TypeExpressionContext):
        result = self.visitErrorUnionExpression(ctx.errorUnionExpression())
        # TODO add this
        prefixes = [
            self.visitPrefixTypeOp(node)
            for node in ctx.prefixTypeOp()
        ]
        if len(prefixes):
            for pre in prefixes:
                result = pre(result)
        # for prefix in reverse(prefixes):
        #     result = Expression(
        #         Symbol(prefix.text), result)
        return result

    def visitDesignatorExpression(self, ctx: ZigParser.DesignatorExpressionContext):
        if ctx.suffixOp():
            return self.visitSuffixOp(ctx.suffixOp())
        elif ctx.fnCallArguments():
            return self.visitFnCallArguments(ctx.fnCallArguments())
        else:
            raise ValueError

    def visitErrorUnionExpression(self, ctx: ZigParser.ErrorUnionExpressionContext):
        result = self.visitSuffixExpression(ctx.suffixExpression())
        if ctx.typeExpression():
            typeof = self.visitTypeExpression(ctx.typeExpression())
            return Expression([
                keywords.SYM_RESULT,
                result, typeof])
        return result

    def visitSuffixExpression(self, ctx: ZigParser.SuffixExpressionContext):
        # print("visitSuffixExpression")
        if ctx.Async():
            # print("visitSuffixExpression ASYNC!")
            raise ValueError
        else:
            primary = self.visitPrimaryTypeExpression(ctx.primaryTypeExpression())
            designators = [
                self.visitDesignatorExpression(node)
                for node in ctx.designatorExpression()]
            for designator in designators:
                primary = designator(primary)
            return primary
            # if len(ctx.children
            # if ctx.suffixOp():
            #     print("visitSuffixExpression SUFFIX!", ctx.suffixOp())
            #     raise ValueError
            # else:
            #     return self.visitPrimaryTypeExpression(ctx.primaryTypeExpression())

    def visitBuiltinCallExpression(self, ctx: ZigParser.BuiltinCallExpressionContext):
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
        return atom.zig_char_literal(token.text)

    def visitSingleStringLiteral(self, ctx: ZigParser.SingleStringLiteralContext):
        token = ctx.SingleString().symbol
        return atom.zig_single_string_literal(token.text)

    def visitLineStringLiteral(self, ctx: ZigParser.LineStringLiteralContext):
        token = ctx.LineString().symbol
        return atom.zig_line_string_literal(token.text)

    # CodeTypeReferenceCollection(value: []CodeTypeReference)
    # CodeTypeReference(type: Type)
    # CodeObject(userData: ListDictionary)

    # CodeMemberField {
    # 	Name: string,
    #	Type: CodeTypeReference,
    #	CustomAttributes: CodeAttributeDeclarationCollection,
    #	Comments: CodeCommentStatementCollection,
    # }

    # RustAST: Arg
    # FnArgType := struct { Name: str, Type: Type }

    # RustAST: Signature
    # FnSigType := struct { Params: []FnArgType, Returns: []FnArgType }

    # CodeMemberMethod {
    # 	Name: string,
    #	Parameters: CodeParameterDeclarationExpressionCollection,
    #	Statements: CodeStatementCollection,
    #	ReturnType: CodeTypeReference,
    #	//ReturnTypeCustomAttributes: CodeAttributeDeclarationCollection,
    #   //ImplementationTypes: CodeTypeReferenceCollection,
    # 	//TypeParameters: CodeTypeParameterCollection,
    #	CustomAttributes: CodeAttributeDeclarationCollection,
    #	Comments: CodeCommentStatementCollection,
    # }

    # CodeMemberProperty {
    # 	Name: string,
    #	Parameters: CodeParameterDeclarationExpressionCollection,
    # 	GetStatements: CodeStatementCollection,
    # 	SetStatements: CodeStatementCollection,
    #	CustomAttributes: CodeAttributeDeclarationCollection,
    #	Comments: CodeCommentStatementCollection,
    # }

    #?
    def visitCompoundTypeExpression(self, ctx: ZigParser.CompoundTypeExpressionContext):
        if ctx.Dot():
            if ctx.Ident():
                # CodeFieldReferenceExpression
                return Expression([
                    keywords.SYM_DOT,
                    repr(ctx.Ident().symbol.text)])
            elif ctx.initList():
                # CodeObjectCreateExpression
                inits = self.visitInitList(ctx.initList())
                return Expression([
                    keywords.SYM_DOT, inits])
            else:
                raise ValueError
        elif ctx.Error():
            print("visitPrimaryTypeExpression.Error")
        elif ctx.CompTime():
            print("visitPrimaryTypeExpression.CompTime")
        elif ctx.builtinCallExpression():
            return self.visitBuiltinCallExpression(
                ctx.builtinCallExpression())
            print("visitPrimaryTypeExpression.CompTime")
        else:
            return self.visitChildren(ctx)

    def visitByteAlign3(self, ctx: ZigParser.ByteAlign3Context):
        return self.visitChildren(ctx)

    def visitContainerDeclaration(self, ctx: ZigParser.ContainerDeclarationContext):
        return self.visitChildren(ctx)

    def visitErrorSetDeclaration(self, ctx: ZigParser.ErrorSetDeclarationContext):
        return self.visitChildren(ctx)

    def visitGroupedExpression(self, ctx: ZigParser.GroupedExpressionContext):
        return self.visitExpression(ctx.expression())

    def visitLabeledTypeExpression(self, ctx: ZigParser.LabeledTypeExpressionContext):
        return self.visitChildren(ctx)

    def visitLoopTypeExpression(self, ctx: ZigParser.LoopTypeExpressionContext):
        return self.visitChildren(ctx)

    def visitWhileTypeExpression(self, ctx: ZigParser.WhileTypeExpressionContext):
        return self.visitChildren(ctx)

    def visitSwitchExpression(self, ctx: ZigParser.SwitchExpressionContext):
        return self.visitChildren(ctx)

    def visitFieldInit(self, ctx: ZigParser.FieldInitContext):
        name = Symbol(ctx.Ident().symbol.text)
        expr = self.visitExpression(ctx.expression())
        return dict([(name, expr)])

    def visitWhileContinueExpression(self, ctx: ZigParser.WhileContinueExpressionContext):
        return self.visitChildren(ctx)

    def visitLinkSection(self, ctx: ZigParser.LinkSectionContext):
        return self.visitChildren(ctx)

    def visitCallConv(self, ctx: ZigParser.CallConvContext):
        return self.visitChildren(ctx)

    def visitParameterDeclaration(self, ctx: ZigParser.ParameterDeclarationContext):
        return self.visitChildren(ctx)

    def visitParameterType(self, ctx: ZigParser.ParameterTypeContext):
        return self.visitChildren(ctx)

    def visitIfPrefix(self, ctx: ZigParser.IfPrefixContext):
        return tuple([
            self.visitCondExpression(ctx.condExpression()),
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

    def visitCompareOpExpression(self, ctx: ZigParser.CompareOpExpressionContext):
        return self.visitChildren(ctx)

    def visitPrefixTypeOp(self, ctx: ZigParser.PrefixTypeOpContext):
        if ctx.Quest():
            return lambda a: Expression([Symbol("zig:option"), a])
        return self.visitChildren(ctx)

    def visitSliceTypeRest(self, ctx: ZigParser.SliceTypeRestContext):
        return self.visitChildren(ctx)

    def visitPtrTypeRest(self, ctx: ZigParser.PtrTypeRestContext):
        return self.visitChildren(ctx)

    def visitSuffixOp(self, ctx: ZigParser.SuffixOpContext):
        def advancedDot(name):
            def designator(prim):
                if isinstance(prim, tuple):
                    if prim[0] == keywords.SYM_DOT:
                        return Expression(
                            [keywords.SYM_DOT] + list(prim[1:]) +
                            [Symbol(name)])
                return Expression([
                    keywords.SYM_DOT,
                    prim, Symbol(name)])
            return designator
        if ctx.LBrack():
            exprs = [
                self.visitExpression(node)
                for node in ctx.expression()
            ]
            return (lambda prim:
                    Expression([
                        keywords.SYM_RANGE,
                        prim] + exprs))
        elif ctx.Dot():
            name = ctx.Ident().symbol.text
            return advancedDot(name)
        elif ctx.DotQue():
            return (lambda prim:
                    Expression([
                        keywords.DOT_QUE,
                        prim]))
        elif ctx.DotStar():
            return (lambda prim:
                    Expression([
                        keywords.DOT_STAR,
                        prim]))
        else:
                        raise ValueError

        results = self.visitChildren(ctx)
        return results

    def visitFnCallArguments(self, ctx: ZigParser.FnCallArgumentsContext):
        results = self.visitArgumentExpressionList(ctx.argumentExpressionList())
        return (lambda prim: Expression([prim] + results))

    def visitSliceTypeStart(self, ctx: ZigParser.SliceTypeStartContext):
        return self.visitChildren(ctx)

    def visitPtrTypeStart(self, ctx: ZigParser.PtrTypeStartContext):
        return self.visitChildren(ctx)

    def visitDeclaration(self, ctx: ZigParser.DeclarationContext):
        if ctx.topFnDefinition():
            return self.visitTopFnDefinition(
                ctx.topFnDefinition())
        elif ctx.topVarDeclaration():
            return self.visitTopVarDeclaration(
                ctx.topVarDeclaration())
        elif ctx.UsingNamespace():
            expr = self.visitExpression(ctx.expression())
            return Expression(
                [keywords.SYM_USING_NS, expr])
        else:
            raise ValueError

    def visitTopFnDefinition(self, ctx: ZigParser.TopFnDefinitionContext):
        if ctx.fnProtoDeclaration():
            proto = self.visitFnProtoDeclaration(ctx.fnProtoDeclaration())
            if ctx.block():
                block = self.visitBlock(ctx.block())
                return Expression(list(proto) + [block])
            else:
                return proto

    def visitTopVarDeclaration(self, ctx: ZigParser.TopVarDeclarationContext):
        if ctx.varDeclaration():
            return self.visitVarDeclaration(ctx.varDeclaration())

    def visitContainerDeclarationAuto(self, ctx: ZigParser.ContainerDeclarationAutoContext):
        return self.visitChildren(ctx)

    def visitContainerDeclarationType(self, ctx: ZigParser.ContainerDeclarationTypeContext):
        return self.visitChildren(ctx)

    def visitByteAlign(self, ctx: ZigParser.ByteAlignContext):
        return self.visitChildren(ctx)

    def visitIdentList(self, ctx: ZigParser.IdentListContext):
        return self.visitChildren(ctx)

    def visitSwitchProngList(self, ctx: ZigParser.SwitchProngListContext):
        return self.visitChildren(ctx)

    def visitStringList(self, ctx: ZigParser.StringListContext):
        return self.visitChildren(ctx)

    def visitParameterDeclarationList(self, ctx: ZigParser.ParameterDeclarationListContext):
        parm_decls = list(map(
            self.visitParameterDeclaration,
            ctx.parameterDeclaration()))
        # TODO this is not an expression
        return parm_decls

    def visitArgumentExpressionList(self, ctx: ZigParser.ArgumentExpressionListContext):
        return [
            self.visitExpression(node)
            for node in ctx.expression()]

    def visitFieldList(self, ctx: ZigParser.FieldListContext):
        return self.visitChildren(ctx)

    def visitTypeName(self, ctx: ZigParser.TypeNameContext):
        # print("visitTypeName", ctx.Ident().symbol.text)
        return Symbol(ctx.Ident().symbol.text)

    def visitContainerDeclarationList(self, ctx: ZigParser.ContainerDeclarationListContext):
        if ctx.testDeclaration():
            return self.visitTestDeclaration(ctx.testDeclaration())
        elif ctx.compTimeDeclaration():
            return self.visitCompTimeDeclaration(ctx.compTimeDeclaration())
        elif ctx.declaration():
            result =  self.visitDeclaration(ctx.declaration())
            return result
        else:
            raise ValueError

    def visitFieldName(self, ctx: ZigParser.FieldNameContext):
        return Symbol(ctx.Ident().symbol.text)

    def visitContainerMembers(self, ctx: ZigParser.ContainerMembersContext):
        if ctx.fieldList():
            fields = self.visitFieldList(ctx.fieldList())
        else:
            fields = []
        if not fields:
            fields = []
        decls = list(map(
                     self.visitContainerDeclarationList,
                     ctx.containerDeclarationList()))
        return Expression([keywords.SYM_MEMBERS] +
                          fields +
                          decls)

    # CodeArgumentReferenceExpression {
    # 	ParameterName: string,
    # }

    # CodeVariableReferenceExpression {
    #	VariableName: string,
    # }
    def visitVarName(self, ctx: ZigParser.VarNameContext):
        return Symbol(ctx.Ident().symbol.text)


    # CodeVariableDeclarationStatement {
    # 	Name: string,
    #	Type: CodeTypeReference,
    # }
    def visitVarDeclaration(self, ctx: ZigParser.VarDeclarationContext):
        isConst = ctx.Const()
        isVar = ctx.Var()
        attrs = {}
        name = self.visitVarName(ctx.varName())
        if ctx.typeExpression():
            typeof = self.visitTypeExpression(ctx.typeExpression())
        else:
            typeof = None
        if ctx.expression():
            value = self.visitExpression(ctx.expression())
        else:
            value = None
        if isVar and isVar.symbol.text == "var":
            varDeclarationType = keywords.SYM_VAR
        elif isConst and isConst.symbol.text == "const":
            varDeclarationType = keywords.SYM_CONST
        else:
            raise ValueError

        if len(attrs) > 0 and typeof != None:
            return Expression([
                varDeclarationType, attrs, name, typeof, value])
        elif len(attrs) == 0 and typeof != None:
            return Expression([
                varDeclarationType, name, typeof, value])
        else:
            return Expression([
                varDeclarationType, name, value])


def convert(filename="/dev/stdin", start="start", debug=False):
    input_stream = FileStream(filename, "utf-8")
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
