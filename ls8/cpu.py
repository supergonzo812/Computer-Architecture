"""CPU functionality."""

import sys

LDI = 0b10000010
PRN = 0b01000111
HLT = 0b00000001
MUL = 0b10100010

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # Create storage for the memory
        self.ram = [0] * 256

        # Create general purpose registers
        self.register = [0] * 8
        # Create a program counter
        self.pc = 0
        self.running = True

    def read_from_memory(self, MAR):
        # MAR = Memory Address Register
        return self.ram[MAR]

    def write_to_memory(self, MAR, MDR):
        # MDR = Memory Data Register
        self.ram[MAR] = MDR

    def load(self):
        """Load a program into memory."""
        address = 0
        file_name = sys.argv[1]

        with open(file_name) as files:
            for address, line in enumerate(files):
                line = line.split("#")
                try:
                    value = int(line[0], 2)
                except ValueError:
                    continue
                self.write_to_memory(address, value)


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        elif op == "MUL"
            self.register[reg_a] *= self.register[reg_b]
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
        
    def ldi(self):
        operand_1 = self.read_from_memory(self.pc + 1)
        operand_2 = self.read_from_memory(self.pc +2)

        self.register[operand_1] = operand_2
        self.pc += 3
    
    def prn(self):
        # Print the value stored at the given register
        operand_1 = self.read_from_memory(self.pc + 1)
        print(operand_1)

        self.pc += 2

    def hlt(self):
        self.running = False

    def mul(self):
        operand_1 = self.read_from_memory(self.pc + 1)
        operand_2 = self.read_from_memory(self.pc + 2)

        self.alu("MUL", operand_1, operand_2)

        self.pc += 3

    def call_function(self, n):

        branch_table = {
            LDI = self.ldi,
            PRN = self.prn,
            HLT = self.hlt,
            MUL = self.mul
        }

        files = branch_table

        if branch_table.get(n) is not None:
            files()
        else:
            print(f'Unknown command {n}')
            sys.exit(1)
    

    def run(self):
  
        while self.running:
            # Make an instruction register to read the memory address that is stored in the the PC register
            IR = self.read_from_memory(self.pc)
            self.call_function(IR)
