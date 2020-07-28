@0
D=M
@i
M=D
@sum
M=0

(LOOP)

@i
D=M
@END
D;JLE
@1
D=M
@sum
M=M+D
@i
M=M-1
@LOOP
0;JMP

(END)

@sum
D=M
@2
M=D