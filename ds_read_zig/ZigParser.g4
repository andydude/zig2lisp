parser grammar ZigParser;
options { tokenVocab = ZigLexer; }

start
	: ContainerDocComment* members
	;

members
	: fieldList?
	  declaration*
	;

declaration
	: testDecl
	| comptimeDecl
	| (DocComment? Pub)? decl
	// | decl
	;

testDecl
	: Test (SingleString | Ident)? block
	;

comptimeDecl
	: CompTime block
	;

decl
	: fnProtoDeclEx? fnProto (Semi | block)
	| varDeclEx? ThreadLocal? varDecl
	| UsingNamespace expr Semi
	;

fnProtoDeclEx
	: Export
	| Extern SingleString?
	| Inline
	| NoInline
	;
	
varDeclEx
	: Export
	| Extern SingleString?
	;  

decl2
	: ( Extern | Packed )? declAuto
	;


fnProto
	: Fn Ident? LParen paramDeclList RParen
	  byteAlign? addrSpace? linkSection?
	  callConv? (AnyError Bang)? typeExpr
	;

varName	: Ident ;
varDecl
	: (Const | Var) varName (Colon typeExpr)?
	  byteAlign? addrSpace? linkSection?
	  (Equal expr)? Semi
	;

fieldName : Ident ;
field
	: DocComment? CompTime? fieldName (Colon typeExpr)?
	  byteAlign?
	  (Equal expr)?
 	;
//	| DocComment? CompTime? (Ident Colon)?
//	// not func?
//	  typeExpr byteAlign?
//	  (Equal expr)?
	
stmt
	: CompTime? varDecl
	| CompTime blockExprStmt
	| NoSuspend blockExprStmt
	| Suspend blockExprStmt
	| Defer blockExprStmt
	| ErrDefer payload? blockExprStmt
	| ifStmt
	| labeledStmt
	| switchExpr
	| assignExpr Semi
	;

elseStmt : stmt ;
ifStmt
	: ifPrefix blockExpr (Else payload? elseStmt)?
	| ifPrefix assignExpr (Semi | Else payload? elseStmt)
	;

labeledStmt
	: blockLabel? (block | loopStmt)
	;

loopStmt
	: Inline (forStmt | whileStmt)
	;

forStmt
	: forPrefix blockExpr (Else stmt)?
	| forPrefix assignExpr (Semi | Else stmt)
	;

whileStmt
	: whilePrefix blockExpr (Else stmt)?
	| whilePrefix assignExpr (Semi | Else stmt)
	;

blockExprStmt
	: blockExpr
	| assignExpr Semi
	;

blockExpr
	: blockLabel? block
	;

assignExpr
	: expr (assignOpExpr expr)?
	;

expr
	: boolOrExpr
	;

boolOrExpr
	: boolAndExpr (Or boolAndExpr)*
	;

boolAndExpr
	: compareExpr (And compareExpr)*
	;

compareExpr
	: bitwiseExpr (compareOpExpr bitwiseExpr)*
	;

bitwiseExpr
	: bitShiftExpr (bitwiseOpExpr bitShiftExpr)*
	;

bitShiftExpr
	: additionExpr (BitShiftOp additionExpr)*
	;

additionExpr
	: multiplyExpr (AdditionOp multiplyExpr)*
	;

multiplyExpr
	: prefixExpr (MultiplyOp prefixExpr)*
	;

prefixExpr
	: PrefixOp* primaryExpr
	;

breakLabel
	: Colon Ident
	;

blockLabel
	: Ident Colon
	;

primaryExpr
	: ifExpr
	// | asmExpr
	| Break breakLabel? expr?
	| CompTime expr
	| NoSuspend expr
	| Continue breakLabel?
	| Resume expr
	| Return expr?
	| blockLabel? loopExpr
	| block
	| curlySuffixExpr
	;

thenExpr : expr ;
elseExpr : expr ;
ifExpr
	: ifPrefix thenExpr (Else payload? elseExpr)?
	;

block
	: LBrace stmt* RBrace
	;

loopExpr
	: Inline? (forExpr | whileExpr)
	;

forExpr
	: forPrefix expr (Else expr)?
	;

whileExpr
	: whilePrefix expr (Else payload? expr)?
	;

curlySuffixExpr
	: typeExpr initList?
	;

initList
	: LBrace fieldInit (Comma fieldInit)* Comma? RBrace
	| LBrace expr (Comma expr)* Comma? RBrace
	| LBrace RBrace
	;

typeExpr
	: prefixTypeOp* errorUnionExpr
	;

errorUnionExpr
	: suffixExpr (Bang typeExpr)?
	;

suffixExpr
	: Async primaryTypeExpr suffixOp* fnCallArguments
	| primaryTypeExpr designatorExpr*
	;

designatorExpr
	: suffixOp
	| fnCallArguments
	;

typeName : Ident ;
compTimeTypeExpr : CompTime typeExpr ;
primaryTypeExpr
	: primaryBiCall
	| charLiteral
	| decl
	| Dot Ident
	// | Dot identList
	| errorSetDecl
	| floatingLiteral
	| fnProto
	| groupedExpr
	| labeledTypeExpr
	| typeName
	| ifTypeExpr
	| integerLiteral
	| compTimeTypeExpr
	| Error Dot Ident
	| AnyFrame
	| Unreachable
	| singleStringLiteral
	| lineStringLiteral
	| switchExpr
	;

primaryBiCall
	: BuiltinIdent fnCallArguments
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
	
errorSetDecl
	: Error LBrace identList RBrace
	;

groupedExpr
	: LParen expr RParen
	;

ifTypeExpr
	: ifPrefix typeExpr (Else payload? typeExpr)?
	;

labeledTypeExpr
	: blockLabel block
	| blockLabel? loopTypeExpr
	;

loopTypeExpr
	: Inline (forTypeExpr | whileTypeExpr)
	;

forTypeExpr
	: forPrefix typeExpr (Else typeExpr)?
	;

whileTypeExpr
	: whilePrefix typeExpr (Else payload? typeExpr)?
	;

switchExpr
	: Switch LParen expr RParen LBrace switchProngList RBrace
	;

// asmExpr : ;
// asmOutput : ;
// asmOutputItem : ;
// asmInput : ;
// asmInputItem : ;
// asmClobbers : ;

fieldInit
	: Dot Ident Equal expr
	;

whileContinueExpr
	: Colon LParen assignExpr RParen
	;

linkSection
	: LinkSection LParen expr RParen
	;

addrSpace
	: AddrSpace LParen expr RParen
	;

callConv
	: CallConv LParen expr RParen
	;

paramDecl
	: DocComment?
	  ( NoAlias
	  | CompTime
	  )?
	  (Ident Colon)? paramType
	| Ellipsis
	;

paramType
	: AnyType
	| typeExpr
	;

condExpr : expr ;
ifPrefix
	: If LParen condExpr RParen ptrPayload?
	;

whilePrefix
	: While LParen condExpr RParen ptrPayload? whileContinueExpr?
	;

forPrefix
	: For LParen forArgumentsList RParen ptrListPayload
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
	: Inline? switchCase EqualArrow ptrIndexPayload? assignExpr
	;

switchCase
	: switchItem (Comma switchItem)* Comma?
	| Else
	;

switchItem
	: expr (Ellipsis expr)?
	;

forArgumentsList
	: forItem (Comma forItem)* Comma?
	;

forItem
	: expr (Dot2 expr?)?
	;

// Operators
assignOpExpr
	: Equal
	| AssignOp
	;
	
compareOpExpr
	: Equal2
	| CompareOp
	;
	
bitwiseOpExpr
	: BitwiseOp
	| bitwiseKwExpr
	;
	
bitwiseKwExpr
	: OrElse
	| Catch payload?
	;
	
prefixTypeOp
	: Question
	| AnyFrame MinusArrow
	| sliceTypeStart
	  sliceTypeRest*
	| ptrTypeStart
	  ptrTypeRest*
	| arrayTypeStart
	;

sliceTypeRest
	: byteAlign
	| addrSpace
	| Const
	| Volatile
	| AllowZero
	;
	
ptrTypeRest
	: addrSpace
	| Align LParen expr (Colon expr Colon expr)? RParen
	| Const
	| Volatile 
	| AllowZero
	;
	
suffixOp
	: LBrack expr (Dot2 (expr (Colon expr)?)?)? RBrack
	| Dot Ident
	| DotStar
	| DotQue
	;

fnCallArguments
	: LParen exprList RParen
	;

sliceTypeStart
	: LBrack (Colon expr)? RBrack
	;

ptrTypeStart
	: Star
	| Star Star
	| LBrack '*' (LetterC | Colon expr)? RBrack
	;

arrayTypeStart
	: LBrack expr (Colon expr)? RBrack
	;

declAuto
	: declType LBrace DocComment? members RBrace
	;

declType
	: Struct (LParen expr RParen)?
	| Opaque
	| Enum (LParen expr RParen)?
	| Union (LParen (Enum (LParen expr RParen)? | expr) RParen)?
	;


byteAlign
	: Align LParen expr RParen
	;

identList
	: (DocComment Ident Comma)*
          (DocComment Ident)?
	;

switchProngList
	: (switchProng Comma)* switchProng?
	;

//asmOutputList
//	: (asmOutputItem Comma)* asmOutputItem?
//	;
//
//asmInputList
//	: (asmInputItem Comma)* asmInputItem?
//	;

stringList
	: (SingleString Comma)* SingleString?
	;

paramDeclList
	: (paramDecl Comma)* paramDecl?
	;

exprList
	// expr? (Comma expr)* Comma
	: (expr Comma)* expr
	;
	
fieldList
	: (field Comma)* field
	;
