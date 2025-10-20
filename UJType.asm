; Borui Liu
; Jack Lucas
LABEL:
add x5, x9, x0
jal x0, END ; expect 0000 0000 1000 0000 0000 0000 0110 1111
addi x5, x5, -1
END:
lui t2, 20
jal x1, -8 ; expect 1111 1111 1001 1111 1111 0000 1110 1111