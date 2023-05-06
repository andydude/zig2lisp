// '(zig:members
//    (zig:const std (@import "std"))
//    (zig:fn main #() void
//      ((zig:dot std debug print)
//       "Hello, World!\n" (zig:dot #()))))
const std = @import("std");

pub fn main() void {
    std.debug.print("Hello, World!\n", .{});
}


