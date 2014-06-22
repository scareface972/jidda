from collections import defaultdict

class EventContext(object):
    def __init__(self):
        self.events = defaultdict(list)

    def on(self, event):
        def wrapper(fn):
            self.events[event].append(fn)
            return fn
        return wrapper

    def off(self, event, handler=None):
        if handler is not None:
            self.events[event].remove(handler)
            return
        self.events[event] = []

    def trigger(self, event, *args, **kwargs):
        for item in self.events[event]:
            if not item(*args, **kwargs):
                break

    def mixin(self, obj):
        obj.on = self.on
        obj.off = self.off
        obj.trigger = self.trigger
