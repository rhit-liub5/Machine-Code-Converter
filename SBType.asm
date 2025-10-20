; Borui Liu
; Jack Lucas
START:
sw x0, 4(t0)
bne x0, t2, END ; expect 0000 0000 0111 0000 0001 1100 0110 0011
beq x0, t0, START ; expect 1111 1110 0101 0000 0000 1100 1110 0011
or t1, x0, t2
blt t4, t3, SKIP; expect 0000 0001 1100 1110 1100 0100 0110 0011
add t4, t4, t4
SKIP: bge t4, t3, START ; expect 1111 1111 1100 1110 1101 0100 1110 0011
END: addi t2, x0, 12