# zig2lisp
Convert Zig programming language to a Lisp representation of Zig


## Example Hello World

The following file can be found in `t/hello_world.zig`
```zig
const std = @import("std");
pub fn main() void {
    std.debug.print("Hello, World!\n", .{});
}
```

To convert it to a Lisp representation, just run the following

```sh
$ zig2lisp t/hello_world.zig
```

```lisp
(zig:members
  (zig:const {} std None (@import "std"))
  (zig:fn main None void
    ((zig:dot std debug print)
      "Hello, World!\n"
      (zig:curlysuffix))))
```