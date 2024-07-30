import logging
from datetime import datetime

import rich
from rich import box, print
from rich.columns import Columns as Columnate
from rich.console import Console, Group
from rich.json import JSON
from rich.logging import RichHandler
from rich.padding import Padding
from rich.panel import Panel
from rich.pretty import Pretty
from rich.pretty import install as _install_rich_pprint
from rich.pretty import pprint
from rich.progress import Progress, track
from rich.prompt import Confirm, Prompt
from rich.syntax import Syntax
from rich.table import Column, Row, Table
from rich.text import Text
from rich.traceback import install as _install_rich_tracebacks
from rich.tree import Tree

_install_rich_tracebacks(show_locals=False)
_install_rich_pprint()

DATETIME_FMT = "%Y-%m-%d %H:%M:%S"
console = Console()
logger = logging.getLogger("IPython")
logger.setLevel(logging.DEBUG)
logger.addHandler(RichHandler(rich_tracebacks=True))


def moment(year, month=1, day=1, hour=0, minute=0, second=0, to_string=True):
    dt = datetime(
        year=year, month=month, day=day, hour=hour, minute=minute, second=second
    )
    if to_string:
        return dt.strftime(DATETIME_FMT)
    else:
        return dt


def clock(func, *args, **kwargs):
    start = datetime.now()
    with console.status(f"Calculating output of function {func.__qualname__}..."):
        result = func(*args, **kwargs)
    total = datetime.now() - start
    t = Table(
        show_header=False, show_lines=True, title="[italics]Benchmark results[/italics]"
    )
    t.add_column("Fields", style="blue")
    t.add_column("Values", style="magenta")
    t.add_row("Execution time:", f"{total} s")
    t.add_row("Result:", Pretty(result, max_string=40, max_depth=5, max_length=50))
    print(t)
    return result
