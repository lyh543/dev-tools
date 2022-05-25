def _log_started_str(operation: str):
    return f">>> GIT_HOOKS started: {operation}"

def _log_done_str(operation: str):
    return f">>> GIT_HOOKS done   : {operation}"

def git_hooks_logging(operation: str):
    def decorator(func):
        def wrapped_func(*args, **kwargs):
            print(_log_started_str(operation), flush=True)
            value = func(*args, **kwargs)
            print(_log_done_str(operation), flush=True)
            return value

        return wrapped_func

    return decorator


def git_hooks_logging_cmd_started(operation: str):
    return f'echo "{_log_started_str(operation)}"'

def git_hooks_logging_cmd_done(operation: str):
    return f'echo "{_log_done_str(operation)}"'
