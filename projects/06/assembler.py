import os
import re


def peek_line(f):
    pos = f.tell()
    line = f.readline()
    f.seek(pos)
    return line


valid_symbol = r'[A-Za-z\.\$\:_][0-9A-Za-z\.\$\:_]*'
a_regex = r'\@([0-9]+|' + valid_symbol + r')'
l_regex = r'\(\s*(' + valid_symbol + r')\s*\)'
c_regex = r'.+'

predefined_symbol_table = {
    '': 0,
    '0': 0,
    'M': 1,
    'D': 2,
    'MD': 3,
    'A': 4,
    'AM': 5,
    'AD': 6,
    'AMD': 7,
    'JGT': 1,
    'JEQ': 2,
    'JGE': 3,
    'JLT': 4,
    'JNE': 5,
    'JLE': 6,
    'JMP': 7,
    'SP': 0,
    'LCL': 1,
    'ARG': 2,
    'THIS': 3,
    'THAT': 4,
    'SCREEN': 0x4000,
    'KBD': 0x6000
}
for i in range(16):
    predefined_symbol_table[f'R{i}'] = i

alu_oper_cmds = {
    '0': 0b101010,
    '1': 0b111111,
    '-1': 0b111010,
    'D': 0b001100,
    'A': 0b110000,
    'M': 0b110000,
    '!D': 0b001101,
    '!A': 0b110001,
    '!M': 0b110001,
    '-D': 0b001111,
    '-A': 0b110011,
    '-M': 0b110011,
    'D+1': 0b011111,
    'A+1': 0b110111,
    'M+1': 0b110111,
    'D-1': 0b001110,
    'A-1': 0b110010,
    'M-1': 0b110010,
    'D+A': 0b000010,
    'D+M': 0b000010,
    'D-A': 0b010011,
    'D-M': 0b010011,
    'A-D': 0b000111,
    'M-D': 0b000111,
    'D&A': 0b000000,
    'D&M': 0b000000,
    'D|A': 0b010101,
    'D|M': 0b010101
}


class SymbolTable:
    sym_table = {}
    cur_address = 0

    def __init__(self, start_address=0xA):
        self.sym_table = dict(**predefined_symbol_table)
        self.cur_address = start_address

    def parse(self, line):
        symbol = ''
        
        if match := re.match(a_regex, line):
            symbol = match.group(1)
        
        if match := re.match(l_regex, line):
            symbol = match.group(1)

        if symbol and symbol not in self.sym_table:
            self.sym_table[symbol] = self.cur_address
            self.cur_address += 1

        return 'hack'
    

class Command:
    text = ''
    command_type = ''
    symbol = ''
    dest = 0
    comp = 0
    jump = 0
    sym_table = {}

    def __init__(self, text, sym_table):
        self.text = text
        self.sym_table = sym_table
        self.set_command_type()

    def set_command_type(self):
        if match := re.match(a_regex, self.text):
            self.command_type = 'A'
            self.symbol = match.group(1)
            return
        
        if match := re.match(l_regex, self.text):
            self.command_type = 'L'
            self.set_symbol = match.group(1)
            return

        if match := re.match(c_regex, self.text):
            self.command_type = 'C'
            self.set_c_params()


    def set_c_params(self):
        equality = self.text.split('=')
        if len(equality) == 2:
            self.set_equality(equality[0], equality[1])
            return

        jump = self.text.split(';')
        if len(jump) == 2:
            self.set_jump(jump[0], jump[1])
            return

        raise Exception('Invalid C command')

    def set_equality(self, reg, oper):
        self.jump = 0
        self.dest = self.sym_table[reg]
        self.comp = alu_oper_cmds[oper]
        if 'M' in oper:
            self.comp += 0b1000000

    def set_jump(self, reg, code):
        self.dest = self.sym_table[reg]
        self.jump = self.sym_table[code]
        self.comp = alu_oper_cmds[reg]

    def get_symbol_val(self):
        return self.sym_table[self.symbol]

    def __str__(self):
        if self.command_type == 'A':
            return format(self.get_symbol_val(), '016b')
        if self.command_type == 'L':
            return ''

        instruction = (0b111 << 13) + (self.comp << 6) + (self.dest << 3) + self.jump
        return format(instruction, '016b')


class CommandLineParser:
    def __init__(self, sym_table):
        self.sym_table = sym_table

    def parse(self, line):
        return Command(line, self.sym_table)
    

class Parser:
    f = None
    line_parser = None
    cur_command = None

    def __init__(self, f_object, line_parser):
        self.f = f_object
        self.line_parser = line_parser

    def has_more_commands(self):
        return self.cur_command is not None or peek_line(self.f) != ''

    def advance(self):
        for line in f:
            cmd = self.clean_line(line)
            if cmd != '':
                self.cur_command = self.line_parser.parse(cmd)
                return
        self.cur_command = None

    def clean_line(self, line):
        return re.sub(r'\s+', ' ',
            re.sub(r'\/\/.*$', '', line)).strip()
    

if __name__ == '__main__':
    script_dir = os.path.dirname(os.path.realpath(__file__))
    filename = os.path.join(script_dir, 'max/Max.asm')
    
    sym = SymbolTable()
    with open(filename, 'r') as f:
        sym_parser = Parser(f, sym)
        sym_parser.advance()
        while sym_parser.has_more_commands():
            sym_parser.advance()

    with open(filename, 'r') as f:
        parser = Parser(f, CommandLineParser(sym.sym_table))
        parser.advance()
        while parser.has_more_commands():
            line = str(parser.cur_command)
            if line:
                print(line)
            parser.advance()
    
    