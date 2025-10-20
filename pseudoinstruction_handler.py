"""

 Pseudoinstruction Handler

 Helper functions for the CSSE232 Assembler. 
 Processes assembly code to replace pseudoinstructions with 
 core instructions.

 VVV Put your name here VVV

 Author: Robert J Williamson, 2024

 NAMES:
 Borui Liu
 Jack Lucas

"""

import assembler

def get_pseudoinstruction_defs():
    """Returns a dictionary mapping pseudoinstruction names to methods 
        that will translate a given pseudoinstruction call to a list of 
        core instructions. Each of these function should have the 
        signature: `func(inst_string, line_num)`"""
    pseudo_dict = {"double":double,
                   "diffsums":diffsums,
                   "push":push,
                   "li":li,
                   "beqz":beqz,
                   "jalif":jalif}

    return pseudo_dict

##############
#
# Individual definitions for pseudoinstructions
#
# Each of these functions should take in a string (e.g. "double t0, t1")
# and the line number from the original code that is being translated.
# The line number is mostly for error tracing, but you may find it
# useful for some pseudoinstructions.
##############

def double(inst, num):
    """Takes a string representing a call to the `double` pseudoinstruction. 
        Returns a list of strings containing the calls for the core instructions 
        which implement this pseudoinstruction.

        Behavior:
            `double r1, r2 -> Reg[r1] = 2 * r2`
        """

    #DONE: Practical 2 - implement this
    split_inst = inst.strip().replace(",", " ").split()
    if len(split_inst) != 3:
        raise assembler.BadOperands(f"double expects 2 operands on line")
    r1 = split_inst[1]
    r2 = split_inst[2]

    return [f"add {r1}, {r2}, {r2}"]

def diffsums(inst, num):
    """Takes a string representing a call to the `diffsums` pseudoinstruction. 
        Returns a list of strings containing the calls for the core instructions 
        which implement this pseudoinstruction.

        Behavior:
            `diffsums r1, r2, r3, r4, r5 -> Reg[r1] = (r2 + r3) - (r4 + r5)`

        Note: the same register may be used multiple times in this instruction, e.g.:
            `diffsums t0, t0, t1, t0, t2`
        """

    #DONE: Practical 2 - implement this
    split_inst = inst.strip().replace(",", " ").split()
    if len(split_inst) != 6:
        raise assembler.BadOperands(f"diffsums expects 5 operands on line")
    rt = split_inst[1]
    r2 = split_inst[2]
    r3 = split_inst[3]
    r4 = split_inst[4]
    r5 = split_inst[5]
    return [f"add x31, {r2}, {r3}",
            f"sub x31, x31, {r4}",
            f"sub {rt}, x31, {r5}"
            ]



def push(inst, num):
    """Takes a string representing a call to the `push` pseudoinstruction. 
        Returns a list of strings containing the calls for the core instructions 
        which implement this pseudoinstruction.

        Behavior:
            `push r1 -> sp = sp-4 ; Mem[sp] = r1`
        """

    #DONE: Practical 2 - implement this
    split_inst = inst.strip().replace(",", " ").split()
    if len(split_inst) != 2:
        raise assembler.BadOperands(f"push expects 1 operands on line")
    r1 = split_inst[1]
    if not assembler.is_register_name(r1):
        raise assembler.BadRegister(f"Invalid register {r1} in push on line {num}: {inst}")
    return [
        f"addi sp, sp, -4",
        f"sw {r1}, 0(sp)"
    ]

def li(inst, num):
    """Takes a string representing a call to the `li` pseudoinstruction. 
        Returns a list of strings containing the calls for the core instructions 
        which implement this pseudoinstruction.

        Behavior:
            `li rd, imm -> rd = imm`

        You should assume that imm can be up to 32 bits.

        Recall that the assembler assumes all immediates are in decimal.
        """

    #DONE: Practical 2 - implement this
    split_inst = inst.strip().replace(",", " ").split()
    if len(split_inst) != 3:
        raise assembler.BadOperands(f"li expects 2 operands on line")
    rd = split_inst[1]
    imm = split_inst[2]
    if not assembler.is_register_name(rd):
        raise assembler.BadRegister(f"Invalid register {rd} in li on line {num}: {inst}")
    if not assembler.is_int(imm):
        raise assembler.BadImmediate(f"Immediate {imm} is not an integer on line {num}: {inst}")
    nimm = int(imm)
    upper = (nimm + (1 << 11)) >> 12   
    lower = nimm - (upper << 12)     

    return [f"lui {rd}, {upper}", f"addi {rd}, {rd}, {lower}"]


def beqz(inst, num):
    """Takes a string representing a call to the `beqz` pseudoinstruction. 
        Returns a list of strings containing the calls for the core instructions 
        which implement this pseudoinstruction.

        Behavior:
            `beqz r1, LABEL -> if(r1 == 0) PC = LABEL`

        You can assume LABEL should fit into 12 bits.
        """

    #DONE: Practical 2 - implement this
    split_inst = inst.strip().replace(",", " ").split()
    if len(split_inst) != 3:
        raise assembler.BadOperands(f"beqz expects 2 operands on line")
    rd = split_inst[1]
    label = split_inst[2]
    if not assembler.is_register_name(rd):
        raise assembler.BadRegister(f"Invalid register {rd} in beqz on line {num}: {inst}")
    if assembler.is_int(label):
        number = int(label)
        if number%4 !=0:
            raise assembler.BadImmediate(f"Immediate {label} is not a multiple of 4 on line {num}: {inst}")
    elif not assembler.is_register_name(label):
        pass
    else:
        raise assembler.BadImmediate(f"Immediate {label} is not a valid label or number on line {num}: {inst}")

    return [f"beq {rd}, x0, {label}"]

def jalif(inst, num):
    """Takes a string representing a call to the `jalif` pseudoinstruction. 
        Returns a list of strings containing the calls for the core instructions 
        which implement this pseudoinstruction.

        Behavior:
            `jalif r1, r2, LABEL -> if(r1 == r2) {ra = PC+4; PC=LABEL}`

        You can assume LABEL should fit into 20 bits.

        Note: Make sure this code works if a program has multiple `jalif` instructions...
        """

    #DONE: Practical 2 - implement this
    split_inst = inst.strip().replace(",", " ").split()
    if len(split_inst) != 4:
        raise assembler.BadOperands(f"jalif expects 3 operands on line")
    r1 = split_inst[1]
    r2 = split_inst[2]
    label = split_inst[3]
    if assembler.is_int(label):
        number = int(label)
        if number%4 !=0:
            raise assembler.BadImmediate(f"Immediate {label} is not a multiple of 4 on line {num}: {inst}")
    elif not assembler.is_register_name(label):
        pass
    else:
        raise assembler.BadImmediate(f"Immediate {label} is not a valid label or number on line {num}: {inst}")
    next = f"next{num}"    
    return [
        f"bne {r1}, {r2}, {next}",
        f"jal ra, {label}",
        f"{next}:"
    ]

##############
#
# Helper methods
#
##############

def replace_all(sym, val, slist):
    """Replaces all instances of `sym` with `val` in each string in the list `slist`."""
    new_slist = []
    for s in slist:
        new_slist.append(s.replace(sym, str(val)))
    return new_slist
