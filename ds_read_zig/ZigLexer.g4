lexer grammar ZigLexer;

// Keywords
AddrSpace : 'addrspace' ;
Align	: 'align' ;
AllowZero : 'allowzero' ;
And	: 'and' ;
AnyFrame : 'anyframe' ;
AnyType : 'anytype' ;
Asm	: 'asm' ;
Async	: 'async' ;
Await   : 'await' ;
Break	: 'break' ;
CallConv : 'callconv' ;
Catch   : 'catch' ;
CompTime: 'comptime' ;
Const	: 'const' ;
Continue: 'continue' ;
Defer	: 'defer' ;
Else	: 'else' ;
Enum	: 'enum' ;
ErrDefer: 'errdefer' ;
Error	: 'error' ;
Export	: 'export' ;
Extern	: 'extern' ;
Fn      : 'fn' ;
For	: 'for' ;
If	: 'if' ;
Inline  : 'inline' ;
LetterC : 'c' ;
LinkSection : 'linksection' ;
NoAlias	: 'noalias' ;
NoInline: 'noinline' ;
NoReturn: 'noreturn' ;
NoSuspend: 'nosuspend' ;
Opaque	: 'opaque' ;
Or	: 'or' ;
OrElse	: 'orelse' ;
Packed	: 'packed' ;
Pub	: 'pub' ;
Resume  : 'resume' ;
Return  : 'return' ;
Struct	: 'struct' ;
Suspend	: 'suspend' ;
Switch  : 'switch' ;
Test	: 'test' ;
ThreadLocal: 'threadlocal' ;
Try     : 'try' ;
Union	: 'union' ;
Unreachable : 'unreachable' ;
UsingNamespace: 'usingnamespace' ;
Var	: 'var' ;
Volatile: 'volatile' ;
While   : 'while' ; // { ZigKeywordSymbol.while } ;


// Other Tokens
LPar		: '(' ;
RPar		: ')' ;
LBrace		: '{' ;
RBrace		: '}' ;
LBrack		: '[' ;
RBrack		: ']' ;
Amp		: '&' ;
At		: '@' ;
Bang		: '!' ;
Caret   	: '^' ;
Colon		: ':' ;
Comma		: ',' ;
Dot		: '.' ;
Dot2		: '..' ;
DotQue  	: '.?' ;
DotStar 	: '.*' ;
Ellipsis	: '...' ;
Equal		: '=' ;
Equal2		: '==' ;
EqualArrow 	: '=>' ;
Esc		: '\\' ;
Minus2   	: '--' ;
Minus   	: '-' ;
MinusArrow 	: '->' ;
MinusPct	: '-%' ;
MinusPipe	: '-|' ;
Pct	    	: '%' ;
Pipe2    	: '||' ;
Pipe    	: '|' ;
Plus2		: '++' ;
Plus		: '+' ;
PlusPct		: '+%' ;
PlusPipe	: '+|' ;
Quest   	: '?' ;
Semi		: ';' ;
Sol		: '/' ;
Star2    	: '**' ;
StarPct    	: '*%' ;
StarPipe    	: '*|' ;
Star    	: '*' ;
Tilde   	: '~' ;

fragment Apos 
	: '\u0027' ;
fragment Quot
	: '"' ;
fragment Sol2Bang
	: '//!' ;
fragment Sol4
	: '////' ;
fragment Sol3
	: '///' ;
fragment Sol2
	: '//' ;

AssignOp
	: '*='
	| '*|='
	| '/='
	| '%='
	| '+='
	| '+|='
	| '-='
	| '-|='
	| '<<='
	| '<<|='
	| '>>='
	| '&='
	| '^='
	| '|='
	| '*%='
	| '+%='
	| '-%='
	;

CompareOp
	: '!='
	| '<'
	| '>'
	| '<='
	| '>='
	;

BitwiseOp
	: Amp
	| Caret
	| Pipe
	;
	
BitShiftOp
	: '<<'
	| '>>'
	| '<<|'
	;

// Identifiers
BuiltinIdent : At Ident ;

// ArgumentReferenceExpression
// BaseReferenceExpression
// EventReferenceExpression
// FieldReferenceExpression
// MethodReferenceExpression
// PropertyReferenceExpression
// PropertySetValueReferenceExpression
// ThisReferenceExpression
// TypeReferenceExpression
// VariableReferenceExpression
Ident
	: SingleIdent
	| StringIdent
	;


fragment SingleIdent
	: [a-zA-Z_] [0-9a-zA-Z_]* ;
fragment StringIdent
	: At SingleString ;

Integer	: Digit+ ;
Float	: Integer Dot Integer ;

Char	: Apos CharChar* Apos Hws?
	;

SingleString
	: Quot StringChar* Quot Hws?
	;
	
// String
// 	: StringSingle
// 	| (LineString Hws?)+
// 	;

LineString
	: ((Esc Esc StringChar* Vws)+ Hws?)+
	;

fragment Bit
	: [01] ;
fragment Digit
	: [0-9] ;
fragment HexDigit
	: [0-9a-fA-F] ;


fragment CharEsc
	: Esc 'x' HexDigit HexDigit
	| Esc 'u{' HexDigit+ '}'
	| Esc [nr\\t'"]
	;

fragment UniCharNNSS
	: ~[\n\\'] ;

fragment UniCharNNDD
	: ~[\n\\"] ;
	
fragment CharChar
	: UniCharNNSS
	| CharEsc
	;

fragment StringChar
	: UniCharNNDD
	| Apos
	| Esc Esc
	| CharEsc
	;

fragment CommentChar
	: [\u0001-\u0009\u000b-\uffff] ;
	//: ~[\n] ;

ContainerDocComment 
	: Sol2Bang Hws? CommentChar* Vws 
	;

// It is extremely important that these rules
// are in this order, because otherwise, the
// DocComment rule will not be recognized.

fragment Line4Comment 
	: Sol4 Hws? CommentChar* Vws
	;

DocComment 
	: Sol3 Hws? CommentChar* Vws 
	;

fragment Line2Comment 
	: Sol2 Hws? CommentChar* Vws
	;

fragment Vws	: [\r\n]+ ;
fragment Hws	: [ \t]+ ;

Ws	: ( ContainerDocComment 
	  | Line4Comment 
	  | DocComment 
	  | Line2Comment 
	  | Hws 
	  | Vws)+ -> skip ;
