def parse_addr(string):
    if isinstance(string, tuple):
        return string
    addr, port = string.rsplit(':',1)
    return addr, int(port)

def runner_factory(instance, wrapper_class, before=None):
    def runner(*args, **kwargs):
        context = wrapper_class(*args, **kwargs)
        if before:
            before(context)
        try:
            instance.trigger('connect', context)
            instance.trigger('disconnect', context)
        except Exception as error:
            instance.trigger('error', context)
        finally:
            context.disconnect()
            instance.trigger('teardown', context)
    return runner
