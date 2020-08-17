import re


keywords = '''
class
constructor
function
method
field
static
var
int
char
boolean
void
true
false
null
this
let
do
if
else
while
return
'''.strip().split('\n')

def match_keyword(token):
    return re.match(f'\\b({")|(".join(keywords)})\\b', token)


def remove_comments(text):
    return re.sub(r'(?:\/\*[\s\S]*?\*\/)|(?:\/\/.*$)', '', text)


print(match_keyword('class something'))
