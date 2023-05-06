parser grammar ZigParser;
options { tokenVocab = ZigLexer; }

// Non-standard
start
	: containerUnit
	;

// SS 6.5.1.0.1 primary-expression
primaryTypeExpression
	: AnyFrame
	| Unreachable
	| typeName
	| constantExpression // C-expression-like
	| groupedExpression
	| primaryTypeStatement // C-statement-like
	| primaryTypeDeclaration // C-declaration-like
	;

// SS 6.5.1.0.1 primary-expression
primaryExpression
	: asmExpression
	| primaryBlockExpression
	| compoundLiteral
	;

asmExpression
	: Asm Volatile? LPar expression asmOutput? RPar
	;

asmOutput
	: Colon asmOutputList asmInput?
	;

asmOutputItem
	: LBrack Ident RBrack SingleString
	  LPar (MinusArrow typeExpression / Ident) RPar
	;

asmInput
	: Colon asmInputList asmClobbers?
	;

asmInputItem
	: LBrack Ident RBrack SingleString
	  LPar expression RPar
	;

asmClobbers
	: Colon stringList
	;

asmOutputList
	: (asmOutputItem Comma)* asmOutputItem?
	;

asmInputList
	: (asmInputItem Comma)* asmInputItem?
	;

// SS 6.5.2.0.1 postfix-expression
suffixExpression
	: Async primaryTypeExpression suffixOp* fnCallArguments
	| primaryTypeExpression designatorExpression*
	;

// Non-standard
designatorExpression
	: suffixOp
	| fnCallArguments
	;

// Non-standard
fnCallArguments
	: LPar argumentExpressionList RPar
	;

// SS 6.5.2.0.2 argument-expression-list
argumentExpressionList
	// expression? (Comma expression)* Comma?
	: (expression Comma)* expression
	;

// SS 6.5.2.5.1 compound-literal
// curlySuffixExpression
compoundLiteral
	: typeExpression initList?
	;

// SS 6.5.17.0.1 expression
expression
	: boolOrExpression
	;

boolOrExpression
	: boolAndExpression (Or boolAndExpression)*
	;

boolAndExpression
	: compareExpression (And compareExpression)*
	;

compareExpression
	: bitwiseExpression (compareOpExpression bitwiseExpression)*
	;

bitwiseExpression
	: bitShiftExpression (bitwiseOpExpression bitShiftExpression)*
	;

bitShiftExpression
	: additionExpression (BitShiftOp additionExpression)*
	;

additionExpression
	: multiplyExpression (AdditionOp multiplyExpression)*
	;

multiplyExpression
	: prefixExpression (MultiplyOp prefixExpression)*
	;

prefixExpression
	: (PrefixOp* | Bang) primaryExpression
	;

// SS 6.6.0.0.1 constant-expression
constantExpression
	: integerLiteral
	| floatingLiteral
	| charLiteral
	| singleStringLiteral
	| lineStringLiteral
	;

//    # System.Linq.Expression.ExpressionType.ArrayLength
//    # System.Linq.Expression.ExpressionType.ArrayIndex
//    # System.Linq.Expression.ExpressionType.Call
//    # System.Linq.Expression.ExpressionType.Coalesce
//    # System.Linq.Expression.ExpressionType.Conditional
//    # System.Linq.Expression.ExpressionType.Constant
//    # System.Linq.Expression.ExpressionType.Convert
//    # System.Linq.Expression.ExpressionType.ConvertChecked
//    # System.Linq.Expression.ExpressionType.Divide
//    # System.Linq.Expression.ExpressionType.Equal
//    # System.Linq.Expression.ExpressionType.GreaterThan
//    # System.Linq.Expression.ExpressionType.GreaterThanOrEqual
//    # System.Linq.Expression.ExpressionType.Invoke
//    # System.Linq.Expression.ExpressionType.Lambda
//    # System.Linq.Expression.ExpressionType.LeftShift
//    # System.Linq.Expression.ExpressionType.LessThan
//    # System.Linq.Expression.ExpressionType.LessThanOrEqual
//    # System.Linq.Expression.ExpressionType.ListInit
//    # System.Linq.Expression.ExpressionType.MemberAccess
//    # System.Linq.Expression.ExpressionType.MemberInit
//    # System.Linq.Expression.ExpressionType.Modulo
//    # System.Linq.Expression.ExpressionType.Multiply
//    # System.Linq.Expression.ExpressionType.MultiplyChecked
//    # System.Linq.Expression.ExpressionType.Negate
//    # System.Linq.Expression.ExpressionType.UnaryPlus
//    # System.Linq.Expression.ExpressionType.NegateChecked
//    # System.Linq.Expression.ExpressionType.New
//    # System.Linq.Expression.ExpressionType.NewArrayInit
//    # System.Linq.Expression.ExpressionType.NewArrayBounds
//    # System.Linq.Expression.ExpressionType.Not
//    # System.Linq.Expression.ExpressionType.NotEqual
//    # System.Linq.Expression.ExpressionType.Parameter
//    # System.Linq.Expression.ExpressionType.Power
//    # System.Linq.Expression.ExpressionType.Quote
//    # System.Linq.Expression.ExpressionType.RightShift
//    # System.Linq.Expression.ExpressionType.TypeAs
//    # System.Linq.Expression.ExpressionType.TypeIs
//    # System.Linq.Expression.ExpressionType.Assign
//    # System.Linq.Expression.ExpressionType.Block
//    # System.Linq.Expression.ExpressionType.DebugInfo
//    # System.Linq.Expression.ExpressionType.Decrement
//    # System.Linq.Expression.ExpressionType.Dynamic
//    # System.Linq.Expression.ExpressionType.Default
//    # System.Linq.Expression.ExpressionType.Extension
//    # System.Linq.Expression.ExpressionType.Increment
//    # System.Linq.Expression.ExpressionType.Index
//    # System.Linq.Expression.ExpressionType.Label
//    # System.Linq.Expression.ExpressionType.RuntimeVariables
//    # System.Linq.Expression.ExpressionType.Loop
//    # System.Linq.Expression.ExpressionType.Switch
//    # System.Linq.Expression.ExpressionType.Throw
//    # System.Linq.Expression.ExpressionType.Try
//    # System.Linq.Expression.ExpressionType.Unbox
//    # System.Linq.Expression.ExpressionType.AddAssign
//    # System.Linq.Expression.ExpressionType.*Assign
//    # System.Linq.Expression.ExpressionType.*AssignChecked
//    # System.Linq.Expression.ExpressionType.PreIncrementAssign
//    # System.Linq.Expression.ExpressionType.PreDecrementAssign
//    # System.Linq.Expression.ExpressionType.PostIncrementAssign
//    # System.Linq.Expression.ExpressionType.PostDecrementAssign
//    # System.Linq.Expression.ExpressionType.TypeEqual
//    # System.Linq.Expression.ExpressionType.OnesComplement
//    # System.Linq.Expression.ExpressionType.IsTrue
//    # System.Linq.Expression.ExpressionType.IsFalse


// SS 6.7.0.0.1 declaration
declaration
	: topFnDefinition
	| topVarDeclaration
	| UsingNamespace expression Semi
	;

// SS 6.7.2.0.1 type-specifier
typeName
	: Ident
	;

containerDeclaration
	: ( Extern | Packed )? containerDeclarationAuto
	;

containerDeclarationAuto
	: containerDeclarationType
	  LBrace DocComment?
	  containerMembers RBrace
	;

containerDeclarationType
	: structOrUnionSpecifier
	| enumSpecifier
	| Opaque
	;

// SS 6.7.2.1.1 struct-or-union-specifier
structOrUnionSpecifier
	: Struct (LPar expression RPar)?
	| Union (LPar (Enum (LPar expression RPar)? | expression) RPar)?
	;

// SS 6.7.2.1.7 member-declarator-list
fieldList
	: (field Comma)* field?
	;

// SS 6.7.2.1.8 member-declarator
field
	: DocComment? CompTime? fieldName
	  (Colon typeExpression)?
	  fieldDeclarationSpecifiers
	  (Equal expression)?
 	;
//	| DocComment? CompTime? (Ident Colon)?
//	  // not func?
//	  typeExpression
//        fieldDeclarationSpecifiers
//	  (Equal expression)?

fieldDeclarationSpecifiers
	: byteAlign?
	;
fieldName
	: Ident
	;

// SS 6.7.2.2.1 enum-specifier
enumSpecifier
	: Enum (LPar expression RPar)?
	;

// SS 6.7.6.0.4 function-declarator
fnProtoDeclaration
	: Fn Ident? LPar parameterDeclarationList RPar
	  fnProtoDeclarationSpecifiers
	  typeExpression
	;

fnProtoDeclarationSpecifiers
	: byteAlign?		// alignment-specifier
	  addrSpace?		// attribute-specifier
	  linkSection?		// attribute-specifier
	  callConv?		// attribute-specifier
	;

// SS 6.7.6.0.7 parameter-type-list
// SS 6.7.6.0.8 parameter-list
parameterDeclarationList
	: (parameterDeclaration Comma)* parameterDeclaration?
	;

// SS 6.7.6.0.9 parameter-declaration
parameterDeclaration
	: DocComment?
	  parameterDeclarationSpecifier?
	  (Ident Colon)? parameterType
	| Ellipsis
	;

parameterDeclarationSpecifier
	: NoAlias		// attribute-specifier
	| CompTime		// storage-class-specifier
	;

parameterType
	: AnyType
	| typeExpression
	;

typeExpression
	: prefixTypeOp* errorUnionExpression
	;

errorUnionExpression
	: suffixExpression (Bang typeExpression)?
	;

// SS 6.7.10.0.1 braced-initializer
// bracedInitializer
initList
	: LBrace fieldInit (Comma fieldInit)* Comma? RBrace
	| LBrace expression (Comma expression)* Comma? RBrace
	| LBrace RBrace
	;


// SS 6.8.0.0.1 statement
statement
	: expressionStatement
	| primaryBlockStatement
	;

////////////////////////////////////////////////////////////
// Primary Block Statements
////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////
// Primary Block Statements
////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////
// Primary Block Statements
////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////
// Primary Block Statements
////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////
// Primary Block Statements
////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////
// Primary Block Statements
////////////////////////////////////////////////////////////

// SS 6.8.0.0.3 primary-block
primaryBlockStatement
	: compoundStatement
	| selectionStatement
	| iterationStatement
	;

// SS 6.8.0.0.3 primary-block (Non-standard)
primaryBlockExpression
	: compoundExpression
	| selectionExpression
	| iterationExpression
	;

// SS 6.8.0.0.3 primary-block (Non-standard)
primaryTypeStatement
	: compoundTypeExpression
	| selectionTypeExpression
	| iterationTypeExpression
	;

primaryTypeDeclaration
	: containerDeclaration
	| errorSetDeclaration
	| fnProtoDeclaration
	;

errorSetDeclaration
	: Error LBrace identList RBrace
	;

identList
	: (DocComment Ident Comma)*
           DocComment Ident
	;

// SS 6.8.2.0.1 compound-statement
compoundStatement
	: CompTime
	  blockExpressionStatement
	| NoSuspend
	  blockExpressionStatement
	| Suspend
	  blockExpressionStatement
	| Defer
	  blockExpressionStatement
	| ErrDefer payload?
	  blockExpressionStatement
	;

compoundExpression
	: Break breakLabel? expression?
	| CompTime expression
	| NoSuspend expression
	| Continue breakLabel?
	| Resume expression
	| Return expression?
	| block
	;

compoundTypeExpression
	: builtinCallExpression
	| Dot Ident		// anonymousFieldReference
	| Dot initList		// anonymousCompoundLiteral 
	| Error Dot Ident
	| CompTime typeExpression
	;

builtinCallExpression
	: BuiltinIdent fnCallArguments
	;

// SS 6.8.3.0.1 expression-statement
expressionStatement
	: CompTime? varDeclaration
	| assignExpression Semi
	;

// SS 6.8.4.0.1 selection-statement
selectionStatement
	: ifStatement
	| switchExpression
	;

// SS 6.8.4.0.1 selection-expression (Non-standard)
selectionExpression
	: ifExpression
	| switchExpression
	;

// SS 6.8.4.0.1 selection-type-expression (Non-standard)
selectionTypeExpression
	: ifTypeExpression
	| switchExpression
	;

ifStatement
	: ifPrefix blockExpression (Else payload? elseStatement)?
	| ifPrefix assignExpression (Semi | Else payload? elseStatement)
	;

ifExpression
	: ifPrefix thenExpression (Else payload? elseExpression)?
	;

ifTypeExpression
	: ifPrefix typeExpression (Else payload? typeExpression)?
	;

ifPrefix
	: If LPar condExpression RPar ptrPayload?
	;

condExpression
	: expression ;
thenExpression
	: expression ;
elseExpression
	: expression ;
elseStatement
	: statement ;

switchExpression
	: Switch LPar expression RPar LBrace switchProngList RBrace
	;

// SS 6.8.5.0.1 iteration-statement
iterationStatement
	: labeledStatement
	;

// SS 6.8.5.0.1 iteration-expression (Non-standard)
iterationExpression
	: labeledExpression
	;

// SS 6.8.5.0.1 iteration-type-expression (Non-standard)
iterationTypeExpression
	: labeledTypeExpression
	;

labeledStatement
	: blockLabel? (block | loopStatement)
	;

labeledExpression
	: blockLabel? loopExpression
	;

labeledTypeExpression
	: blockLabel block
	| blockLabel? loopTypeExpression
	;

loopStatement
	: Inline (forStatement | whileStatement)
	;

loopExpression
	: Inline? (forExpression | whileExpression)
	;

loopTypeExpression
	: Inline (forTypeExpression | whileTypeExpression)
	;

forStatement
	: forPrefix blockExpression (Else statement)?
	| forPrefix assignExpression (Semi | Else statement)
	;

forExpression
	: forPrefix expression (Else expression)?
	;

forTypeExpression
	: forPrefix typeExpression (Else typeExpression)?
	;

forPrefix
	: For LPar forArgumentsList RPar ptrListPayload
	;

whileStatement
	: whilePrefix blockExpression (Else statement)?
	| whilePrefix assignExpression (Semi | Else statement)
	;

whileExpression
	: whilePrefix expression (Else payload? expression)?
	;

whileTypeExpression
	: whilePrefix typeExpression (Else payload? typeExpression)?
	;

whilePrefix
	: While LPar condExpression RPar ptrPayload? whileContinueExpression?
	;

blockExpressionStatement
	: blockExpression
	| assignExpression Semi
	;

blockExpression
	: blockLabel? block
	;

assignExpression
	: expression (assignOpExpression expression)?
	;

breakLabel
	: Colon Ident
	;

blockLabel
	: Ident Colon
	;

block
	: LBrace statement* RBrace
	;

integerLiteral
	: Integer
	;

floatingLiteral
	: Float
	;

charLiteral
	: Char
	;

singleStringLiteral
	: SingleString
	;

lineStringLiteral
	: LineString
	;

groupedExpression
	// LPar typeExpression RPar
	: LPar expression RPar
	;

fieldInit
	: Dot Ident Equal expression
	;

whileContinueExpression
	: Colon LPar assignExpression RPar
	;

linkSection
	: LinkSection LPar expression RPar
	;

addrSpace
	: AddrSpace LPar expression RPar
	;

callConv
	: CallConv LPar expression RPar
	;


payload
	: Pipe Ident Pipe
	;

ptrPayload
	: Pipe Star? Ident Pipe
	;

ptrIndexPayload
	: Pipe Star? Ident (Comma Ident)? Pipe
	;

ptrListPayload
	: Pipe Star? Ident (Comma Star? Ident)* Comma? Pipe
	;

switchProng
	: Inline? switchCase EqualArrow ptrIndexPayload? assignExpression
	;

switchCase
	: switchItem (Comma switchItem)* Comma?
	| Else
	;

switchItem
	: expression (Ellipsis expression)?
	;

forArgumentsList
	: forItem (Comma forItem)* Comma?
	;

forItem
	: expression //(Dot2 expression?)?
	;

// Operators
assignOpExpression
	: Equal
	| AssignOp
	;

compareOpExpression
	: Equal2
	| CompareOp
	;

bitwiseOpExpression
	: BitwiseOp
	| bitwiseKwExpression
	;

bitwiseKwExpression
	: OrElse
	| Catch payload?
	;

prefixTypeOp
	: Quest
	| AnyFrame MinusArrow
	| sliceTypeStart
	  sliceTypeRest*
	| ptrTypeStart
	  ptrTypeRest*
	| arrayTypeStart
	;

arrayTypeStart
	: LBrack expression (Colon expression)? RBrack
	;

sliceTypeStart
	: LBrack (Colon expression)? RBrack
	;

sliceTypeRest
	: byteAlign	// alignment-specifier
	| addrSpace	// attribute-specifier
	| AllowZero	// attribute-specifier
	| Const		// type-qualifier
	| Volatile	// type-qualifier
	;

ptrTypeStart
	: Star
	| Star Star
	| LBrack Star (LetterC | Colon expression)? RBrack
	;

ptrTypeRest
	: byteAlign3	// alignment-specifier
	| addrSpace	// attribute-specifier
	| AllowZero	// attribute-specifier
	| Const		// type-qualifier
	| Volatile	// type-qualifier
	;

suffixOp
	: LBrack expression (Dot2 (expression (Colon expression)?)?)? RBrack
	| Dot Ident
	| DotStar
	| DotQue
	;

// SS 6.7.5.0.1 alignment-specifier
byteAlign
	: Align LPar expression RPar
	;
byteAlign3
	: Align LPar expression (Colon expression Colon expression)? RPar
	;

switchProngList
	: (switchProng Comma)* switchProng?
	;

stringList
	: (SingleString Comma)* SingleString?
	;

// Non-standard
containerUnit
	: ContainerDocComment* containerMembers
	;

// SS 6.9.0.0.1 translation-unit
containerMembers
	: fieldList
	  containerDeclarationList*
	;

// SS 6.9.0.0.2 external-declaration
containerDeclarationList
	: testDeclaration
	| compTimeDeclaration
	| DocComment? Pub? declaration
	;

// SS 6.9.1.0.1 function-definition
topFnDefinition
	: fnProtoDeclarationEx? fnProtoDeclaration (Semi | block)
	;
topVarDeclaration
	: varDeclarationEx? ThreadLocal? varDeclaration
	;

fnProtoDeclarationEx
	: Export
	| Extern SingleString?
	| Inline
	| NoInline
	;

varDeclarationEx
	: Export
	| Extern SingleString?
	;

varName	: Ident ;
varDeclaration
	: (Const | Var) varName (Colon typeExpression)?
	  varDeclarationSpecifiers
	  (Equal expression)? Semi
	;

varDeclarationSpecifiers
	: byteAlign?		// alignment-specifier
	  addrSpace?		// attribute-specifier
	  linkSection?		// attribute-specifier
	;

testDeclaration
	: Test (SingleString | Ident)? block
	;

compTimeDeclaration
	: CompTime block
	;
