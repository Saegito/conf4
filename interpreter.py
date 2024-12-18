import sys
import struct
import json

MEMORY_SIZE = 1024  # Adjust size as needed

class EVM:
    def __init__(self):
        self.accumulator = 0
        self.memory = [0] * MEMORY_SIZE

    def execute_instruction(self, instruction_word):
        opcode = instruction_word & 0xFF
        operand = instruction_word >> 8

        if opcode == 66:  # LOAD_CONST
            constant = operand & ((1 << 22) - 1)  # 22 bits
            self.accumulator = constant
        elif opcode == 165:  # READ_MEM
            offset = operand & ((1 << 11) - 1)  # 11 bits
            address = (self.accumulator + offset) % MEMORY_SIZE
            self.accumulator = self.memory[address]
        elif opcode == 187:  # WRITE_MEM
            address = operand & ((1 << 23) - 1)  # 23 bits
            address = address % MEMORY_SIZE
            self.memory[address] = self.accumulator
        elif opcode == 47:  # POW
            address = operand & ((1 << 23) - 1)  # 23 bits
            address = address % MEMORY_SIZE
            value = self.memory[address]
            self.accumulator = pow(self.accumulator, value)
        else:
            raise ValueError(f"Unknown opcode: {opcode}")

    def execute(self, binary_file_path):
        with open(binary_file_path, 'rb') as binary_file:
            while True:
                bytes_read = binary_file.read(4)
                if not bytes_read:
                    break
                instruction_word = struct.unpack('<I', bytes_read)[0]
                self.execute_instruction(instruction_word)

def interpret(binary_file_path, result_file_path, mem_start, mem_end):
    evm = EVM()
    evm.execute(binary_file_path)

    # Extract memory range
    memory_range = evm.memory[mem_start:mem_end]

    # Save to result file
    with open(result_file_path, 'w') as result_file:
        json.dump(memory_range, result_file, indent=4)

    print(f"Execution completed. Memory range saved to '{result_file_path}'.")

def main():
    if len(sys.argv) != 5:
        print("Usage: python interpreter.py <binary_file> <result_file> <mem_start> <mem_end>")
        sys.exit(1)

    binary_file_path = sys.argv[1]
    result_file_path = sys.argv[2]
    mem_start = int(sys.argv[3])
    mem_end = int(sys.argv[4])

    interpret(binary_file_path, result_file_path, mem_start, mem_end)

if __name__ == '__main__':
    main()
