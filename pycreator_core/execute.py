import sys
import traceback
from codeop import CommandCompiler
from pycreator_core.utils import FakeStdout


__all__ = ["execute_interactive", "execute_file"]


class Interpreter:
    def __init__(self, locals=None):
        if locals is None:
            locals = {"__name__": "__console__", "__doc__": None}
        self.locals = locals
        self.compile = CommandCompiler()

    def runsource(self, source, filename="<input>", symbol="single"):
        try:
            code = self.compile(source, filename, symbol)
        except (OverflowError, SyntaxError, ValueError):
            # Case 1
            return self.showsyntaxerror(filename)

        if code is None:
            # Case 2
            return

        # Case 3
        return self.runcode(code)

    def runcode(self, code):
        try:
            return exec(code, self.locals)
        except SystemExit:
            raise
        except:
            return self.showtraceback()

    @staticmethod
    def showsyntaxerror(filename=None):
        type, value, tb = sys.exc_info()
        sys.last_type = type
        sys.last_value = value
        sys.last_traceback = tb
        if filename and type is SyntaxError:
            # Work hard to stuff the correct filename in the exception
            try:
                msg, (dummy_filename, lineno, offset, line) = value.args
            except ValueError:
                # Not the format we expect; leave it alone
                pass
            else:
                # Stuff in the right filename
                value = SyntaxError(msg, (filename, lineno, offset, line))
                sys.last_value = value
        lines = traceback.format_exception_only(type, value)
        return ''.join(lines)

    @staticmethod
    def showtraceback():
        sys.last_type, sys.last_value, last_tb = ei = sys.exc_info()
        sys.last_traceback = last_tb
        try:
            lines = traceback.format_exception(ei[0], ei[1], last_tb.tb_next)
            return ''.join(lines)
        finally:
            last_tb = ei = None


def execute_interactive(code):
    return Interpreter().runsource(code)


def execute_file(code):
    return Interpreter().runsource(code, "code.py", "exec")