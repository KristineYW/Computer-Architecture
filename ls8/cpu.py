"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.registers = [0] * 8
        # R5 is reserved as the interrupt mask (IM)
        # R6 is reserved as the interrypt status (IS)
        # R7 is reserved as the stack pointer (SP)
        self.ram = [0] * 256
        self.pc = 0
        self.running = True
        self.opcodes = {
            0b10000010: self.LDI,
            0b01000111: self.PRN,
            0b00000001: self.HLT,
            0b10100010: self.MUL,
            0b10100011: self.DIV,
            0b10100000: self.ADD,
            0b10100001: self.SUB
        }

    def load(self):
        """Load a program into memory."""

        # address = 0

        # # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1

        if len(sys.argv) != 2:
            print("usage: python3 ls8.py examples/filename")
            sys.exit(1)

        try:
            address = 0

            with open(sys.argv[1]) as f:
                for line in f:
                    t = line.split('#')
                    n = t[0].strip()

                    if n == '':
                        continue

                    try:
                        n = int(n, 2)
                    except ValueError:
                        print(f"Invalid number '{n}'")
                        sys.exit(1)

                    self.ram[address] = n
                    address += 1

        except FileNotFoundError:
            print(f"File not found: {sys.argv[1]}")
            sys.exit(2)

    def ram_read(self, MAR):
        # Should accept the address to read and return the value stored there.
        return self.ram[MAR]
    
    def ram_write(self, MDR, MAR):
        # Should accept a value to write, and the address to write it to.
        self.ram[MAR] = MDR

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.registers[reg_a] += self.registers[reg_b]
        elif op == "MUL":
            self.registers[reg_a] *= self.registers[reg_b]
        elif op == "SUB":
            self.registers[reg_a] -= self.registers[reg_b] 
        elif op == "DIV":
            self.registers[reg_a] //= self.registers[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def LDI(self):
        operand_a = self.ram_read(self.pc + 1)
        operand_b = self.ram_read(self.pc + 2)
        self.registers[operand_a] = operand_b

    def PRN(self):
        operand_a = self.ram_read(self.pc + 1)
        print(self.registers[operand_a])

    def HLT(self):
        exit()

    def MUL(self):
        operand_1 = self.ram_read(self.pc + 1)
        operand_2 = self.ram_read(self.pc + 2)
        self.alu("MUL", operand_1, operand_2)
    
    def DIV(self):
        operand_1 = self.ram_read(self.pc + 1)
        operand_2 = self.ram_read(self.pc + 2)
        self.alu("DIV", operand_1, operand_2)

    def ADD(self):
        operand_1 = self.ram_read(self.pc + 1)
        operand_2 = self.ram_read(self.pc + 2)
        self.alu("ADD", operand_1, operand_2)

    def SUB(self):
        operand_1 = self.ram_read(self.pc + 1)
        operand_2 = self.ram_read(self.pc + 2)
        self.alu("SUB", operand_1, operand_2)

    def run(self):
        """Run the CPU.
        
        It needs to read the memory address that's stored in register PC, 
        and store that result in IR, the Instruction Register. 

        This can just be a local variable in run().

        Some instructions requires up to the next two bytes of data after the PC 
        in memory to perform operations on. 

        Sometimes the byte value is a register number, 
        other times it's a constant value (in the case of LDI). Using ram_read(), 
        read the bytes at PC+1 and PC+2 from RAM into variables operand_a and operand_b 
        in case the instruction needs them.

        Then, depending on the value of the opcode, 
        perform the actions needed for the instruction per the LS-8 spec. 
        Maybe an if-elif cascade...? There are other options, too.

        After running code for any particular instruction, 
        the PC needs to be updated to point to the next instruction for the 
        next iteration of the loop in run(). 
        The number of bytes an instruction uses can be determined from the two 
        high bits (bits 6-7) of the instruction opcode. See the LS-8 spec for details.
        """

        self.running = True

        # while self.running:

        #     ir = self.ram_read(self.pc) # Instruction Register, contains a copy of the currently executing instruction
            
        #     operand_1 = self.ram_read(self.pc + 1)
        #     operand_2 = self.ram_read(self.pc + 2)
            
        #     if ir == 0b10000010: # LDI
        #         self.registers[operand_1] = operand_2
        #         self.pc += 3

        #     elif ir == 0b01000111: # PRN
        #         print(self.registers[operand_1])
        #         self.pc += 2

        #     elif ir == 0b00000001: # HLT
        #         self.running = False
        #         self.pc += 1

        #     else:
        #         print(f"Unknown instruction")

        while self.running:
            ir = self.ram_read(self.pc)
            self.opcodes[ir]()
            number_of_operands = (ir & 0b11000000) >> 6
            how_far_to_move_pc = number_of_operands + 1
            self.pc += how_far_to_move_pc

