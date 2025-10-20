; Borui Liu
; Jack Lucas

START:li sp, 4198400 ; expect lui 1025, addi 0
    li t0, 4097 ; expect lui 1, addi 1
    li t1, -1 ; expect lui 0, addi -1 because sign extension
    double t2, t1 ; expect add t2, t1, t1
    diffsums t3, t0, t2, t1, t0 ; expect add x31, t2, t1 ; sub x31, x31, t1 ; sub t3, x31, t0
    beqz t0, 4 ; expect beq t0, x0, 4
    double t4, t0 ; expect add t4, t0, t0
    li t0, 0 ; expect lui 0, addi 0
    beqz t0, SKIP ; exoect beq t0, x0, SKIP
    double t5, t5 ; expect add t5, t5, t5
SKIP:li a0, 5 ; expect lui 0, addi 5
    li a1, 10240 ; expect lui 3, addi -2048
    jalif a0, a1, TARGET ; expect bne a0, a1, next12 ; jal ra, TARGET ; next12
    double a0, a0 ; expect add a0, a0, a0
    push ra ; expect addi sp, sp, -4 ; sw ra, 0(sp)
TARGET:double a1, a1 ; expect add a1, a1, a1
END:beqz x0, END ; expect beq x0, x0, END

