The output language is what I call "ZigS" or "ZigEssExpression"

```
member
    | (zig:field fieldAttrs ident type value)
    | (zig:test expr block)
    | (zig:comptime block)
    | decl

decl
    | `(zig:fn fnProtoAttrs ident paramDeclList typeExpr block?)
    | `(zig:usingnamespace expr)
    | varDecl

varDecl
    | `(zig:const ident type? varAttrs? value)
    | `(zig:var   ident type? varAttrs? value)
```

# Example Field:
```
(zig:field {} pi f32 3.14)
```

# Example Field Attributes:
```
(zig:field {bytealign: expr
            comptime: #t} pi f32 ...)
```

```
```

# Example Function Prototype:
```
(zig:fn {} greet [] void
  (std.debug.print "Hello, World!" (zig:dot {}))))
```

# Example Constant Declaration:
```
(zig:const {} std None (@import "std"))
```

# Example Function Prototype Attributes:
```
(zig:fn {addrspace: expr
         bytealign: expr
         linksection: expr
         callconv: expr
         export: #t
         extern: expr
         inline: #t
         noinline: #t} greet [] void ...)
```

# Example Constant Declaration Attributes:
```
(zig:const {addrspace: expr
            bytealign: expr
            linksection: expr
            export: #t
            extern: #t} pi f64 ...)
```

```
stmt
    | varDecl
    | ( (zig:comptime varDecl)
      | (zig:comptime blockExprStmt)
      | (zig:nosuspend blockExprStmt)
      | (zig:suspend blockExprStmt)
      | (zig:defer blockExprStmt)
      | (zig:errdefer blockExprStmt)
      | (zig:if-stmt blockExprStmt)
      | (zig:label-stmt blockExprStmt)
      | (zig:switch-stmt blockExprStmt)
      | (zig:for-stmt confExpr thenStmt elseStmt)
      | (zig:while-stmt confExpr thenStmt elseStmt)
      | (zig:block-stmt stmt)
      | (zig:= blockExprStmt))
```


```
expr
    | (or expr ...)
    | (and expr ...)
    # compare
    | ( (== expr ...)
      | (!= expr ...)
      | (< expr ...)
      | (> expr ...)
      | (<= expr ...)
      | (>= expr ...))
    # bitwise
    | ( (& expr ...)
      | (^ expr ...)
      | (| expr ...)
      | (zig:orelse expr ...)
      | (zig:catch lambdaPayload expr ...))
    # bitshift
    | ( (<< expr ...)
      | (<<| expr ...)
      | (>> expr ...))
    # addition
    | ( (+ expr ...)
      | (+% expr ...)
      | (+| expr ...)
      | (++ expr ...)
      | (- expr ...)
      | (-% expr ...)
      | (-| expr ...)
      | (-- expr ...))
    | ( (% expr ...)
      | (* expr ...)
      | (*% expr ...)
      | (** expr ...)
      | (*| expr ...)
      | (/ expr ...)
      | (|| expr ...)) # Error-Union Merge
    | ( (! expr) # boolean not
      | (~ expr) # bitwise not
      | (- expr) # arithmetic negative
      | (-% expr)
      | (& expr) # pointer reference
      | (zig:try expr)
      | (zig:await expr))
    | ( (zig:if-expr condExpr thenExpr elseExpr)
      | (zig:asm-expr
      | (zig:break expr)
      | (zig:comptime expr)
      | (zig:nosuspend expr)
      | (zig:continue expr)
      | (zig:resume expr)
      | (zig:return expr)
      | (zig:label-expr blockLabel expr)
      | (zig:block-expr stmt*)
      | (zig:for-expr condExpr thenExpr elseExpr)
      | (zig:while-expr condExpr thenExpr elseExpr)
      | (zig:make-object typeExpr initList)))
    | ( (? typeExpr)
      | (zig:anyframe -> typeExpr)
      | (! suffixExpr typeExpr)
      | (builtinIdent expr ...)
      | 'char'
      | (zig:struct expr members)
      | (zig:opaque)
      | (zig:enum expr members)
      | (zig:union expr members)
      | (zig:dot ident)
      | (zig:dot identList)
      | 3.14
      | 3
      | fnProto
      | (zig:label-type-expr expr ...)
      | typeName
      | (zig:if-type-expr
      | (zig:error-dot ident)
      | (zig:anyframe)
      | (zig:unreachable)
      | "..."
      | (zig:switch-expr expr prong ...)
    )
```

```zig
const std = @import("zig");
```

```lisp
(zig:const std (@import "zig"))
```

It is interesting that many of the forms that would be expressions in C have 3 forms in Zig:

```
      | (zig:if-stmt condExpr thenStmt elseStmt)
      | (zig:if-expr condExpr thenExpr elseExpr)
      | (zig:if-type-expr condExpr thenTypeExpr elseTypeExpr)
```
