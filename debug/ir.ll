; ModuleID = "mukhya"
target triple = "x86_64-pc-windows-msvc"
target datalayout = ""

@"true" = constant i1 1
@"false" = constant i1 0
define i32 @"mukhya"()
{
mukhya_entry:
  %".2" = alloca i32
  store i32 4, i32* %".2"
  %".4" = load i32, i32* %".2"
  %".5" = icmp slt i32 %".4", 5
  br i1 %".5", label %"mukhya_entry.if", label %"mukhya_entry.else"
mukhya_entry.if:
  %".7" = load i32, i32* %".2"
  ret i32 %".7"
mukhya_entry.else:
  %".9" = load i32, i32* %".2"
  %".10" = mul i32 %".9", 5
  ret i32 %".10"
mukhya_entry.endif:
  ret i32 0
}
