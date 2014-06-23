from traceback import format_exc

def parse_addr(string):
    if isinstance(string, tuple):
        return string
    addr, port = string.rsplit(':',1)
    return addr, int(port)

def runner_factory(instance, wrapper_class, before=None):
    def runner(*args, **kwargs):
        request = wrapper_class(*args, **kwargs)
        if before: before(request)
        try:
            instance.trigger('connect', request)
            instance.trigger('disconnect', request)
        except Exception as error:
            instance.trigger('error', request)
        finally:
            request.disconnect()
            instance.trigger('teardown', request)
    return runner

def print_traceback_on_error(traceback):
    print(format_exc(traceback))
    return True
