import sys
import struct
import json

# Define the opcodes
OPCODES = {
    'LOAD_CONST': 66,    # Opcode for loading a constant
    'READ_MEM': 165,     # Opcode for reading from memory
    'WRITE_MEM': 187,    # Opcode for writing to memory
    'POW': 47            # Opcode for pow() operation
}

def assemble_instruction(instruction):
    parts = instruction.strip().split()
    if not parts:
        return None, None

    mnemonic = parts[0]
    if mnemonic not in OPCODES:
        raise ValueError(f"Unknown instruction '{mnemonic}'")

    opcode = OPCODES[mnemonic]
    operand = int(parts[1])

    # Prepare the instruction based on mnemonic
    if mnemonic == 'LOAD_CONST':
        # Bits 0-7: opcode (8 bits)
        # Bits 8-29: constant (22 bits)
        if operand >= (1 << 22):
            raise ValueError("Constant too large for LOAD_CONST")
        instruction_word = (operand << 8) | opcode
    elif mnemonic == 'READ_MEM':
        # Bits 0-7: opcode (8 bits)
        # Bits 8-18: offset (11 bits)
        if operand >= (1 << 11):
            raise ValueError("Offset too large for READ_MEM")
        instruction_word = (operand << 8) | opcode
    elif mnemonic == 'WRITE_MEM':
        # Bits 0-7: opcode (8 bits)
        # Bits 8-30: address (23 bits)
        if operand >= (1 << 23):
            raise ValueError("Address too large for WRITE_MEM")
        instruction_word = (operand << 8) | opcode
    elif mnemonic == 'POW':
        # Bits 0-7: opcode (8 bits)
        # Bits 8-30: address (23 bits)
        if operand >= (1 << 23):
            raise ValueError("Address too large for POW")
        instruction_word = (operand << 8) | opcode
    else:
        raise ValueError(f"Unhandled instruction '{mnemonic}'")

    # Convert instruction_word to 4-byte little-endian binary
    binary_instruction = struct.pack('<I', instruction_word)

    # Prepare log entry
    log_entry = {
        'mnemonic': mnemonic,
        'opcode': opcode,
        'operand': operand,
        'instruction_word': instruction_word
    }

    return binary_instruction, log_entry

def assemble(source_file_path, binary_file_path, log_file_path):
    # Указываем кодировку 'utf-8' при чтении исходного файла
    with open(source_file_path, 'r', encoding='utf-8') as source_file:
        lines = source_file.readlines()

    binary_instructions = []
    log_entries = []

    for line in lines:
        line = line.strip()
        if not line or line.startswith('#'):
            continue  # Пропускаем пустые строки и комментарии
        binary_instruction, log_entry = assemble_instruction(line)
        if binary_instruction:
            binary_instructions.append(binary_instruction)
            log_entries.append(log_entry)

    # Записываем бинарные инструкции
    with open(binary_file_path, 'wb') as binary_file:
        for binary_instruction in binary_instructions:
            binary_file.write(binary_instruction)

    # Сохраняем лог в формате JSON
    with open(log_file_path, 'w', encoding='utf-8') as log_file:
        json.dump(log_entries, log_file, indent=4, ensure_ascii=False)

def main():
    if len(sys.argv) != 4:
        print("Usage: python assembler.py <source_file> <binary_file> <log_file>")
        sys.exit(1)

    source_file_path = sys.argv[1]
    binary_file_path = sys.argv[2]
    log_file_path = sys.argv[3]

    assemble(source_file_path, binary_file_path, log_file_path)
    print(f"Assembly completed. Binary saved to '{binary_file_path}'. Log saved to '{log_file_path}'.")

if __name__ == '__main__':
    main()
