import re
import os
import sys
import optparse


class AssemblerError(Exception):
    pass


opcodes = {
    "nop": int("000000", 2),
    "add": int("000000", 2),
    "sub": int("000000", 2),
    "mult": int("000000", 2),
    "mulu": int("000000", 2),
    "div": int("000000", 2),
    "divu": int("000000", 2),
    "slt": int("000000", 2),
    "sltu": int("000000", 2),
    "and": int("000000", 2),
    "or": int("000000", 2),
    "nor": int("000000", 2),
    "xor": int("000000", 2),
    "addi": int("001000", 2),
    "slti": int("001010", 2),
    "sltiu": int("001011", 2),
    "andi": int("001100", 2),
    "ori": int("001101", 2),
    "xori": int("001110", 2),
    "lw": int("100011", 2),
    "sw": int("101011", 2),
    "pop": int("111000", 2),
    "push": int("111000", 2),
    "beq": int("000100", 2),
    "bne": int("000101", 2),
    "blez": int("000110", 2),
    "bgtz": int("000111", 2),
    "bltz": int("000001", 2),
    "j": int("000010", 2),
    "jr": int("000000", 2),
    "mfhi": int("000000", 2),
    "mflo": int("000000", 2),
    "halt": int("111111", 2),
    "tty": int("111111", 2),
    "rnd": int("111111", 2),
    "kbd": int("111111", 2),
}

functs = {
    "nop": int("000000", 2),
    "add": int("100000", 2),
    "sub": int("100010", 2),
    "mult": int("011000", 2),
    "mulu": int("011001", 2),
    "div": int("011010", 2),
    "divu": int("011011", 2),
    "slt": int("101010", 2),
    "sltu": int("101011", 2),
    "and": int("100100", 2),
    "or": int("100101", 2),
    "nor": int("100111", 2),
    "xor": int("101000", 2),
    "pop": int("000000", 2),
    "push": int("000001", 2),
    "jr": int("001000", 2),
    "mfhi": int("010000", 2),
    "mflo": int("010010", 2),
    "halt": int("111111", 2),
    "tty": int("000001", 2),
    "rnd": int("000010", 2),
    "kbd": int("000100", 2),
}


def print_instructions(instructions, outputdir):

    hex_instructions = [("%04x" % inst).zfill(8) for inst in instructions]
    little_endian = [
        inst[6:8] + inst[4:6] + inst[2:4] + inst[0:2] for inst in hex_instructions
    ]

    used = little_endian
    bank0 = used[0::4]
    bank1 = used[1::4]
    bank2 = used[2::4]
    bank3 = used[3::4]

    for bank_name, bank in zip(
        ["Bank0", "Bank1", "Bank2", "Bank3"], [bank0, bank1, bank2, bank3]
    ):
        bf = open(os.path.join(outputdir, bank_name), "w")
        bf.write("v2.0 raw\n")
        bf.write(" ".join(bank))
        bf.close()
    with open(os.path.join(outputdir, "Bank"), "w") as file:
        file.write("v2.0 raw\n")
        file.write("\n".join(used))
        file.write("\nffffffff\n")



def parse_nasm_instructions(inputfile):

    # instr = rtype_0.group("instr")
    # funct = functs[instr]
    # opcode = opcodes[instr]
    # rd, rs, rt = 0, 0, 0
    # num = opcode << 26 | rs << 21 | rt << 16 | rd << 11 | funct

    instructions = []
    for line in input_file:
        instructions.append(1)

    return instructions




if __name__ == "__main__":
    usage = "%prog infile [options]"
    parser = optparse.OptionParser(usage=usage)
    parser.add_option(
        "-o",
        "--out",
        dest="output_folder",
        type="string",
        default=".",
        help="Specify output folder to write the 4 memory bank dumps.",
    )
    parser.add_option(
        "-v",
        "--verbose",
        dest="verbose",
        action="store_true",
        default=False,
        help="Verbose debug mode",
    )
    options, args = parser.parse_args()
    if len(args) != 1:
        parser.error("Incorrect command line arguments")
        sys.exit(1)

    verbose = options.verbose

    output_folder = options.output_folder
    input_file = args[0]
    # if re.match(r""".*(?P<extension>\.s)$""",input_file,re.I) and output_file == 'a.hex':
    # output_file = input_file[:-1] + "hex"



    try: # ABRIR EL DOCUMENTO
        infile = open(input_file)
    except IOError as e:
        print >> sys.stderr, "Unable to open input file %s" % input_file
        sys.exit(1)

    try: # PARSEAR EL DOCUMENTO
        instructions = parse_nasm_instructions(infile)
        infile.close()
    except AssemblerError as e:
        print >> sys.stderr, str(e)
        sys.exit(1)

    try: # COPIA LAS INSTRUCCIONES EN LOS FICHEROS BANCOS
        print_instructions(instructions, output_folder)
    except IOError as e:
        print >> sys.stderr, "Unable to write to output file %s" #% output_file
        sys.exit(1)
    sys.exit(0)
