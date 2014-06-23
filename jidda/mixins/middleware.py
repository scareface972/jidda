class MiddlewareContext(object):
    def __init__(self):
        self.stack = []

    def use(self, fn):
        self.stack.append(fn)
        return fn

    def transform_request(self, request):
        for transformer in self.stack:
            request = transformer(request)
        return request

    def mixin(self, obj):
        obj.use = self.use
        obj.transform_request = self.transform_request

