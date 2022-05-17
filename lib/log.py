def git_hooks_logging(operation: str):
    def decorator(func):
        def wrapped_func(*args, **kwargs):
            print(f'GIT_HOOKS: {operation}...', end='', flush=True)
            value =  func(*args, **kwargs)
            print('done', flush=True)
            return value
        return wrapped_func
    return decorator


def git_hooks_logging_cmd(operation: str):
    return f'echo "GIT_HOOKS: {operation}...done"'
