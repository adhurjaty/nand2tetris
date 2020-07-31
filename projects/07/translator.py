import os
import re


def unindent_multiline(s):
    return '\n'.join(line.strip() for line in s.split('\n')).strip()

operations_dict = {
    'add': '+',
    'sub': '-'
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
        return unindent_multiline(f'''
            @{self.arg2}
            D=A
            @SP
            A=M
            M=D
            {self.increment_sp()}
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


def translate(commands):
    return '\n'.join(c.cmd_str() for c in commands)


if __name__ == '__main__':
    script_dir = os.path.dirname(os.path.realpath(__file__))
    filename = os.path.join(script_dir, 'StackArithmetic/SimpleAdd/SimpleAdd.vm')
    
    with open(filename, 'r') as f:
        cmds = Parser(f).parse()
        print(translate(cmds))