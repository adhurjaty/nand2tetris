@256
D=A
@SP
M=D
@return$Sys.init.1
D=A
@SP
A=M
M=D
@SP
M=M+1
@0
D=A
@LCL
A=M+D
D=A
@SP
A=M
M=D
@SP
M=M+1
@0
D=A
@ARG
A=M+D
D=A
@SP
A=M
M=D
@SP
M=M+1
@0
D=A
@THIS
A=M+D
D=A
@SP
A=M
M=D
@SP
M=M+1
@0
D=A
@THAT
A=M+D
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
D=M
@5
D=D-A
@0
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Sys.init
0;JMP
(return$Sys.init.1)
(Main.fibonacci)
@0
D=A
@ARG
A=M+D
D=M
@SP
A=M
M=D
@SP
M=M+1
@2
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
M=M-D
D=A
@R14
M=D
A=M
D=M
@CONDITIONALJUMP.TRUE.0
D;JLT
D=0
@CONDITIONALJUMP.END.0
0;JMP
(CONDITIONALJUMP.TRUE.0)
D=-1
(CONDITIONALJUMP.END.0)
@R14
A=M
M=D
@SP
M=M+1
@SP
M=M-1
A=M
D=M
@FibonacciElement$IF_TRUE
D;JNE
@FibonacciElement$IF_FALSE
0;JMP
(FibonacciElement$IF_TRUE)
@0
D=A
@ARG
A=M+D
D=M
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@R15
M=D
@5
A=D-A
D=M
@R14
M=D
@0
D=A
@ARG
A=M+D
D=A
@R13
M=D
@SP
M=M-1
@SP
A=M
D=M
@R13
A=M
M=D
D=A
@SP
M=D+1
@R15
M=M-1
A=M
D=M
@THAT
M=D
@R15
M=M-1
A=M
D=M
@THIS
M=D
@R15
M=M-1
A=M
D=M
@ARG
M=D
@R15
M=M-1
A=M
D=M
@LCL
M=D
@R14
A=M
0;JMP
(FibonacciElement$IF_FALSE)
@0
D=A
@ARG
A=M+D
D=M
@SP
A=M
M=D
@SP
M=M+1
@2
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
M=M-D
@SP
M=M+1
@return$Main.fibonacci.1
D=A
@SP
A=M
M=D
@SP
M=M+1
@0
D=A
@LCL
A=M+D
D=A
@SP
A=M
M=D
@SP
M=M+1
@0
D=A
@ARG
A=M+D
D=A
@SP
A=M
M=D
@SP
M=M+1
@0
D=A
@THIS
A=M+D
D=A
@SP
A=M
M=D
@SP
M=M+1
@0
D=A
@THAT
A=M+D
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
D=M
@5
D=D-A
@1
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Main.fibonacci
0;JMP
(return$Main.fibonacci.1)
@0
D=A
@ARG
A=M+D
D=M
@SP
A=M
M=D
@SP
M=M+1
@1
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
M=M-D
@SP
M=M+1
@return$Main.fibonacci.2
D=A
@SP
A=M
M=D
@SP
M=M+1
@0
D=A
@LCL
A=M+D
D=A
@SP
A=M
M=D
@SP
M=M+1
@0
D=A
@ARG
A=M+D
D=A
@SP
A=M
M=D
@SP
M=M+1
@0
D=A
@THIS
A=M+D
D=A
@SP
A=M
M=D
@SP
M=M+1
@0
D=A
@THAT
A=M+D
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
D=M
@5
D=D-A
@1
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Main.fibonacci
0;JMP
(return$Main.fibonacci.2)
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
M=M+D
@SP
M=M+1
@LCL
D=M
@R15
M=D
@5
A=D-A
D=M
@R14
M=D
@0
D=A
@ARG
A=M+D
D=A
@R13
M=D
@SP
M=M-1
@SP
A=M
D=M
@R13
A=M
M=D
D=A
@SP
M=D+1
@R15
M=M-1
A=M
D=M
@THAT
M=D
@R15
M=M-1
A=M
D=M
@THIS
M=D
@R15
M=M-1
A=M
D=M
@ARG
M=D
@R15
M=M-1
A=M
D=M
@LCL
M=D
@R14
A=M
0;JMP
(Sys.init)
@4
D=A
@SP
A=M
M=D
@SP
M=M+1
@return$Main.fibonacci.3
D=A
@SP
A=M
M=D
@SP
M=M+1
@0
D=A
@LCL
A=M+D
D=A
@SP
A=M
M=D
@SP
M=M+1
@0
D=A
@ARG
A=M+D
D=A
@SP
A=M
M=D
@SP
M=M+1
@0
D=A
@THIS
A=M+D
D=A
@SP
A=M
M=D
@SP
M=M+1
@0
D=A
@THAT
A=M+D
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
D=M
@5
D=D-A
@1
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Main.fibonacci
0;JMP
(return$Main.fibonacci.3)
(FibonacciElement$WHILE)
@FibonacciElement$WHILE
0;JMP