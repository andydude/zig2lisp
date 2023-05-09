# Generated from ZigParser.g4 by ANTLR 4.12.0
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .ZigParser import ZigParser
else:
    from ZigParser import ZigParser

# This class defines a complete generic visitor for a parse tree produced by ZigParser.

class ZigParserVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by ZigParser#start.
    def visitStart(self, ctx:ZigParser.StartContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#primaryTypeExpression.
    def visitPrimaryTypeExpression(self, ctx:ZigParser.PrimaryTypeExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#primaryExpression.
    def visitPrimaryExpression(self, ctx:ZigParser.PrimaryExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#asmExpression.
    def visitAsmExpression(self, ctx:ZigParser.AsmExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#asmOutput.
    def visitAsmOutput(self, ctx:ZigParser.AsmOutputContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#asmOutputItem.
    def visitAsmOutputItem(self, ctx:ZigParser.AsmOutputItemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#asmInput.
    def visitAsmInput(self, ctx:ZigParser.AsmInputContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#asmInputItem.
    def visitAsmInputItem(self, ctx:ZigParser.AsmInputItemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#asmClobbers.
    def visitAsmClobbers(self, ctx:ZigParser.AsmClobbersContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#asmOutputList.
    def visitAsmOutputList(self, ctx:ZigParser.AsmOutputListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#asmInputList.
    def visitAsmInputList(self, ctx:ZigParser.AsmInputListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#suffixExpression.
    def visitSuffixExpression(self, ctx:ZigParser.SuffixExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#designatorExpression.
    def visitDesignatorExpression(self, ctx:ZigParser.DesignatorExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#fnCallArguments.
    def visitFnCallArguments(self, ctx:ZigParser.FnCallArgumentsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#argumentExpressionList.
    def visitArgumentExpressionList(self, ctx:ZigParser.ArgumentExpressionListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#compoundLiteral.
    def visitCompoundLiteral(self, ctx:ZigParser.CompoundLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#expression.
    def visitExpression(self, ctx:ZigParser.ExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#boolOrExpression.
    def visitBoolOrExpression(self, ctx:ZigParser.BoolOrExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#boolAndExpression.
    def visitBoolAndExpression(self, ctx:ZigParser.BoolAndExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#compareExpression.
    def visitCompareExpression(self, ctx:ZigParser.CompareExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#bitwiseExpression.
    def visitBitwiseExpression(self, ctx:ZigParser.BitwiseExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#bitShiftExpression.
    def visitBitShiftExpression(self, ctx:ZigParser.BitShiftExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#additionExpression.
    def visitAdditionExpression(self, ctx:ZigParser.AdditionExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#additionOp.
    def visitAdditionOp(self, ctx:ZigParser.AdditionOpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#multiplyExpression.
    def visitMultiplyExpression(self, ctx:ZigParser.MultiplyExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#multiplyOp.
    def visitMultiplyOp(self, ctx:ZigParser.MultiplyOpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#prefixExpression.
    def visitPrefixExpression(self, ctx:ZigParser.PrefixExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#prefixOp.
    def visitPrefixOp(self, ctx:ZigParser.PrefixOpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#constantExpression.
    def visitConstantExpression(self, ctx:ZigParser.ConstantExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#declaration.
    def visitDeclaration(self, ctx:ZigParser.DeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#typeName.
    def visitTypeName(self, ctx:ZigParser.TypeNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#containerDeclaration.
    def visitContainerDeclaration(self, ctx:ZigParser.ContainerDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#containerDeclarationAuto.
    def visitContainerDeclarationAuto(self, ctx:ZigParser.ContainerDeclarationAutoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#containerDeclarationType.
    def visitContainerDeclarationType(self, ctx:ZigParser.ContainerDeclarationTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#structOrUnionSpecifier.
    def visitStructOrUnionSpecifier(self, ctx:ZigParser.StructOrUnionSpecifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#fieldList.
    def visitFieldList(self, ctx:ZigParser.FieldListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#field.
    def visitField(self, ctx:ZigParser.FieldContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#fieldDeclarationSpecifiers.
    def visitFieldDeclarationSpecifiers(self, ctx:ZigParser.FieldDeclarationSpecifiersContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#fieldName.
    def visitFieldName(self, ctx:ZigParser.FieldNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#enumSpecifier.
    def visitEnumSpecifier(self, ctx:ZigParser.EnumSpecifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#fnProtoDeclaration.
    def visitFnProtoDeclaration(self, ctx:ZigParser.FnProtoDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#fnProtoDeclarationSpecifiers.
    def visitFnProtoDeclarationSpecifiers(self, ctx:ZigParser.FnProtoDeclarationSpecifiersContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#parameterDeclarationList.
    def visitParameterDeclarationList(self, ctx:ZigParser.ParameterDeclarationListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#parameterDeclaration.
    def visitParameterDeclaration(self, ctx:ZigParser.ParameterDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#parameterDeclarationSpecifier.
    def visitParameterDeclarationSpecifier(self, ctx:ZigParser.ParameterDeclarationSpecifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#parameterType.
    def visitParameterType(self, ctx:ZigParser.ParameterTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#typeExpression.
    def visitTypeExpression(self, ctx:ZigParser.TypeExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#errorUnionExpression.
    def visitErrorUnionExpression(self, ctx:ZigParser.ErrorUnionExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#initList.
    def visitInitList(self, ctx:ZigParser.InitListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#statement.
    def visitStatement(self, ctx:ZigParser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#primaryBlockStatement.
    def visitPrimaryBlockStatement(self, ctx:ZigParser.PrimaryBlockStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#primaryBlockExpression.
    def visitPrimaryBlockExpression(self, ctx:ZigParser.PrimaryBlockExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#primaryTypeStatement.
    def visitPrimaryTypeStatement(self, ctx:ZigParser.PrimaryTypeStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#primaryTypeDeclaration.
    def visitPrimaryTypeDeclaration(self, ctx:ZigParser.PrimaryTypeDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#errorSetDeclaration.
    def visitErrorSetDeclaration(self, ctx:ZigParser.ErrorSetDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#identList.
    def visitIdentList(self, ctx:ZigParser.IdentListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#compoundStatement.
    def visitCompoundStatement(self, ctx:ZigParser.CompoundStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#compoundExpression.
    def visitCompoundExpression(self, ctx:ZigParser.CompoundExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#compoundTypeExpression.
    def visitCompoundTypeExpression(self, ctx:ZigParser.CompoundTypeExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#builtinCallExpression.
    def visitBuiltinCallExpression(self, ctx:ZigParser.BuiltinCallExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#expressionStatement.
    def visitExpressionStatement(self, ctx:ZigParser.ExpressionStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#selectionStatement.
    def visitSelectionStatement(self, ctx:ZigParser.SelectionStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#selectionExpression.
    def visitSelectionExpression(self, ctx:ZigParser.SelectionExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#selectionTypeExpression.
    def visitSelectionTypeExpression(self, ctx:ZigParser.SelectionTypeExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#ifStatement.
    def visitIfStatement(self, ctx:ZigParser.IfStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#ifExpression.
    def visitIfExpression(self, ctx:ZigParser.IfExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#ifTypeExpression.
    def visitIfTypeExpression(self, ctx:ZigParser.IfTypeExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#ifPrefix.
    def visitIfPrefix(self, ctx:ZigParser.IfPrefixContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#condExpression.
    def visitCondExpression(self, ctx:ZigParser.CondExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#thenExpression.
    def visitThenExpression(self, ctx:ZigParser.ThenExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#elseExpression.
    def visitElseExpression(self, ctx:ZigParser.ElseExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#elseStatement.
    def visitElseStatement(self, ctx:ZigParser.ElseStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#switchExpression.
    def visitSwitchExpression(self, ctx:ZigParser.SwitchExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#iterationStatement.
    def visitIterationStatement(self, ctx:ZigParser.IterationStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#iterationExpression.
    def visitIterationExpression(self, ctx:ZigParser.IterationExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#iterationTypeExpression.
    def visitIterationTypeExpression(self, ctx:ZigParser.IterationTypeExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#labeledStatement.
    def visitLabeledStatement(self, ctx:ZigParser.LabeledStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#labeledExpression.
    def visitLabeledExpression(self, ctx:ZigParser.LabeledExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#labeledTypeExpression.
    def visitLabeledTypeExpression(self, ctx:ZigParser.LabeledTypeExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#loopStatement.
    def visitLoopStatement(self, ctx:ZigParser.LoopStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#loopExpression.
    def visitLoopExpression(self, ctx:ZigParser.LoopExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#loopTypeExpression.
    def visitLoopTypeExpression(self, ctx:ZigParser.LoopTypeExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#forStatement.
    def visitForStatement(self, ctx:ZigParser.ForStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#forExpression.
    def visitForExpression(self, ctx:ZigParser.ForExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#forTypeExpression.
    def visitForTypeExpression(self, ctx:ZigParser.ForTypeExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#forPrefix.
    def visitForPrefix(self, ctx:ZigParser.ForPrefixContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#whileStatement.
    def visitWhileStatement(self, ctx:ZigParser.WhileStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#whileExpression.
    def visitWhileExpression(self, ctx:ZigParser.WhileExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#whileTypeExpression.
    def visitWhileTypeExpression(self, ctx:ZigParser.WhileTypeExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#whilePrefix.
    def visitWhilePrefix(self, ctx:ZigParser.WhilePrefixContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#blockExpressionStatement.
    def visitBlockExpressionStatement(self, ctx:ZigParser.BlockExpressionStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#blockExpression.
    def visitBlockExpression(self, ctx:ZigParser.BlockExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#assignExpression.
    def visitAssignExpression(self, ctx:ZigParser.AssignExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#breakLabel.
    def visitBreakLabel(self, ctx:ZigParser.BreakLabelContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#blockLabel.
    def visitBlockLabel(self, ctx:ZigParser.BlockLabelContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#block.
    def visitBlock(self, ctx:ZigParser.BlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#integerLiteral.
    def visitIntegerLiteral(self, ctx:ZigParser.IntegerLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#floatingLiteral.
    def visitFloatingLiteral(self, ctx:ZigParser.FloatingLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#charLiteral.
    def visitCharLiteral(self, ctx:ZigParser.CharLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#singleStringLiteral.
    def visitSingleStringLiteral(self, ctx:ZigParser.SingleStringLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#lineStringLiteral.
    def visitLineStringLiteral(self, ctx:ZigParser.LineStringLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#groupedExpression.
    def visitGroupedExpression(self, ctx:ZigParser.GroupedExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#fieldInit.
    def visitFieldInit(self, ctx:ZigParser.FieldInitContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#whileContinueExpression.
    def visitWhileContinueExpression(self, ctx:ZigParser.WhileContinueExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#linkSection.
    def visitLinkSection(self, ctx:ZigParser.LinkSectionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#addrSpace.
    def visitAddrSpace(self, ctx:ZigParser.AddrSpaceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#callConv.
    def visitCallConv(self, ctx:ZigParser.CallConvContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#payload.
    def visitPayload(self, ctx:ZigParser.PayloadContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#ptrPayload.
    def visitPtrPayload(self, ctx:ZigParser.PtrPayloadContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#ptrIndexPayload.
    def visitPtrIndexPayload(self, ctx:ZigParser.PtrIndexPayloadContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#ptrListPayload.
    def visitPtrListPayload(self, ctx:ZigParser.PtrListPayloadContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#switchProng.
    def visitSwitchProng(self, ctx:ZigParser.SwitchProngContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#switchCase.
    def visitSwitchCase(self, ctx:ZigParser.SwitchCaseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#switchItem.
    def visitSwitchItem(self, ctx:ZigParser.SwitchItemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#forArgumentsList.
    def visitForArgumentsList(self, ctx:ZigParser.ForArgumentsListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#forItem.
    def visitForItem(self, ctx:ZigParser.ForItemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#assignOpExpression.
    def visitAssignOpExpression(self, ctx:ZigParser.AssignOpExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#compareOpExpression.
    def visitCompareOpExpression(self, ctx:ZigParser.CompareOpExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#bitwiseOpExpression.
    def visitBitwiseOpExpression(self, ctx:ZigParser.BitwiseOpExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#bitwiseKwExpression.
    def visitBitwiseKwExpression(self, ctx:ZigParser.BitwiseKwExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#prefixTypeOp.
    def visitPrefixTypeOp(self, ctx:ZigParser.PrefixTypeOpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#arrayTypeStart.
    def visitArrayTypeStart(self, ctx:ZigParser.ArrayTypeStartContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#sliceTypeStart.
    def visitSliceTypeStart(self, ctx:ZigParser.SliceTypeStartContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#sliceTypeRest.
    def visitSliceTypeRest(self, ctx:ZigParser.SliceTypeRestContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#ptrTypeStart.
    def visitPtrTypeStart(self, ctx:ZigParser.PtrTypeStartContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#ptrTypeRest.
    def visitPtrTypeRest(self, ctx:ZigParser.PtrTypeRestContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#suffixOp.
    def visitSuffixOp(self, ctx:ZigParser.SuffixOpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#byteAlign.
    def visitByteAlign(self, ctx:ZigParser.ByteAlignContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#byteAlign3.
    def visitByteAlign3(self, ctx:ZigParser.ByteAlign3Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#switchProngList.
    def visitSwitchProngList(self, ctx:ZigParser.SwitchProngListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#stringList.
    def visitStringList(self, ctx:ZigParser.StringListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#containerUnit.
    def visitContainerUnit(self, ctx:ZigParser.ContainerUnitContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#containerMembers.
    def visitContainerMembers(self, ctx:ZigParser.ContainerMembersContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#containerDeclarationList.
    def visitContainerDeclarationList(self, ctx:ZigParser.ContainerDeclarationListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#fnProtoDeclTop.
    def visitFnProtoDeclTop(self, ctx:ZigParser.FnProtoDeclTopContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#varDeclarationTop.
    def visitVarDeclarationTop(self, ctx:ZigParser.VarDeclarationTopContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#fnProtoDeclarationEx.
    def visitFnProtoDeclarationEx(self, ctx:ZigParser.FnProtoDeclarationExContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#varDeclarationEx.
    def visitVarDeclarationEx(self, ctx:ZigParser.VarDeclarationExContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#varName.
    def visitVarName(self, ctx:ZigParser.VarNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#varDeclaration.
    def visitVarDeclaration(self, ctx:ZigParser.VarDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#varDeclarationSpecifiers.
    def visitVarDeclarationSpecifiers(self, ctx:ZigParser.VarDeclarationSpecifiersContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#testDeclaration.
    def visitTestDeclaration(self, ctx:ZigParser.TestDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#compTimeDeclaration.
    def visitCompTimeDeclaration(self, ctx:ZigParser.CompTimeDeclarationContext):
        return self.visitChildren(ctx)



del ZigParser