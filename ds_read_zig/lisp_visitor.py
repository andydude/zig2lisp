from hy.models import (Symbol, Expression)
from .ZigParser import ZigParser
from .ZigParserVisitor import ZigParserVisitor
from . import atom
from . import keywords


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


class LispVisitor(ZigParserVisitor):
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
        operators = [
            Symbol(op.symbol.text)
            for op in ctx.additionOp()]
        operands = list(map(
            self.visitMultiplyExpression,
            ctx.multiplyExpression()))
        if len(operators) == 1:
            return Expression([operators[0]] + operands)
        elif len(operators) == 0:
            return operands[0]
        else:
            raise ValueError

    def visitAdditionOp(self, ctx:ZigParser.AdditionOpContext):
        return self.visitChildren(ctx)
        
    def visitAddrSpace(self, ctx: ZigParser.AddrSpaceContext):
        return self.visitChildren(ctx)

    def visitArgumentExpressionList(self, ctx: ZigParser.ArgumentExpressionListContext):
        return [
            self.visitExpression(node)
            for node in ctx.expression()]

    # This must return a designator, which is a lambda
    # from Type -> Type
    def visitArrayTypeStart(self, ctx: ZigParser.ArrayTypeStartContext):
        exprs = list(map(
            self.visitExpression,
            ctx.expression()))
        return lambda t: Expression(
            [keywords.SYM_ARRAY_TYPE, t] + exprs)

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

    # System.Linq.Expression.ExpressionType.LeftShift
    # System.Linq.Expression.ExpressionType.RightShift
    def visitBitShiftExpression(self, ctx: ZigParser.BitShiftExpressionContext):
        operators = [
            Symbol(op.symbol.text)
            for op in ctx.BitShiftOp()]
        operands = list(map(
            self.visitAdditionExpression,
            ctx.additionExpression()))
        if len(operators) == 1:
            return Expression([operators[0]] + operands)
        elif len(operators) == 0:
            return operands[0]
        else:
            raise ValueError

    # System.CodeDom.CodeBinaryOperatorType.BitwiseOr
    # System.CodeDom.CodeBinaryOperatorType.BitwiseAnd
    # System.Linq.Expression.ExpressionType.And		// BitwiseAnd
    # System.Linq.Expression.ExpressionType.Or		// BitwiseOr
    # System.Linq.Expression.ExpressionType.ExclusiveOr	// BitwiseXor
    def visitBitwiseExpression(self, ctx: ZigParser.BitwiseExpressionContext):
        operators = list(map(
            self.visitBitwiseOpExpression,
            ctx.bitwiseOpExpression()))
        operands = list(map(
            self.visitBitShiftExpression,
            ctx.bitShiftExpression()))
        if len(operators) == 1:
            return Expression([operators[0]] + operands)
        elif len(operators) == 0:
            return operands[0]
        else:
            raise ValueError

    def visitBitwiseKwExpression(self, ctx: ZigParser.BitwiseKwExpressionContext):
        if ctx.OrElse():
            return Symbol(ctx.OrElse().symbol.text)
        elif ctx.Catch():
            # TODO
            return Symbol(ctx.Catch().symbol.text)
        else:
            raise ValueError

    def visitBitwiseOpExpression(self, ctx: ZigParser.BitwiseOpExpressionContext):
        if ctx.BitwiseOp():
            return Symbol(ctx.BitwiseOp().symbol.text)
        elif ctx.bitwiseKwExpression():
            return self.visitBitwiseKwExpression(
                ctx.bitwiseKwExpression())
        else:
            raise ValueError

    def visitBlockExpression(self, ctx: ZigParser.BlockExpressionContext):
        # TODO handle label
        return self.visitBlock(ctx.block())

    def visitBlockExpressionStatement(self, ctx: ZigParser.BlockExpressionStatementContext):
        if ctx.assignExpression():
            return self.visitAssignExpression(ctx.assignExpression())
        else:
            return self.visitChildren(ctx)

    def visitBlockLabel(self, ctx: ZigParser.BlockLabelContext):
            return self.visitChildren(ctx)

    def visitBlock(self, ctx: ZigParser.BlockContext):
        if len(ctx.statement()) == 1:
            return self.visitStatement(ctx.statement()[0])
        else:
            return Expression([keywords.SYM_BLOCK] + [
                self.visitStatement(node)
                for node in ctx.statement()])

    # System.CodeDom.CodeBinaryOperatorType.BooleanAnd	// LogicalAnd
    # System.Linq.Expression.ExpressionType.AndAlso	// LogicalAnd
    def visitBoolAndExpression(self, ctx: ZigParser.BoolAndExpressionContext):
        operators = [
            Symbol(op.symbol.text) for op in ctx.And()]
        operands = list(map(
            self.visitCompareExpression,
            ctx.compareExpression()))
        if len(operators):
            return Expression([operators[0]] + operands)
        else:
            return operands[0]

    # System.CodeDom.CodeBinaryOperatorType.BooleanOr	// LogicalOr
    # System.Linq.Expression.ExpressionType.OrElse	// LogicalOr
    def visitBoolOrExpression(self, ctx: ZigParser.BoolOrExpressionContext):
        operators = [
            Symbol(op.symbol.text) for op in ctx.Or()]
        operands = list(map(
            self.visitBoolAndExpression,
            ctx.boolAndExpression()))
        if len(operators):
            return Expression([operators[0]] + operands)
        else:
            return operands[0]

    def visitBreakLabel(self, ctx: ZigParser.BreakLabelContext):
            return self.visitChildren(ctx)

    def visitBuiltinCallExpression(self, ctx: ZigParser.BuiltinCallExpressionContext):
        name = ctx.BuiltinIdent().symbol.text
        designator = self.visitFnCallArguments(ctx.fnCallArguments())
        return designator(Symbol(name))

    def visitByteAlign3(self, ctx: ZigParser.ByteAlign3Context):
        return self.visitChildren(ctx)

    def visitByteAlign(self, ctx: ZigParser.ByteAlignContext):
        return self.visitChildren(ctx)

    def visitCallConv(self, ctx: ZigParser.CallConvContext):
        return self.visitChildren(ctx)

    def visitCharLiteral(self, ctx: ZigParser.CharLiteralContext):
        token = ctx.Char().symbol
        return atom.zig_char_literal(token.text)

    # CodeBinaryOperatorType.LessThan
    # CodeBinaryOperatorType.LessThanOrEqual
    # CodeBinaryOperatorType.GreaterThan
    # CodeBinaryOperatorType.GreaterThanOrEqual
    def visitCompareExpression(self, ctx: ZigParser.CompareExpressionContext):
        operators = list(map(
            self.visitCompareOpExpression,
            ctx.compareOpExpression()))
        operands = list(map(
            self.visitBitwiseExpression,
            ctx.bitwiseExpression()))
        if len(operators) == 1:
            return Expression([operators[0]] + operands)
        elif len(operators) == 0:
            return operands[0]
        else:
            raise ValueError

    def visitCompareOpExpression(self, ctx: ZigParser.CompareOpExpressionContext):
        if ctx.Equal2():
            return Symbol(ctx.Equal2().symbol.text)
        elif ctx.CompareOp():
            return Symbol(ctx.CompareOp().symbol.text)
        else:
            raise ValueError

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

    # Zig-Spec: `CurlySuffixExpr`
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

    def visitCompoundStatement(self, ctx: ZigParser.CompoundStatementContext):
        stmt = self.visitBlockExpressionStatement(
            ctx.blockExpressionStatement())

        sym = None
        if ctx.CompTime():
            sym = keywords.SYM_COMPTIME
        elif ctx.NoSuspend():
            sym = keywords.SYM_NOSUSPEND
        elif ctx.Defer():
            sym = keywords.SYM_DEFER
        elif ctx.ErrDefer():
            sym = keywords.SYM_ERRDEFER
        else:
            raise ValueError

        return Expression([sym, stmt])

    def visitCompoundTypeExpression(self, ctx: ZigParser.CompoundTypeExpressionContext):
        if ctx.Error():
            if ctx.Ident():
                return Expression([
                    keywords.SYM_DOT,
                    keywords.SYM_ERROR,
                    Symbol(ctx.Ident().symbol.text)])
                
            else:
                raise ValueError
        elif ctx.Dot():
            if ctx.Ident():
                # CodeFieldReferenceExpression
                return Expression([
                    keywords.SYM_DOT,
                    Symbol(ctx.Ident().symbol.text)])
            elif ctx.initList():
                # CodeObjectCreateExpression
                inits = self.visitInitList(ctx.initList())
                return Expression([
                    keywords.SYM_DOT, inits])
            else:
                raise ValueError
        elif ctx.CompTime():
            print("visitPrimaryTypeExpression.CompTime")
        elif ctx.builtinCallExpression():
            return self.visitBuiltinCallExpression(
                ctx.builtinCallExpression())
            print("visitPrimaryTypeExpression.CompTime")
        else:
            return self.visitChildren(ctx)

    def visitCompTimeDeclaration(self, ctx: ZigParser.CompTimeDeclarationContext):
            return self.visitChildren(ctx)

    def visitCondExpression(self, ctx: ZigParser.CondExpressionContext):
            return self.visitChildren(ctx)

    # RustAST: Lit
    # CodePrimitiveExpression(object value)
    def visitConstantExpression(self, ctx: ZigParser.ConstantExpressionContext):
        if ctx.integerLiteral():
            return self.visitIntegerLiteral(ctx.integerLiteral())
        elif ctx.floatingLiteral():
            return self.visitFloatingLiteral(ctx.floatingLiteral())
        elif ctx.charLiteral():
            return self.visitCharLiteral(ctx.charLiteral())
        elif ctx.singleStringLiteral():
            return self.visitSingleStringLiteral(ctx.singleStringLiteral())
        elif ctx.lineStringLiteral():
            return self.visitLineStringLiteral(ctx.lineStringLiteral())
        else:
            raise ValueError

    def visitContainerDeclarationAuto(self, ctx: ZigParser.ContainerDeclarationAutoContext):
        return self.visitChildren(ctx)

    def visitContainerDeclarationList(self, ctx: ZigParser.ContainerDeclarationListContext):
        # print("visitContainerDeclarationList")
        if ctx.testDeclaration():
            return self.visitTestDeclaration(ctx.testDeclaration())
        elif ctx.compTimeDeclaration():
            return self.visitCompTimeDeclaration(ctx.compTimeDeclaration())
        elif ctx.declaration():
            result =  self.visitDeclaration(ctx.declaration())
            return result
        else:
            raise ValueError

    def visitContainerDeclaration(self, ctx: ZigParser.ContainerDeclarationContext):
        return self.visitChildren(ctx)

    def visitContainerDeclarationType(self, ctx: ZigParser.ContainerDeclarationTypeContext):
        return self.visitChildren(ctx)

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
        return Expression(
            [keywords.SYM_MEMBERS] +
            fields + decls)

    def visitContainerUnit(self, ctx: ZigParser.ContainerUnitContext):
        return self.visitContainerMembers(ctx.containerMembers())

    def visitDeclaration(self, ctx: ZigParser.DeclarationContext):
        if ctx.fnProtoDeclTop():
            return self.visitFnProtoDeclTop(
                ctx.fnProtoDeclTop())
        elif ctx.varDeclarationTop():
            return self.visitVarDeclarationTop(
                ctx.varDeclarationTop())
        elif ctx.UsingNamespace():
            expr = self.visitExpression(ctx.expression())
            return Expression(
                [keywords.SYM_USING_NS, expr])
        else:
            raise ValueError

    def visitDesignatorExpression(self, ctx: ZigParser.DesignatorExpressionContext):
        if ctx.suffixOp():
            return self.visitSuffixOp(ctx.suffixOp())
        elif ctx.fnCallArguments():
            return self.visitFnCallArguments(ctx.fnCallArguments())
        else:
            raise ValueError

    def visitElseExpression(self, ctx: ZigParser.ElseExpressionContext):
            return self.visitChildren(ctx)

    def visitElseStatement(self, ctx: ZigParser.ElseStatementContext):
            return self.visitChildren(ctx)
        
    def visitEnumSpecifier(self, ctx: ZigParser.EnumSpecifierContext):
            return self.visitChildren(ctx)

    def visitErrorSetDeclaration(self, ctx: ZigParser.ErrorSetDeclarationContext):
        return self.visitChildren(ctx)

    def visitErrorUnionExpression(self, ctx: ZigParser.ErrorUnionExpressionContext):
        result = self.visitSuffixExpression(ctx.suffixExpression())
        if ctx.typeExpression():
            typeof = self.visitTypeExpression(ctx.typeExpression())
            return Expression([
                keywords.SYM_RESULT,
                result, typeof])
        return result

    # CodeBinaryOperatorExpression {
    #	left: CodeExpression,
    #	op: CodeBinaryOperatorType,
    #	right: CodeExpression,
    # }
    def visitExpression(self, ctx: ZigParser.ExpressionContext):
        return self.visitBoolOrExpression(ctx.boolOrExpression())

    def visitExpressionStatement(self, ctx: ZigParser.ExpressionStatementContext):
        if ctx.varDeclaration():
            # TODO add comptime
            return self.visitVarDeclaration(ctx.varDeclaration())
        elif ctx.assignExpression():
            return self.visitAssignExpression(ctx.assignExpression())
        else:
            raise ValueError
        
    def visitFieldDeclarationSpecifiers(self, ctx: ZigParser.FieldDeclarationSpecifiersContext):
            return self.visitChildren(ctx)

    def visitFieldInit(self, ctx: ZigParser.FieldInitContext):
        name = Symbol(ctx.Ident().symbol.text)
        expr = self.visitExpression(ctx.expression())
        return dict([(name, expr)])

    def visitFieldList(self, ctx: ZigParser.FieldListContext):
        # print("visitFieldList")
        return list(map(
            self.visitField,
            ctx.field()))

    def visitFieldName(self, ctx: ZigParser.FieldNameContext):
        return Symbol(ctx.Ident().symbol.text)

    # System.CodeDom.CodeMemberField {
    # 	Name: string,
    #	Type: CodeTypeReference,
    #	CustomAttributes: CodeAttributeDeclarationCollection,
    #	Comments: CodeCommentStatementCollection,
    # }
    def visitField(self, ctx: ZigParser.FieldContext):
            return self.visitChildren(ctx)

    def visitFloatingLiteral(self, ctx: ZigParser.FloatingLiteralContext):
        token = ctx.Float().symbol
        return float(token.text)

    def visitFnCallArguments(self, ctx: ZigParser.FnCallArgumentsContext):
        if ctx.argumentExpressionList():
            results = self.visitArgumentExpressionList(ctx.argumentExpressionList())
            return (lambda prim: Expression([prim] + results))
        else:
            return (lambda prim: Expression([prim]))
    
    def visitFnProtoDeclarationEx(self, ctx: ZigParser.FnProtoDeclarationExContext):
            return self.visitChildren(ctx)

    def visitFnProtoDeclaration(self, ctx: ZigParser.FnProtoDeclarationContext):
        retType = self.visitTypeExpression(ctx.typeExpression())
        name = Symbol(ctx.Ident().symbol.text)
        if ctx.Bang():
            retType = Expression(
                [keywords.SYM_RESULT,
                 keywords.SYM_ANYERROR,
                 retType])
        params = self.visitParameterDeclarationList(ctx.parameterDeclarationList())
        return Expression(
            [keywords.SYM_FN, name, params, retType])
        
    def visitFnProtoDeclarationSpecifiers(self, ctx: ZigParser.FnProtoDeclarationSpecifiersContext):
            return self.visitChildren(ctx)

    # System.CodeDom.CodeMemberMethod {
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
    def visitFnProtoDeclTop(self, ctx: ZigParser.FnProtoDeclTopContext):
        if ctx.fnProtoDeclaration():
            proto = self.visitFnProtoDeclaration(ctx.fnProtoDeclaration())
            if ctx.block():
                block = self.visitBlock(ctx.block())
                return Expression(list(proto) + [block])
            else:
                return proto

    def visitForArgumentsList(self, ctx: ZigParser.ForArgumentsListContext):
        return list(map(
            self.visitForItem,
            ctx.forItem()))

    def visitForExpression(self, ctx: ZigParser.ForExpressionContext):
        (args, payload) = self.visitForPrefix(ctx.forPrefix())
        elseStatements = [self.visitExpression(ctx.expression()[1])] \
            if ctx.Else() else []
        thenExpression = self.visitExpression(ctx.expression()[0])
        return Expression(
            [keywords.SYM_FOR_EXPR, args, payload,
             thenExpression] + elseStatements)

    def visitForItem(self, ctx: ZigParser.ForItemContext):
        return list(map(
            self.visitExpression,
            ctx.expression()))

    def visitForPrefix(self, ctx: ZigParser.ForPrefixContext):
        args = self.visitForArgumentsList(ctx.forArgumentsList())
        payload = self.visitPtrListPayload(ctx.ptrListPayload())
        return (args, payload)

    # CodeIterationStatement(
    #	InitStatement: CodeStatement,
    #	TestExpression: CodeExpression,
    #	IncrementStatement: CodeStatement,
    #	Statements: []CodeStatement)
    def visitForStatement(self, ctx: ZigParser.ForStatementContext):
        (args, payload) = self.visitForPrefix(ctx.forPrefix())
        elseStatements = [self.visitStatement(ctx.statement())] \
            if ctx.Else() else []
        if ctx.blockExpression():
            thenExpression = self.visitBlockExpression(ctx.blockExpression())
            return Expression(
                [keywords.SYM_FOR_STMT, args, payload,
                 thenExpression] + elseStatements)
        elif ctx.assignExpression():
            thenExpression = self.visitAssignExpression(ctx.assignExpression())
            return Expression(
                [keywords.SYM_FOR_STMT, args, payload,
                 thenExpression] + elseStatements)
        else:
            raise ValueError

    def visitForTypeExpression(self, ctx: ZigParser.ForTypeExpressionContext):
        (args, payload) = self.visitForPrefix(ctx.forPrefix())
        elseStatements = [self.visitTypeExpression(ctx.typeExpression()[1])] \
            if ctx.Else() else []
        thenExpression = self.visitTypeExpression(ctx.typeExpression()[0])
        return Expression(
            [keywords.SYM_FOR_TYPE, args, payload,
             thenExpression] + elseStatements)

    def visitGroupedExpression(self, ctx: ZigParser.GroupedExpressionContext):
        return self.visitExpression(ctx.expression())

    def visitIdentList(self, ctx: ZigParser.IdentListContext):
        return self.visitChildren(ctx)

    # CodeConditionStatement {
    #	Condition: CodeExpr,
    #	TrueStatements: []CodeStatement,  // Expr
    #	FalseStatements: []CodeStatement, // Expr
    # }
    def visitIfExpression(self, ctx: ZigParser.IfExpressionContext):
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

    def visitIfPrefix(self, ctx: ZigParser.IfPrefixContext):
        return tuple([
            self.visitCondExpression(ctx.condExpression()),
            self.visitPtrPayload(ctx.ptrPayload())
            if ctx.ptrPayload() else None])

    # CodeConditionStatement {
    #	Condition: CodeExpr,
    #	TrueStatements: []CodeStmt,
    #	TalseStatements: []CodeStmt,
    # }
    def visitIfStatement(self, ctx: ZigParser.IfStatementContext):
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
    #	TrueStatements: []CodeStatement,  // TypeExpr
    #	FalseStatements: []CodeStatement, // TypeExpr
    # }
    def visitIfTypeExpression(self, ctx: ZigParser.IfTypeExpressionContext):
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
            [keywords.SYM_IF_TYPE, condExpression]
            + payload2lambda(thenPayload, thenExpression)
            + payload2lambda(elsePayload, elseExpression))

    def visitInitList(self, ctx: ZigParser.InitListContext):
        if ctx.fieldInit():
            results = [
                self.visitFieldInit(node)
                for node in ctx.fieldInit()]
            results = dict(sum([
                list(result.items())
                for result in results
            ], []))
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

    def visitIntegerLiteral(self, ctx: ZigParser.IntegerLiteralContext):
        token = ctx.Integer().symbol
        return int(token.text)
    
    def visitIterationExpression(self, ctx: ZigParser.IterationExpressionContext):
            return self.visitChildren(ctx)
        
    def visitIterationStatement(self, ctx: ZigParser.IterationStatementContext):
            return self.visitChildren(ctx)
        
    def visitIterationTypeExpression(self, ctx: ZigParser.IterationTypeExpressionContext):
            return self.visitChildren(ctx)

    def visitLabeledExpression(self, ctx: ZigParser.LabeledExpressionContext):
        return self.visitLoopExpression(ctx.loopExpression())

    # CodeLabeledStatement {
    #	Label: string,
    #	Statement: CodeStatement,
    # }
    def visitLabeledStatement(self, ctx: ZigParser.LabeledStatementContext):
        result = None
        if ctx.block():
            result = self.visitBlock(ctx.block())
        elif ctx.loopStatement():
            result = self.visitLoopStatement(ctx.loopStatement())
        if ctx.blockLabel():
            # self.visitBlockLabel(ctx.blockLabel())
            raise ValueError
        return result

    def visitLabeledTypeExpression(self, ctx: ZigParser.LabeledTypeExpressionContext):
        result = None
        if ctx.block():
            result = self.visitBlock(ctx.block())
        elif ctx.loopStatement():
            result = self.visitLoopStatement(ctx.loopStatement())
        if ctx.blockLabel():
            # self.visitBlockLabel(ctx.blockLabel())
            raise ValueError
        return result

    def visitLineStringLiteral(self, ctx: ZigParser.LineStringLiteralContext):
        token = ctx.LineString().symbol
        return atom.zig_line_string_literal(token.text)

    def visitLinkSection(self, ctx: ZigParser.LinkSectionContext):
        return self.visitChildren(ctx)

    def visitLoopExpression(self, ctx: ZigParser.LoopExpressionContext):
        result = None
        if ctx.forExpression():
            result = self.visitForExpression(ctx.forExpression())
        elif ctx.whileExpression():
            result = self.visitWhileExpression(ctx.whileExpression())
        else:
            raise ValueError
        return result

    def visitLoopStatement(self, ctx: ZigParser.LoopStatementContext):
        result = None
        if ctx.forStatement():
            result = self.visitForStatement(ctx.forStatement())
        elif ctx.whileStatement():
            result = self.visitWhileStatement(ctx.whileStatement())
        else:
            raise ValueError
        return result

    def visitLoopTypeExpression(self, ctx: ZigParser.LoopTypeExpressionContext):
        result = None
        if ctx.forTypeExpression():
            result = self.visitForTypeExpression(ctx.forTypeExpression())
        elif ctx.whileTypeExpression():
            result = self.visitWhileTypeExpression(ctx.whileTypeExpression())
        else:
            raise ValueError
        return result

    # CodeBinaryOperatorType.Multiply
    # CodeBinaryOperatorType.Divide
    # CodeBinaryOperatorType.Modulus
    def visitMultiplyExpression(self, ctx: ZigParser.MultiplyExpressionContext):
        operators = [
            Symbol(op.children[0].symbol.text)
            for op in ctx.multiplyOp()]
        operands = list(map(
            self.visitPrefixExpression,
            ctx.prefixExpression()))
        if len(operators) == 1:
            return Expression([operators[0]] + operands)
        elif len(operators) == 0:
            return operands[0]
        else:
            raise ValueError

    def visitMultiplyOp(self, ctx:ZigParser.MultiplyOpContext):
        return self.visitChildren(ctx)

    def visitParameterDeclarationList(self, ctx: ZigParser.ParameterDeclarationListContext):
        parm_decls = list(map(
            self.visitParameterDeclaration,
            ctx.parameterDeclaration()))
        return Expression(
            [keywords.SYM_PARM_LIST] + parm_decls)

    def visitParameterDeclaration(self, ctx: ZigParser.ParameterDeclarationContext):
        if ctx.parameterDeclarationSpecifier():
            specs = [self.visitParameterDeclarationSpecifier(
                ctx.parameterDeclarationSpecifier())]
        else:
            specs = []
        if ctx.Ident():
            name = Symbol(ctx.Ident().symbol.text)
        else:
            name = Symbol("_")
        type_ = self.visitParameterType(ctx.parameterType())
        return Expression(
            [keywords.SYM_PARM, name, type_])

    def visitParameterDeclarationSpecifier(self, ctx: ZigParser.ParameterDeclarationSpecifierContext):
        if ctx.NoAlias():
            return keywords.SYM_NOALIAS
        elif ctx.CompTime():
            return keywords.SYM_COMPTIME
        else:
            raise ValueError

    def visitParameterType(self, ctx: ZigParser.ParameterTypeContext):
        if ctx.AnyType():
            return keywords.SYM_ANYTYPE
        elif ctx.typeExpression():
            return self.visitTypeExpression(ctx.typeExpression())
        else:
            raise ValueError

    def visitPayload(self, ctx: ZigParser.PayloadContext):
        name = Symbol(ctx.Ident().symbol.text)
        return Expression(
            [keywords.SYM_PAYLOAD, name])

    def visitPrefixExpression(self, ctx: ZigParser.PrefixExpressionContext):
        result = self.visitPrimaryExpression(ctx.primaryExpression())
        if ctx.prefixOp():
            # print("visitPrefixExpression,Prefix")
            pass
        elif ctx.Bang():
            # print("visitPrefixExpression,Prefix")
            pass
        else:
            return result
        
    def visitPrefixOp(self, ctx:ZigParser.PrefixOpContext):
        return self.visitChildren(ctx)

    def visitPrefixTypeOp(self, ctx: ZigParser.PrefixTypeOpContext):
        # TODO
        if ctx.Quest():
            #print("visitPrefixTypeOp.Quest")
            return lambda a: Expression([keywords.SYM_OPTION, a])
        elif ctx.AnyFrame():
            #print("visitPrefixTypeOp.AnyFrame")
            return lambda a: Expression([keywords.SYM_ANYFRAME, a])
        elif ctx.sliceTypeStart():
            #print("visitPrefixTypeOp.Slice")
            return self.visitSliceTypeStart(ctx.sliceTypeStart())
        elif ctx.ptrTypeStart():
            #print("visitPrefixTypeOp.Ptr")
            return self.visitPtrTypeStart(ctx.ptrTypeStart())
        elif ctx.arrayTypeStart():
            #print("visitPrefixTypeOp.Array")
            return self.visitArrayTypeStart(ctx.arrayTypeStart())
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

    def visitPrimaryExpression(self, ctx: ZigParser.PrimaryExpressionContext):
        if ctx.primaryBlockExpression():
            return self.visitPrimaryBlockExpression(
                ctx.primaryBlockExpression())
        elif ctx.compoundLiteral():
            return self.visitCompoundLiteral(
                ctx.compoundLiteral())
        elif ctx.asmExpression():
            return self.visitAsmExpression(
                ctx.asmExpression())
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

    def visitPtrIndexPayload(self, ctx: ZigParser.PtrIndexPayloadContext):
        name = Symbol(ctx.Ident()[0].symbol.text)
        return Expression(
            [keywords.SYM_PAYLOAD, name])

    def visitPtrListPayload(self, ctx: ZigParser.PtrListPayloadContext):
        name = Symbol(ctx.Ident()[0].symbol.text)
        return Expression(
            [keywords.SYM_PAYLOAD, name])

    def visitPtrPayload(self, ctx: ZigParser.PtrPayloadContext):
        # TODO handle ptr
        name = Symbol(ctx.Ident().symbol.text)
        return Expression(
            [keywords.SYM_PAYLOAD, name])

    def visitPtrTypeRest(self, ctx: ZigParser.PtrTypeRestContext):
        return self.visitChildren(ctx)

    def visitPtrTypeStart(self, ctx: ZigParser.PtrTypeStartContext):
        if ctx.LBrack():
            if ctx.LetterC():
                return lambda t: Expression([keywords.SYM_PTRS, t, keywords.SYM_C])
            elif ctx.Colon():
                expr = self.visitExpression(ctx.expression())
                return lambda t: Expression([keywords.SYM_PTRS, t, expr])
            else:
                return lambda t: Expression([keywords.SYM_PTRS, t])
        elif ctx.Star2():
            return lambda t: Expression([keywords.SYM_PTR2, t])
        elif ctx.Star():
            return lambda t: Expression([keywords.SYM_PTR, t])
        else:
            raise ValueError
        




















    def visitSelectionExpression(self, ctx: ZigParser.SelectionExpressionContext):
        if ctx.ifExpression():
            return self.visitIfExpression(ctx.ifExpression())
        elif ctx.switchExpression():
            return self.visitSwitchExpression(ctx.switchExpression())
        else:
            raise ValueError

    def visitSelectionStatement(self, ctx: ZigParser.SelectionStatementContext):
        if ctx.ifStatement():
            return self.visitIfStatement(ctx.ifStatement())
        elif ctx.switchExpression():
            return self.visitSwitchExpression(ctx.switchExpression())
        else:
            raise ValueError
        
    def visitSelectionTypeExpression(self, ctx: ZigParser.SelectionTypeExpressionContext):
        if ctx.ifTypeExpression():
            return self.visitIfTypeExpression(ctx.ifTypeExpression())
        elif ctx.switchExpression():
            return self.visitSwitchExpression(ctx.switchExpression())
        else:
            raise ValueError

    def visitSingleStringLiteral(self, ctx: ZigParser.SingleStringLiteralContext):
        token = ctx.SingleString().symbol
        return atom.zig_single_string_literal(token.text)

    # System.CodeDom.CodeTypeReferenceCollection(value: []CodeTypeReference)
    # System.CodeDom.CodeTypeReference(type: Type)
    # System.CodeDom.CodeObject(userData: ListDictionary)


    # RustAST: Arg
    # FnArgType := struct { Name: str, Type: Type }

    # RustAST: Signature
    # FnSigType := struct { Params: []FnArgType, Returns: []FnArgType }


    # System.CodeDom.CodeMemberProperty {
    # 	Name: string,
    #	Parameters: CodeParameterDeclarationExpressionCollection,
    # 	GetStatements: CodeStatementCollection,
    # 	SetStatements: CodeStatementCollection,
    #	CustomAttributes: CodeAttributeDeclarationCollection,
    #	Comments: CodeCommentStatementCollection,
    # }

    def visitSliceTypeRest(self, ctx: ZigParser.SliceTypeRestContext):
        return self.visitChildren(ctx)

    def visitSliceTypeStart(self, ctx: ZigParser.SliceTypeStartContext):
        exprs = [self.visitExpression(ctx.expression())] \
            if ctx.expression() else []
        return lambda t: Expression(
            [keywords.SYM_SLICE_TYPE, t] + exprs)

    def visitStart(self, ctx:ZigParser.StartContext):
        return self.visitContainerUnit(ctx.containerUnit())
    
    def visitStatement(self, ctx: ZigParser.StatementContext):
        if ctx.expressionStatement():
            return self.visitExpressionStatement(ctx.expressionStatement())
        elif ctx.primaryBlockStatement():
            return self.visitPrimaryBlockStatement(ctx.primaryBlockStatement())
        else:
            raise ValueError
            
    def visitStringList(self, ctx: ZigParser.StringListContext):
        return self.visitChildren(ctx)

    def visitStructOrUnionSpecifier(self, ctx: ZigParser.StructOrUnionSpecifierContext):
            return self.visitChildren(ctx)

    def visitSuffixExpression(self, ctx: ZigParser.SuffixExpressionContext):
        # print("visitSuffixExpression")
        if ctx.Async():
            # print("visitSuffixExpression ASYNC!")
            raise ValueError
        else:
            primary = self.visitPrimaryTypeExpression(ctx.primaryTypeExpression())
            designators = list(map(
                self.visitDesignatorExpression,
                ctx.designatorExpression()))
            for designator in designators:
                primary = designator(primary)
            return primary
            # if len(ctx.children
            # if ctx.suffixOp():
            #     print("visitSuffixExpression SUFFIX!", ctx.suffixOp())
            #     raise ValueError
            # else:
            #     return self.visitPrimaryTypeExpression(ctx.primaryTypeExpression()

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
            exprs = list(map(
                self.visitExpression,
                ctx.expression()))
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

    def visitSwitchCase(self, ctx: ZigParser.SwitchCaseContext):
        items = list(map(
            self.visitSwitchItem,
            ctx.switchItem()))
        if ctx.Else():
            return Expression([
                keywords.SYM_SWITCH_ELSE])
        else:
            return Expression([
                keywords.SYM_SWITCH_CASE, tuple(items)])

    # System.Linq.Expression.ExpressionType.Switch
    def visitSwitchExpression(self, ctx: ZigParser.SwitchExpressionContext):
        expr = self.visitExpression(ctx.expression())
        prongs = self.visitSwitchProngList(ctx.switchProngList())
        return Expression(
            [keywords.SYM_SWITCH_EXPR, expr] + prongs)

    def visitSwitchItem(self, ctx: ZigParser.SwitchItemContext):
        items = list(map(
            self.visitExpression,
            ctx.expression()))
        if len(items) == 2:
            return Expression(
                [keywords.SYM_SWITCH_RNG] + items)
        elif len(items) == 1:
            return items[0]
        else:
            raise ValueError

    def visitSwitchProngList(self, ctx: ZigParser.SwitchProngListContext):
        prongs = list(map(
            self.visitSwitchProng,
            ctx.switchProng()))
        return prongs

    def visitSwitchProng(self, ctx: ZigParser.SwitchProngContext):
        cases = self.visitSwitchCase(ctx.switchCase())
        payloads = [self.visitPtrIndexPayload(ctx.ptrIndexPayload())] \
            if ctx.ptrIndexPayload() else []
        expr = self.visitAssignExpression(ctx.assignExpression())
        return Expression(
            [cases[0]] + list(cases[1:]) + payloads + [expr])

    def visitTestDeclaration(self, ctx: ZigParser.TestDeclarationContext):
            return self.visitChildren(ctx)
    def visitThenExpression(self, ctx: ZigParser.ThenExpressionContext):
            return self.visitChildren(ctx)

    def visitTypeExpression(self, ctx: ZigParser.TypeExpressionContext):
        result = self.visitErrorUnionExpression(ctx.errorUnionExpression())
        # TODO add this
        prefixes = list(map(
            self.visitPrefixTypeOp,
            ctx.prefixTypeOp()))
        if ctx.prefixTypeOp():
            for pre in reversed(prefixes):
                result = pre(result)
        # for prefix in reverse(prefixes):
        #     result = Expression(
        #         Symbol(prefix.text), result)
        return result

    def visitTypeName(self, ctx: ZigParser.TypeNameContext):
        return Symbol(ctx.Ident().symbol.text)

    def visitVarDeclarationEx(self, ctx: ZigParser.VarDeclarationExContext):
            return self.visitChildren(ctx)

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

    def visitVarDeclarationSpecifiers(self, ctx: ZigParser.VarDeclarationSpecifiersContext):
            return self.visitChildren(ctx)

    # CodeArgumentReferenceExpression {
    # 	ParameterName: string,
    # }
    def visitVarDeclarationTop(self, ctx: ZigParser.VarDeclarationTopContext):
        if ctx.varDeclaration():
            return self.visitVarDeclaration(ctx.varDeclaration())

    # CodeVariableReferenceExpression {
    #	VariableName: string,
    # }
    def visitVarName(self, ctx: ZigParser.VarNameContext):
        return Symbol(ctx.Ident().symbol.text)

    def visitWhileContinueExpression(self, ctx: ZigParser.WhileContinueExpressionContext):
        return self.visitAssignExpression(ctx.assignExpression())

    # System.Linq.Expression.ExpressionType.Loop
    def visitWhileExpression(self, ctx: ZigParser.WhileExpressionContext):
        (condExpr, payloads, continueExprs) = self.visitWhilePrefix(ctx.whilePrefix())
        elseStatements = [self.visitExpression(ctx.expression()[1])] \
            if ctx.Else() else []
        thenExpression = self.visitExpression(ctx.expression()[0])
        return Expression(
            [keywords.SYM_WHILE_EXPR, condExpr, payloads, continueExprs,
             thenExpression] + elseStatements)
        return self.visitChildren(ctx)

    def visitWhilePrefix(self, ctx: ZigParser.WhilePrefixContext):
        condExpr = self.visitCondExpression(ctx.condExpression())
        payloads = [self.visitPtrPayload(ctx.ptrPayload())] \
            if ctx.ptrPayload() else []
        continueExprs = [
            self.visitWhileContinueExpression(
                ctx.whileContinueExpression())] \
            if ctx.whileContinueExpression() else []
        return (condExpr, payloads, continueExprs)

    def visitWhileStatement(self, ctx: ZigParser.WhileStatementContext):
        (condExpr, payloads, continueExprs) = self.visitWhilePrefix(ctx.whilePrefix())
        elseStatements = [self.visitStatement(ctx.statement())] \
            if ctx.Else() else []
        if ctx.blockExpression():
            thenExpression = self.visitBlockExpression(ctx.blockExpression())
        elif ctx.assignExpression():
            thenExpression = self.visitAssignExpression(ctx.assignExpression())
        else:
            raise ValueError
        return Expression(
            [keywords.SYM_WHILE_STMT, condExpr, payloads, continueExprs,
             thenExpression] + elseStatements)

    def visitWhileTypeExpression(self, ctx: ZigParser.WhileTypeExpressionContext):
        (condExpr, payloads, continueExprs) = self.visitWhilePrefix(ctx.whilePrefix())
        elseStatements = [self.visitTypeExpression(ctx.typeExpression()[1])] \
            if ctx.Else() else []
        thenExpression = self.visitTypeExpression(ctx.typeExpression()[0])
        return Expression(
            [keywords.SYM_WHILE_TYPE, condExpr, payloads, continueExprs,
             thenExpression] + elseStatements)
