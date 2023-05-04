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

AdditionOp
	: Plus
	| Minus
	| MinusPct
	| '++'
	| '+%'
	| '+|'
	| '-|'
	;

MultiplyOp
	: '||'
	| Star
	| Slash
	| '%'
	| '**'
	| '*%'
	| '*|'
	;

PrefixOp
	: Bang
	| Minus
	| Tilde
	| MinusPct
	| Amp
	| Try
	| Await
	;

// Identifiers
BuiltinIdent : At Ident ;

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
	: DQuote StringChar* DQuote Hws?
	;
	
// String
// 	: StringSingle
// 	| (LineString Hws?)+
// 	;

LineString
	: ((BackSlash2 CommentChar* Vws)+ Hws?)+
	;

// Other Tokens
LParen	: '(' ;
RParen	: ')' ;
LBrace	: '{' ;
RBrace	: '}' ;
LBrack	: '[' ;
RBrack	: ']' ;
Amp	: '&' ;
At	: '@' ;
BackSlash2: '\\\\' ;
Bang	: '!' ;
Caret   : '^' ;
Colon	: ':' ;
Comma	: ',' ;
Dot	: '.' ;
Dot2	: '..' ;
Ellipsis: '...' ;
Equal	: '=' ;
Equal2	: '==' ;
EqualArrow : '=>' ;
Esc	: '\\' ;
Minus   : '-' ;
MinusArrow : '->' ;
MinusPct: '-%' ;
Pipe    : '|' ;
Plus	: '+' ;
Semi	: ';' ;
Slash	: '/' ;
Star    : '*' ;
Tilde   : '~' ;
Question: '?' ;
DotStar : '.*' ;
DotQue  : '.?' ;

fragment Bit
	: [01] ;
fragment Digit
	: [0-9] ;
fragment HexDigit
	: [0-9a-fA-F] ;

fragment Slash2
	: '//' ;
fragment Slash3
	: '///' ;
fragment Slash4
	: '////' ;

fragment Slash2Bang
	: '//!' ;
fragment DQuote
	: '"' ;
fragment Apos 
	: '\u0027' ;

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
	: ~[\n] ;

ContainerDocComment 
	: Slash2Bang Hws CommentChar* Vws 
	;

DocComment 
	: Slash3 Hws CommentChar* Minus? Vws 
	;

LineComment 
	: Slash2 Hws CommentChar* Vws
	| Slash4 Hws CommentChar* Vws
	;

fragment Vws	: [\n]+ ;
fragment Hws	: [ \t]+ ;
Ws	: (ContainerDocComment | LineComment | Hws | Vws) -> skip ;
// End : EOF -> skip ;