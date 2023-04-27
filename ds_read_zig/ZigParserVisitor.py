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


    # Visit a parse tree produced by ZigParser#members.
    def visitMembers(self, ctx:ZigParser.MembersContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#declaration.
    def visitDeclaration(self, ctx:ZigParser.DeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#testDecl.
    def visitTestDecl(self, ctx:ZigParser.TestDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#comptimeDecl.
    def visitComptimeDecl(self, ctx:ZigParser.ComptimeDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#decl.
    def visitDecl(self, ctx:ZigParser.DeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#fnProtoDeclEx.
    def visitFnProtoDeclEx(self, ctx:ZigParser.FnProtoDeclExContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#varDeclEx.
    def visitVarDeclEx(self, ctx:ZigParser.VarDeclExContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#decl2.
    def visitDecl2(self, ctx:ZigParser.Decl2Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#fnProto.
    def visitFnProto(self, ctx:ZigParser.FnProtoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#varName.
    def visitVarName(self, ctx:ZigParser.VarNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#varDecl.
    def visitVarDecl(self, ctx:ZigParser.VarDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#fieldName.
    def visitFieldName(self, ctx:ZigParser.FieldNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#field.
    def visitField(self, ctx:ZigParser.FieldContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#stmt.
    def visitStmt(self, ctx:ZigParser.StmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#elseStmt.
    def visitElseStmt(self, ctx:ZigParser.ElseStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#ifStmt.
    def visitIfStmt(self, ctx:ZigParser.IfStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#labeledStmt.
    def visitLabeledStmt(self, ctx:ZigParser.LabeledStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#loopStmt.
    def visitLoopStmt(self, ctx:ZigParser.LoopStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#forStmt.
    def visitForStmt(self, ctx:ZigParser.ForStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#whileStmt.
    def visitWhileStmt(self, ctx:ZigParser.WhileStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#blockExprStmt.
    def visitBlockExprStmt(self, ctx:ZigParser.BlockExprStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#blockExpr.
    def visitBlockExpr(self, ctx:ZigParser.BlockExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#assignExpr.
    def visitAssignExpr(self, ctx:ZigParser.AssignExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#expr.
    def visitExpr(self, ctx:ZigParser.ExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#boolOrExpr.
    def visitBoolOrExpr(self, ctx:ZigParser.BoolOrExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#boolAndExpr.
    def visitBoolAndExpr(self, ctx:ZigParser.BoolAndExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#compareExpr.
    def visitCompareExpr(self, ctx:ZigParser.CompareExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#bitwiseExpr.
    def visitBitwiseExpr(self, ctx:ZigParser.BitwiseExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#bitShiftExpr.
    def visitBitShiftExpr(self, ctx:ZigParser.BitShiftExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#additionExpr.
    def visitAdditionExpr(self, ctx:ZigParser.AdditionExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#multiplyExpr.
    def visitMultiplyExpr(self, ctx:ZigParser.MultiplyExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#prefixExpr.
    def visitPrefixExpr(self, ctx:ZigParser.PrefixExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#breakLabel.
    def visitBreakLabel(self, ctx:ZigParser.BreakLabelContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#blockLabel.
    def visitBlockLabel(self, ctx:ZigParser.BlockLabelContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#primaryExpr.
    def visitPrimaryExpr(self, ctx:ZigParser.PrimaryExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#thenExpr.
    def visitThenExpr(self, ctx:ZigParser.ThenExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#elseExpr.
    def visitElseExpr(self, ctx:ZigParser.ElseExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#ifExpr.
    def visitIfExpr(self, ctx:ZigParser.IfExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#block.
    def visitBlock(self, ctx:ZigParser.BlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#loopExpr.
    def visitLoopExpr(self, ctx:ZigParser.LoopExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#forExpr.
    def visitForExpr(self, ctx:ZigParser.ForExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#whileExpr.
    def visitWhileExpr(self, ctx:ZigParser.WhileExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#curlySuffixExpr.
    def visitCurlySuffixExpr(self, ctx:ZigParser.CurlySuffixExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#initList.
    def visitInitList(self, ctx:ZigParser.InitListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#typeExpr.
    def visitTypeExpr(self, ctx:ZigParser.TypeExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#errorUnionExpr.
    def visitErrorUnionExpr(self, ctx:ZigParser.ErrorUnionExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#suffixExpr.
    def visitSuffixExpr(self, ctx:ZigParser.SuffixExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#designatorExpr.
    def visitDesignatorExpr(self, ctx:ZigParser.DesignatorExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#typeName.
    def visitTypeName(self, ctx:ZigParser.TypeNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#compTimeTypeExpr.
    def visitCompTimeTypeExpr(self, ctx:ZigParser.CompTimeTypeExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#primaryTypeExpr.
    def visitPrimaryTypeExpr(self, ctx:ZigParser.PrimaryTypeExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#primaryBiCall.
    def visitPrimaryBiCall(self, ctx:ZigParser.PrimaryBiCallContext):
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


    # Visit a parse tree produced by ZigParser#errorSetDecl.
    def visitErrorSetDecl(self, ctx:ZigParser.ErrorSetDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#groupedExpr.
    def visitGroupedExpr(self, ctx:ZigParser.GroupedExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#ifTypeExpr.
    def visitIfTypeExpr(self, ctx:ZigParser.IfTypeExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#labeledTypeExpr.
    def visitLabeledTypeExpr(self, ctx:ZigParser.LabeledTypeExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#loopTypeExpr.
    def visitLoopTypeExpr(self, ctx:ZigParser.LoopTypeExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#forTypeExpr.
    def visitForTypeExpr(self, ctx:ZigParser.ForTypeExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#whileTypeExpr.
    def visitWhileTypeExpr(self, ctx:ZigParser.WhileTypeExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#switchExpr.
    def visitSwitchExpr(self, ctx:ZigParser.SwitchExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#fieldInit.
    def visitFieldInit(self, ctx:ZigParser.FieldInitContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#whileContinueExpr.
    def visitWhileContinueExpr(self, ctx:ZigParser.WhileContinueExprContext):
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


    # Visit a parse tree produced by ZigParser#paramDecl.
    def visitParamDecl(self, ctx:ZigParser.ParamDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#paramType.
    def visitParamType(self, ctx:ZigParser.ParamTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#condExpr.
    def visitCondExpr(self, ctx:ZigParser.CondExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#ifPrefix.
    def visitIfPrefix(self, ctx:ZigParser.IfPrefixContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#whilePrefix.
    def visitWhilePrefix(self, ctx:ZigParser.WhilePrefixContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#forPrefix.
    def visitForPrefix(self, ctx:ZigParser.ForPrefixContext):
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


    # Visit a parse tree produced by ZigParser#assignOpExpr.
    def visitAssignOpExpr(self, ctx:ZigParser.AssignOpExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#compareOpExpr.
    def visitCompareOpExpr(self, ctx:ZigParser.CompareOpExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#bitwiseOpExpr.
    def visitBitwiseOpExpr(self, ctx:ZigParser.BitwiseOpExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#bitwiseKwExpr.
    def visitBitwiseKwExpr(self, ctx:ZigParser.BitwiseKwExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#prefixTypeOp.
    def visitPrefixTypeOp(self, ctx:ZigParser.PrefixTypeOpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#sliceTypeRest.
    def visitSliceTypeRest(self, ctx:ZigParser.SliceTypeRestContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#ptrTypeRest.
    def visitPtrTypeRest(self, ctx:ZigParser.PtrTypeRestContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#suffixOp.
    def visitSuffixOp(self, ctx:ZigParser.SuffixOpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#fnCallArguments.
    def visitFnCallArguments(self, ctx:ZigParser.FnCallArgumentsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#sliceTypeStart.
    def visitSliceTypeStart(self, ctx:ZigParser.SliceTypeStartContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#ptrTypeStart.
    def visitPtrTypeStart(self, ctx:ZigParser.PtrTypeStartContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#arrayTypeStart.
    def visitArrayTypeStart(self, ctx:ZigParser.ArrayTypeStartContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#declAuto.
    def visitDeclAuto(self, ctx:ZigParser.DeclAutoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#declType.
    def visitDeclType(self, ctx:ZigParser.DeclTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#byteAlign.
    def visitByteAlign(self, ctx:ZigParser.ByteAlignContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#identList.
    def visitIdentList(self, ctx:ZigParser.IdentListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#switchProngList.
    def visitSwitchProngList(self, ctx:ZigParser.SwitchProngListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#stringList.
    def visitStringList(self, ctx:ZigParser.StringListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#paramDeclList.
    def visitParamDeclList(self, ctx:ZigParser.ParamDeclListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#exprList.
    def visitExprList(self, ctx:ZigParser.ExprListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ZigParser#fieldList.
    def visitFieldList(self, ctx:ZigParser.FieldListContext):
        return self.visitChildren(ctx)



del ZigParser