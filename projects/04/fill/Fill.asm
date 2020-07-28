// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.

(LOOP)

@24576
D=M     // get keyboard pressed button
@140
D=D-A
@END
D;JEQ   // stop if esc is pressed

@24576
D=M
@BLACK
D;JGT
@LOOP
0;JMP

(BLACK)
@16384
D=A
@i
M=D
(BLOOP)
@i
D=M
@24576
D=A-D
@LOOP
D;JLE

@24576
D=M     // get keyboard pressed button
@CLEAR
D;JEQ
// @-1
D=-1
@i
A=M
M=D
@i
M=M+1
@BLOOP
0;JMP

(CLEAR)
@16384
D=A
@i
M=D
(CLOOP)
@i
D=M
@24576
D=A-D
@LOOP
D;JLE

@24576
D=M     // get keyboard pressed button
@LOOP
D;JGT

@i
A=M
M=0
@i
M=M+1
@CLOOP
0;JMP

(END)