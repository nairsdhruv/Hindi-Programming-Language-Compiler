; ModuleID = "mukhya"
target triple = "x86_64-pc-windows-msvc"
target datalayout = ""

declare i32 @"printf"(i8* %".1", ...)

@"true" = constant i1 1
@"false" = constant i1 0
define i32 @"mukhya"()
{
mukhya_entry:
  %".2" = alloca i32
  store i32 1, i32* %".2"
  %".4" = load i32, i32* %".2"
  %".5" = icmp sle i32 %".4", 10
  br i1 %".5", label %"while_loop_entry_1", label %"while_loop_otherwise_1"
while_loop_entry_1:
  %".7" = getelementptr inbounds [4 x i8], [4 x i8]* @"__str_2", i32 0, i32 0
  %".8" = load i32, i32* %".2"
  %".9" = call i32 (i8*, ...) @"printf"(i8* %".7", i32 %".8")
  %".10" = load i32, i32* %".2"
  %".11" = add i32 %".10", 1
  store i32 %".11", i32* %".2"
  %".13" = load i32, i32* %".2"
  %".14" = icmp sle i32 %".13", 10
  br i1 %".14", label %"while_loop_entry_1", label %"while_loop_otherwise_1"
while_loop_otherwise_1:
  ret i32 0
}

@"__str_2" = internal constant [4 x i8] c"%d\0a\00"