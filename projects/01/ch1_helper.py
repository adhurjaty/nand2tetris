def and16():
    return '\n'.join((f'And(a=a[{i}], b=b[{i}], out=out[{i}]);' for i in range(16)))


def mux16():
    return '\n'.join((f'Mux(a=a[{i}], b=b[{i}], sel=sel, out=out[{i}]);' for i in range(16)))


def mux4way16():
    template = '''
Mux(a=a[{i}], b=b[{i}], sel=sel[0], out=ab{i});
Mux(a=c[{i}], b=d[{i}], sel=sel[0], out=cd{i});
Mux(a=ab{i}, b=cd{i}, sel=sel[1], out=out[{i}]);
    '''.strip()

    return '\n'.join((template.format(i=i) for i in range(16)))


def mux8way16():
    template = '''
Mux4Way16(a=a[{i}], b=b[{i}], sel=sel[0], out=ab{i});
Mux(a=c[{i}], b=d[{i}], sel=sel[0], out=cd{i});
Mux(a=ab{i}, b=cd{i}, sel=sel[1], out=out[{i}]);
    '''.strip()

    return '\n'.join((template.format(i=i) for i in range(16)))


not16 = '\n'.join(f'Not(in=in[{i}], out=out[{i}]);' for i in range(16))
or16 = '\n'.join(f'Or(a=a[{i}], b=b[{i}], out=out[{i}]);' for i in range(16))
print(or16)