import contextlib
import sys
from io import StringIO
import ast

@contextlib.contextmanager
def redirect_stdout(stdout=None):
    old = sys.stdout
    if stdout is None:
        stdout = StringIO()
    sys.stdout = stdout
    yield stdout
    sys.stdout = old

def exec_python(cmd: str) -> str:
    with redirect_stdout() as s:
        try:
            blocks = ast.parse(cmd, mode='exec')
            exec(compile(blocks, '<string>', mode='exec'), locals(), globals())
        except Exception as e:
            val = str(e)
        else:
            val = s.getvalue()[:-1]
        return val

def get_joke():
    r = requests.get('https://official-joke-api.appspot.com/random_joke')
    data = r.json()
    setup = data['setup']
    punch = data['punchline']
    return f'{setup} {punch}'