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

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1

    def ram_read(self, MAR):
        # Should accept the address to read and return the value stored there.
        return self.ram[MAR]
    
    def ram_write(self, MDR, MAR):
        # Should accept a value to write, and the address to write it to.
        self.ram[MAR] = MDR

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
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
        pc = 0 # Program Counter, address of the currently executing instruction
        running = True

        while running:
            ir = self.ram_read(self.pc) # Instruction Register, contains a copy of the currently executing instruction

            operand_1 = self.ram_read(self.pc + 1)
            operand_2 = self.ram_read(self.pc + 2)
            
            if ir == '10000010': # LDI
                self.registers[operand_1] = operand_2
                pc += 3

            elif ir == '01000111': # PRN
                print(self.registers[operand_1])
                pc += 2

            elif ir == '00000001': # HLT
                running = False
                pc += 1

            else:
                print(f"Unknown instruction")
