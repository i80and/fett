from typing import Any, Callable, Dict, List, Tuple
import re
import sys

TOKEN_COMMENT = sys.intern('comment')
TOKEN_ELSE = sys.intern('else')
TOKEN_END = sys.intern('end')
TOKEN_FOR = sys.intern('for')
TOKEN_IF = sys.intern('if')
TOKEN_LITERAL = sys.intern('literal')
TOKEN_SUB = sys.intern('sub')


def eat_error(f: Callable[[], Any]) -> Any:
    """Call f(), returning an empty string on error."""
    try:
        return f()
    except (IndexError, KeyError):
        return ''


class VariableStack:
    """Tracks variable scopes and loop counter depth."""
    __slots__ = ('stack', 'loop_counter')

    def __init__(self) -> None:
        self.stack = []  # type: List[str]
        self.loop_counter = 0

    def __contains__(self, value: str) -> bool:
        if value == 'i' and self.loop_counter > 0:
            return True

        return value in self.stack


class Template:
    """A compiled Fett template."""
    PAT = re.compile(r'\{\{[^{]+\}\}')
    ONLY_WHITESPACE_LEFT = re.compile(r'[^\S\n]*(?:\n|$)')
    ONLY_WHITESPACE_RIGHT = re.compile(r'(?:\n|^)[^\S\n]*$')
    NAME_PAT = re.compile(r'^[a-zA-Z0-9_]+$')
    FILTERS = {'odd': lambda x: int(x) % 2 != 0,
               'even': lambda x: int(x) % 2 == 0,
               'car': lambda x: x[0],
               'cdr': lambda x: x[1:],
               'len': lambda x: len(x),
               'strip': lambda x: str(x).strip(),
               'inc': lambda x: int(x) + 1,
               'not': lambda x: not x}

    def __init__(self, template: str) -> None:
        self.program_source = ''

        tasks = []  # type: List[Tuple[str, ...]]
        depth = 0
        a = 0
        b = 0
        for match in self.PAT.finditer(template):
            tag = match.group(0)[2:-2].strip()
            components = tag.split(None, 4)

            # Trim standalone tag whitespace
            start_of_line = max(0, template.rfind('\n', 0, match.start()))
            line_start = self.ONLY_WHITESPACE_RIGHT.match(template,
                                                          start_of_line,
                                                          match.start())
            line_end = self.ONLY_WHITESPACE_LEFT.match(template, match.end())
            if line_start and line_end and not self.is_interpolation(tag):
                skip_newline = 0 if line_start.start() == 0 else 1
                literal = template[a:line_start.start() + skip_newline]
                if literal:
                    tasks.append((TOKEN_LITERAL, literal))

                a = line_end.end()
                b = line_end.end()
            else:
                b = match.start()
                if a != b:
                    literal = template[a:b]
                    if literal:
                        tasks.append((TOKEN_LITERAL, literal))
                (a, b) = (match.end(), match.end())

            # Comment
            if tag.startswith('#'):
                tasks.append((TOKEN_COMMENT, tag))
                continue

            if len(components) >= 4 \
               and components[0] == 'for' \
               and components[2] == 'in':
                expr = ' '.join(components[3:])
                tasks.append((TOKEN_FOR, components[1], expr))
                depth += 1
            elif len(components) >= 2 and components[0] == 'if':
                tasks.append((TOKEN_IF, ' '.join(components[1:])))
            elif components and components[0] == 'else':
                tasks.append((TOKEN_ELSE,))
            elif components and components[0] == 'end':
                tasks.append((TOKEN_END,))
                depth -= 1
            else:
                start_of_line = max(0,
                                    template.rfind('\n', 0, match.start()) + 1)
                indentation = []
                while template[start_of_line] in (' ', '\t'):
                    indentation.append(template[start_of_line])
                    start_of_line += 1
                tasks.append((TOKEN_SUB, tag, ''.join(indentation)))

        literal = template[b:]
        if literal:
            tasks.append((TOKEN_LITERAL, literal))

        if depth > 0:
            raise ValueError('Expected "end"')

        try:
            self.program = self._compile(tasks)
        except SyntaxError as err:
            raise err.__class__('{}. Source:\n{}'.format(str(err),
                                                         self.program_source))

    def render(self, data: Dict[str, Any]) -> str:
        """Render this compiled template into a string using the given data."""
        env = self.FILTERS.copy()
        env['__eat_error__'] = eat_error

        gobj = {}  # type: Dict[str, Any]
        program = eval(self.program, env, gobj)
        program = gobj['run']

        try:
            generator = program(data)
            if generator:
                return ''.join([x for x in generator])

            return ''
        except Exception as err:
            raise err.__class__('{}. Source:\n{}'.format(str(err),
                                                         self.program_source))

    def _compile(self, tasks: List[Tuple[str, ...]]) -> Any:
        indent = 4
        need_pass = False
        local_stack = VariableStack()
        stack = []  # type: List[Tuple[str, ...]]
        program = ['def run(__data__):']

        for task in tasks:
            if task[0] is TOKEN_LITERAL:
                program.append(indent * ' ' + 'yield ' + repr(task[1]))
                need_pass = False
            elif task[0] is TOKEN_FOR:
                iter_name = self.vet_name(task[1])
                attr = self.transform_expr(task[2], local_stack)
                program.append('{}for i, {} in enumerate({}):'
                               .format(' ' * indent, iter_name, attr))
                stack.append((TOKEN_FOR, task[2]))
                local_stack.stack.append(task[1])
                local_stack.loop_counter += 1
                need_pass = True
                indent += 4
            elif task[0] is TOKEN_IF:
                attr = self.transform_expr(task[1], local_stack)
                program.append('{}if {}:'.format(' ' * indent, attr))
                stack.append((TOKEN_IF,))
                need_pass = True
                indent += 4
            elif task[0] is TOKEN_ELSE:
                if not stack:
                    raise ValueError('"else" without matching "for" or "if"')

                if need_pass:
                    program.append('{}pass'.format(' ' * indent))

                if stack[-1][0] is TOKEN_FOR:
                    attr = self.transform_expr(stack[-1][1], local_stack)
                    program.append('{}if not {}:'
                                   .format(' ' * (indent - 4), attr))
                elif stack[-1][0] is TOKEN_IF:
                    program.append('{}else:'.format(' ' * (indent - 4)))
                else:
                    assert False

                need_pass = True
            elif task[0] is TOKEN_END:
                if stack[-1][0] is TOKEN_FOR:
                    local_stack.stack.pop()
                    local_stack.loop_counter -= 1

                stack.pop()

                if need_pass:
                    program.append('{}pass'.format(' ' * indent))
                    need_pass = False

                indent -= 4
                if indent < 4:
                    raise ValueError('Unmatched "end"')
            elif task[0] is TOKEN_SUB:
                getter = self.transform_expr(task[1], local_stack)
                program.append('{}yield str({}).replace("\\n", "\\n" + {})'
                               .format(' ' * indent, getter, repr(task[2])))
                need_pass = False

        self.program_source = '\n'.join(program)
        return compile(self.program_source, 'renderer', 'exec')

    @classmethod
    def is_interpolation(cls, tag: str) -> bool:
        return not (tag.startswith('if ') or tag.startswith('for ') or
                    tag.startswith('#') or tag in ('else', 'end'))

    @classmethod
    def transform_expr(cls, expr: str, unmangle: VariableStack) -> str:
        """Transform a space-delimited sequence of tokens into a chained
           sequence of function calls."""
        components = expr.split(' ')
        result = components[0]
        components = components[1:]
        result = cls.dot_to_subscript(result, unmangle)

        while components:
            name = components.pop()
            if name not in cls.FILTERS:
                raise ValueError('Unknown filter: ' + name)

            result = '{}({})'.format(name, result)

        return result

    @classmethod
    def dot_to_subscript(cls, name: str, unmangle: VariableStack) -> str:
        """Transform a.b.c into data['a']['b']['c']."""
        path = name.split('.')

        from_local = False
        if len(path) >= 1 and path[0] in unmangle:
            from_local = True

        if from_local:
            if len(path) > 1:
                return path[0] + ''.join(['[{}]'.format(repr(x))
                                          for x in path[1:]])

            return name

        result = ''.join(['[{}]'.format(repr(cls.vet_name(x))) for x in path])
        return '__eat_error__(lambda: __data__' + result + ')'

    @classmethod
    def vet_name(cls, name: str) -> str:
        """Check if a name (field name or iteration variable) is legal."""
        if not cls.NAME_PAT.match(name):
            raise ValueError('Illegal name: ' + name)

        return name
