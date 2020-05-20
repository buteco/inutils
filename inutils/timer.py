import time
from functools import wraps


class Timer:
    def __init__(self, label="", verbose=True, disable_ms=False, parent=None):
        self.verbose = verbose
        self.label = label
        self.disable_ms = disable_ms
        self.parent = parent
        self.level = 0
        self.start_time = -1
        self.end_time = -1
        self.report = ""

        if parent:
            self.level = parent.level + 1

    @property
    def root(self):
        root = self
        while root.parent is not None:
            root = root.parent
        return root

    @property
    def total(self):
        return format_time(self.total_time, disable_ms=self.disable_ms)

    @property
    def total_in_ms(self):
        return format_ms(self.total_time)

    @property
    def total_in_mins(self):
        return format_mins(self.total_time)

    def __enter__(self):
        self.start_time = time.perf_counter()
        self.print("{} start".format(self.label))

        return self

    def __exit__(self, *exc):
        self.end_time = time.perf_counter()
        self.total_time = self.end_time - self.start_time
        self.print("{} end ({})".format(self.label, self.total))

    def __call__(self, func):
        if not self.label:
            self.label = func.__name__

        @wraps(func)
        def inner(*args, **kwargs):
            with self:
                return func(*args, **kwargs)

        return inner

    def __repr__(self):
        parent = self.parent.label if self.parent else None
        return "<{}(label={!r}, parent={!r})>".format(type(self).__name__, self.label, parent)

    def print(self, *args):
        now = format_time(time.perf_counter() - self.root.start_time, disable_ms=True)
        prefix = "[{}]".format(now)
        prefix = "{:<11}".format(prefix)

        if self.level >= 1:
            prefix += "      " * self.level
            prefix = prefix[:-2] + "↳ "

        vals = (prefix, *args)
        output = " ".join(vals) + "\n"

        # FIXME: make this to work properly with parent/child
        self.report += output
        if self.root is not self:
            self.root.report += output

        if self.verbose:
            print(output, end="")

    def child(self, *args, **kwargs):
        return Timer(*args, parent=self, **kwargs)


def format_time(seconds, *, disable_ms=False):
    if seconds < 1 and not disable_ms:
        return format_ms(seconds)
    if seconds < 3600:
        return format_mins(seconds)
    return format_hours(seconds)


def format_ms(seconds):
    return "{:.0f}ms".format(seconds * 1000)


def format_mins(seconds):
    mins, secs = divmod(round(seconds), 60)
    return "{}m{:02}s".format(mins, secs)


def format_hours(seconds):
    mins, secs = divmod(round(seconds), 60)
    hours, mins = divmod(mins, 60)
    return "{}h{:02}m{:02}s".format(hours, mins, secs)
