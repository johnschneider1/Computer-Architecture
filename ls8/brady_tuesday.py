import sys
​
PRINT_BEEJ = 1  # 0000 0001
HALT = 2  # 0000 0010
PRINT_NUM = 3
SAVE = 4  # Saves a value to a registers
PRINT_REGISTER = 5
ADD = 6
​
​
​
memory = [0] * 256
registers = [0] * 8
​
​
pc = 0
running = True
​
​
​


def load_memory(filename):


​
try:
        address = 0
        with open(filename) as f:
            for line in f:
                # Ignore comments
                comment_split = line.split("#")
                num = comment_split[0].strip()
​
if num == "":
        continue  # Ignore blank lines
​
value = int(num)   # Base 10, but ls-8 is base 2
​
memory[address] = value
address += 1
​
except FileNotFoundError:
        print(f"{sys.argv[0]}: {filename} not found")
        sys.exit(2)
​
​
if len(sys.argv) != 2:
    print("Usage: file.py filename", file=sys.stderr)
    sys.exit(1)
​
load_memory(sys.argv[1])
​
print(memory)
​
while running:
    # Execute instructions in memory
​
command = memory[pc]
​
if command == PRINT_BEEJ:
        print("Beej!")
        pc += 1
​
elif command == PRINT_NUM:
        num = memory[pc+1]
        print(num)
        pc += 2
​
elif command == HALT:
        running = False
        pc += 1
​
elif command == SAVE:
        num = memory[pc + 1]
        reg = memory[pc + 2]
        registers[reg] = num
        pc += 3
​
elif command == ADD:
        reg_a = memory[pc + 1]
        reg_b = memory[pc + 2]
        registers[reg_a] += registers[reg_b]
        pc += 3
​
elif command == PRINT_REGISTER:
        reg = memory[pc + 1]
        print(registers[reg])
        pc += 2
​
else:
        print(f"Error: Unknown command: {command}")
        sys.exit(1)
