@17
D=A
@SP
A=M
M=D
@SP
M=M+1
@17
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
D;JEQ
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
@17
D=A
@SP
A=M
M=D
@SP
M=M+1
@16
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
@CONDITIONALJUMP.TRUE.1
D;JEQ
D=0
@CONDITIONALJUMP.END.1
0;JMP
(CONDITIONALJUMP.TRUE.1)
D=-1
(CONDITIONALJUMP.END.1)
@R14
A=M
M=D
@SP
M=M+1
@16
D=A
@SP
A=M
M=D
@SP
M=M+1
@17
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
@CONDITIONALJUMP.TRUE.2
D;JEQ
D=0
@CONDITIONALJUMP.END.2
0;JMP
(CONDITIONALJUMP.TRUE.2)
D=-1
(CONDITIONALJUMP.END.2)
@R14
A=M
M=D
@SP
M=M+1
@892
D=A
@SP
A=M
M=D
@SP
M=M+1
@891
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
@CONDITIONALJUMP.TRUE.3
D;JLT
D=0
@CONDITIONALJUMP.END.3
0;JMP
(CONDITIONALJUMP.TRUE.3)
D=-1
(CONDITIONALJUMP.END.3)
@R14
A=M
M=D
@SP
M=M+1
@891
D=A
@SP
A=M
M=D
@SP
M=M+1
@892
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
@CONDITIONALJUMP.TRUE.4
D;JLT
D=0
@CONDITIONALJUMP.END.4
0;JMP
(CONDITIONALJUMP.TRUE.4)
D=-1
(CONDITIONALJUMP.END.4)
@R14
A=M
M=D
@SP
M=M+1
@891
D=A
@SP
A=M
M=D
@SP
M=M+1
@891
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
@CONDITIONALJUMP.TRUE.5
D;JLT
D=0
@CONDITIONALJUMP.END.5
0;JMP
(CONDITIONALJUMP.TRUE.5)
D=-1
(CONDITIONALJUMP.END.5)
@R14
A=M
M=D
@SP
M=M+1
@32767
D=A
@SP
A=M
M=D
@SP
M=M+1
@32766
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
@CONDITIONALJUMP.TRUE.6
D;JGT
D=0
@CONDITIONALJUMP.END.6
0;JMP
(CONDITIONALJUMP.TRUE.6)
D=-1
(CONDITIONALJUMP.END.6)
@R14
A=M
M=D
@SP
M=M+1
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1
@32767
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
@CONDITIONALJUMP.TRUE.7
D;JGT
D=0
@CONDITIONALJUMP.END.7
0;JMP
(CONDITIONALJUMP.TRUE.7)
D=-1
(CONDITIONALJUMP.END.7)
@R14
A=M
M=D
@SP
M=M+1
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1
@32766
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
@CONDITIONALJUMP.TRUE.8
D;JGT
D=0
@CONDITIONALJUMP.END.8
0;JMP
(CONDITIONALJUMP.TRUE.8)
D=-1
(CONDITIONALJUMP.END.8)
@R14
A=M
M=D
@SP
M=M+1
@57
D=A
@SP
A=M
M=D
@SP
M=M+1
@31
D=A
@SP
A=M
M=D
@SP
M=M+1
@53
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
M=M+D
@SP
M=M+1
@112
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
@SP
M=M-1
A=M

M=-M
@SP
M=M+1
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
M=M&D
@SP
M=M+1
@82
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
M=M|D
@SP
M=M+1
@SP
M=M-1
A=M

M=!M
@SP
M=M+1