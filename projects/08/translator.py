import os
import re


script_dir = os.path.dirname(os.path.realpath(__file__))


def unindent_multiline(s):
    return '\n'.join(line.strip() for line in s.split('\n')).strip()


cond_key = 0
def conditional(cond):
    global cond_key
    output = unindent_multiline(f'''
        M=M-D
        D=A
        @R14
        M=D
        A=M
        D=M
        @CONDITIONALJUMP.TRUE.{cond_key}
        D;J{cond}
        D=0
        @CONDITIONALJUMP.END.{cond_key}
        0;JMP
        (CONDITIONALJUMP.TRUE.{cond_key})
        D=-1
        (CONDITIONALJUMP.END.{cond_key})
        @R14
        A=M
        M=D
        ''')
    cond_key += 1
    return output


operations_dict = {
    'add': lambda: 'M=M+D',
    'sub': lambda: 'M=M-D',
    'neg': lambda: 'M=-M',
    'and': lambda: 'M=M&D',
    'or': lambda: 'M=M|D',
    'not': lambda: 'M=!M',
    'gt': lambda: conditional('GT'),
    'lt': lambda: conditional('LT'),
    'eq': lambda: conditional('EQ')
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


def pointer_fn(arg):
    if int(arg) >= 2:
        raise Exception('Cannot have a pointer arg > 1')

    symbol = 'THIS' if arg == '0' else 'THAT'
    return f'@{symbol}'


def static_fn_wrapper(name):
    def static_fn(arg):
        return f'@{name}.{arg}'

    return static_fn


class SymbolFns:
    symbol_fns = {
        'constant': const_fn,
        'local': local_fn,
        'argument': arg_fn,
        'this': this_fn,
        'that': that_fn,
        'temp': temp_fn,
        'static': None,
        'pointer': pointer_fn
    }

    def __init__(self, name):
        self.symbol_fns['static'] = static_fn_wrapper(name)

    def get(self, name):
        return self.symbol_fns.get(name) or (lambda a: symbol_fn(name, a))

    def is_constant(self, name):
        return name == 'constant' or name not in self.symbol_fns.keys()


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


class LabelCommand(Command):
    name = ''

    def __init__(self, name, label):
        self.name = name
        self.arg1 = label

    def jump_label(self):
        return f'{self.name}${self.arg1}'

    def cmd_str(self):
        return f'({self.jump_label()})'


class GotoCommand(LabelCommand):
    def __init__(self, name, label):
        super().__init__(name, label)

    def cmd_str(self):
        return unindent_multiline(f'''
            @{self.jump_label()}
            0;JMP
            ''')

class IfGotoCommand(LabelCommand):
    def __init__(self, name, label):
        super().__init__(name, label)

    def cmd_str(self):
        return unindent_multiline(f'''
            {self.decrement_sp()}
            A=M
            D=M
            @{self.jump_label()}
            D;JNE
            ''')


class ArithmeticCommand(Command):
    def __init__(self, arg):
        self.arg1 = arg

    def cmd_str(self):
        operation = operations_dict[self.arg1]()

        extra_pop = ''
        if 'D' in operation:
            extra_pop = unindent_multiline(f'''
                D=M
                {self.decrement_sp()}
                A=M
                ''')

        return unindent_multiline(f'''
            {self.decrement_sp()}
            A=M
            {extra_pop}
            {operation}
            {self.increment_sp()}
            ''')


class StackChangeCommand(Command):
    sym_fns = None

    def __init__(self, tokens, sym_fns):
        self.arg1 = tokens[0]
        self.arg2 = tokens[1]
        self.sym_fns = sym_fns


class PushCommand(StackChangeCommand):
    def cmd_str(self):
        val = 'A' if self.sym_fns.is_constant(self.arg1) else 'M'
        return unindent_multiline(f'''
            {self.sym_fns.get(self.arg1)(self.arg2)}
            D={val}
            @SP
            A=M
            M=D
            {self.increment_sp()}
            ''')


class PopCommand(StackChangeCommand):
    def cmd_str(self):
        return unindent_multiline(f'''
            {self.sym_fns.get(self.arg1)(self.arg2)}
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
        

class FunctionCommand(StackChangeCommand):
    def cmd_str(self):
        push = PushCommand(['constant', '0'], self.sym_fns)
        pushes = '\n'.join(push.cmd_str() for _ in range(int(self.arg2)))
        return unindent_multiline(f'''
            ({self.arg1})
            {pushes}
            ''')
    
    
class ReturnCommand(Command):
    sym_fns = None

    def __init__(self, sym_fns):
        self.sym_fns = sym_fns

    def cmd_str(self):
        pop = PopCommand(['argument', '0'], self.sym_fns)
        move_ptrs = '\n'.join(self.move_pointer(lbl) 
            for lbl in 'THAT THIS ARG LCL'.split())
        return unindent_multiline(f'''
            @LCL
            D=M
            @R15
            M=D
            @5
            A=D-A
            D=M
            @R14
            M=D
            {pop.cmd_str()}
            D=A
            @SP
            M=D+1
            {move_ptrs}
            @R14
            A=M
            0;JMP
            ''')

    def move_pointer(self, ptr_label):
        return unindent_multiline(f'''
            @R15
            M=M-1
            A=M
            D=M
            @{ptr_label}
            M=D
            ''')


class CallCommand(StackChangeCommand):
    func_usage = {}

    def cmd_str(self):
        jump_label = self.create_label()
        return unindent_multiline(f'''
            @{jump_label}
            D=A
            @SP
            A=M
            M=D
            {self.increment_sp()}
            {PushCommand(['LCL', '0'], self.sym_fns).cmd_str()}
            {PushCommand(['ARG', '0'], self.sym_fns).cmd_str()}
            {PushCommand(['THIS', '0'], self.sym_fns).cmd_str()}
            {PushCommand(['THAT', '0'], self.sym_fns).cmd_str()}
            @SP
            D=M
            @5
            D=D-A
            @{self.arg2}
            D=D-A
            @ARG
            M=D
            @SP
            D=M
            @LCL
            M=D
            @{self.arg1}
            0;JMP
            ({jump_label})
            ''')

    def create_label(self):
        if self.arg1 not in CallCommand.func_usage:
            CallCommand.func_usage[self.arg1] = 0
        CallCommand.func_usage[self.arg1] += 1
        return f'return${self.arg1}.{CallCommand.func_usage[self.arg1]}'


class InitCommand(Command):
    sym_fns = None

    def __init__(self, sym_fns):
        self.sym_fns = sym_fns

    def cmd_str(self):
        caller = CallCommand(['Sys.init', '0'], self.sym_fns)
        return unindent_multiline(f'''
            @256
            D=A
            @SP
            M=D
            {caller.cmd_str()}
            ''')


class Parser:
    f = None
    sym_fns = None
    name = ''

    def __init__(self, f, name):
        self.f = f
        self.name = name
        self.sym_fns = SymbolFns(name)

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

        if tokens[0] in operations_dict.keys():
            return ArithmeticCommand(tokens[0])
        if tokens[0] == 'push':
            return PushCommand(tokens[1:], self.sym_fns)
        if tokens[0] == 'pop':
            return PopCommand(tokens[1:], self.sym_fns)
        if tokens[0] == 'label':
            return LabelCommand(self.name, tokens[1])
        if tokens[0] == 'goto':
            return GotoCommand(self.name, tokens[1])
        if tokens[0] == 'if-goto':
            return IfGotoCommand(self.name, tokens[1])
        if tokens[0] == 'function':
            return FunctionCommand(tokens[1:], self.sym_fns)
        if tokens[0] == 'return':
            return ReturnCommand(self.sym_fns)
        if tokens[0] == 'call':
            return CallCommand(tokens[1:], self.sym_fns)

        raise Exception('invalid instruction')


def translate(commands):
    return '\n'.join(c.cmd_str() for c in commands)


def change_ext(filename, ext):
    basename = os.path.basename(filename)
    basename = basename.split('.')[0]
    return os.path.join(os.path.dirname(filename), f'{basename}.{ext}')


def translate_folder(name):
    folder = os.path.join(script_dir, name)
    basename = os.path.basename(folder)
    out_file = os.path.join(folder, f'{basename}.asm')

    vm_files = (os.path.join(folder, n) 
        for n in os.listdir(folder)
        if n.endswith('.vm') and not n.startswith('.'))
    
    cmds = [InitCommand(SymbolFns(basename))]
    for filename in vm_files:
        with open(filename, 'r') as f:
            cmds += list(Parser(f, basename).parse())

    with open(out_file, 'w') as f:    
        f.write(translate(cmds))


if __name__ == '__main__':
    translate_folder('FunctionCalls/StaticsTest')