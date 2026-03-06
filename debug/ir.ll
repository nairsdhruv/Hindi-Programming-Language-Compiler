; ModuleID = "mukhya"
target triple = "x86_64-pc-windows-msvc"
target datalayout = ""

define i32 @"mukhya"()
{
mukhya_entry:
  %".2" = alloca i32
  store i32 4, i32* %".2"
  %".4" = load i32, i32* %".2"
  ret i32 %".4"
}
