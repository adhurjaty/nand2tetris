import os
import re


script_dir = os.path.dirname(os.path.realpath(__file__))


def unindent_multiline(s):
    return '\n'.join(line.strip() for line in s.split('\n')).strip()


operations_dict = {
    'add': '+',
    'sub': '-'
}


def const_fn(arg):
    return f'@{arg}'


def symbol_fn(const, arg):
    return unindent_multiline(f'''
        @{arg}
        D=A
        @{const}
        A=M+D
        ''')


def local_fn(arg):
    return symbol_fn('LCL', arg)


def arg_fn(arg):
    return symbol_fn('ARG', arg)


def this_fn(arg):
    return symbol_fn('THIS', arg)


def that_fn(arg):
    return symbol_fn('THAT', arg)


def temp_fn(arg):
    offset = str(5 + int(arg))
    return f'@{offset}'


symbol_fns = {
    'constant': const_fn,
    'local': local_fn,
    'argument': arg_fn,
    'this': this_fn,
    'that': that_fn,
    'temp': temp_fn,
    'static': None,
    'pointer': None
}

class Command:
    arg1 = ''
    arg2 = ''

    def cmd_str(self, *args, **kwargs):
        raise Exception('cannot call cmd_str on abstract command')

    def increment_sp(self):
        return unindent_multiline('''
            @SP
            M=M+1
            ''')

    def decrement_sp(self):
        return unindent_multiline('''
            @SP
            M=M-1
            ''')


class ReturnCommand(Command):
    def cmd_str(self):
        return 'probably a jump statement'


class ArithmeticCommand(Command):
    def __init__(self, arg):
        self.arg1 = arg

    def cmd_str(self):
        operation = operations_dict[self.arg1]
        return unindent_multiline(f'''
            {self.decrement_sp()}
            A=M
            D=M
            {self.decrement_sp()}
            A=M
            M=M{operation}D
            {self.increment_sp()}
            ''')


class StackChangeCommand(Command):
    def __init__(self, tokens):
        self.arg1 = tokens[0]
        self.arg2 = tokens[1]


class PushCommand(StackChangeCommand):
    def __init__(self, tokens):
        super().__init__(tokens)

    def cmd_str(self):
        val = 'A' if self.arg1 == 'constant' else 'M'
        return unindent_multiline(f'''
            {symbol_fns[self.arg1](self.arg2)}
            D={val}
            @SP
            A=M
            M=D
            {self.increment_sp()}
            ''')


class PopCommand(StackChangeCommand):
    def __init__(self, tokens):
        super().__init__(tokens)

    def cmd_str(self):
        return unindent_multiline(f'''
            {symbol_fns[self.arg1](self.arg2)}
            D=A
            @R13
            M=D
            {self.decrement_sp()}
            @SP
            A=M
            D=M
            @R13
            A=M
            M=D
            ''')


class Parser:
    f = None

    def __init__(self, f):
        self.f = f

    def parse(self):
        for line in self.f:
            cleaned_line = self.clean_line(line)
            if cleaned_line:
                yield self.create_command(cleaned_line)

    def clean_line(self, line):
        return re.sub(r'\s+', ' ',
            re.sub(r'\/\/.*$', '', line)).strip()
    
    def create_command(self, line):
        tokens = line.split()

        if tokens[0] == 'return':
            return ReturnCommand(tokens)
        if tokens[0] in operations_dict.keys():
            return ArithmeticCommand(tokens[0])
        if tokens[0] == 'push':
            return PushCommand(tokens[1:])
        if tokens[0] == 'pop':
            return PopCommand(tokens[1:])        

        raise Exception('invalid instruction')


def translate(commands):
    return '\n'.join(c.cmd_str() for c in commands)


def change_ext(filename, ext):
    basename = os.path.basename(filename)
    basename = basename.split('.')[0]
    return os.path.join(os.path.dirname(filename), f'{basename}.{ext}')


def translate_file(name):
    filename = os.path.join(script_dir, name)
    out_file = change_ext(filename, 'asm')

    with open(filename, 'r') as f:
        cmds = list(Parser(f).parse())

    with open(out_file, 'w') as f:    
        f.write(translate(cmds))


if __name__ == '__main__':
    # filename = os.path.join(script_dir, 'StackArithmetic/SimpleAdd/SimpleAdd.vm')
    filename = os.path.join(script_dir, 'MemoryAccess/BasicTest/BasicTest.vm')
    translate_file(filename)