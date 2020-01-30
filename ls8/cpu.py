"""CPU functionality."""


ldi = 0b10000010
prn = 0b01000111
hlt = 0b00000001
mul = 0b10100010
push = 0b01000101
pop = 0b01000110


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256

        self.reg = [0] * 8
        self.pc = 0

        self.sp = 7
        self.running = False

        self.reg[self.sp] = 0xF4

        self.branchtable = {}
        self.branchtable[ldi] = self.ldi
        self.branchtable[prn] = self.prn
        self.branchtable[hlt] = self.hlt
        self.branchtable[mul] = self.mul
        self.branchtable[push] = self.push
        self.branchtable[pop] = self.pop

    def ram_read(self, mar):
        return self.ram[mar]

    def ram_write(self, mar, mdr):
        self.ram[mar] = mdr

    def hlt(self):
        self.running = False

    def ldi(self):
        print("ldi")
        operand_a = self.ram_read(self.pc + 1)
        operand_b = self.ram_read(self.pc + 2)

        self.reg[operand_a] = operand_b
        self.pc += 3

    def prn(self):
        print("prn")
        operand_a = self.ram_read(self.pc + 1)

        print(self.reg[operand_a])
        self.pc += 2

    def mul(self):
        print("mul")
        operand_a = self.ram_read(self.pc + 1)
        operand_b = self.ram_read(self.pc + 2)

        self.reg[operand_a] * self.reg[operand_b]
        self.pc += 3

    def push(self):
        print("push")

        reg = self.ram[self.pc + 1]
        val = self.reg[reg]
        self.reg[self.sp] -= 1

        self.ram[self.reg[self.sp]] = val
        self.pc += 2

    def pop(self):
        print("pop")
        reg = self.ram[self.pc + 1]
        val = self.ram[self.reg[self.sp]]
        self.reg[reg] = val
        self.reg[self.sp] += 1
        self.pc += 2

    def load(self, filename):
        """Load a program into memory."""
        try:
            address = 0

            with open(filename) as f:
                for line in f:

                    comment_split = line.split("#")
                    num = comment_split[0].strip()
                    if num == "":
                        continue
                    value = int(num, 2)

                    self.ram[address] = value
                    address += 1
        except FileNotFoundError:
            print(f"{sys.argv[0]}: {filename} not found")
            sys.exit(2)

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]

        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""

        self.running = True

        while self.running:

            ir = self.ram[self.pc]
            print("ir", ir)
            self.branchtable[ir]()
