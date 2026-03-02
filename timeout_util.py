# Source used to build this helper function https://ashutoshvarma.github.io/blog/timeout-on-function-call-in-python?utm_source=chatgpt.com

import threading

def run_with_timeout(func, timeout, *args, **kwargs):
    result = {}
    error = {}
    # Set timeout to 60 if not provided
    if timeout is None:
        timeout = 60

    def wrapper():
        try:
            result["value"] = func(*args, **kwargs)
        except Exception as e:
            error["exception"] = e

    # We use thread and join with timeout
    thread = threading.Thread(target=wrapper)
    thread.start()
    thread.join(timeout)

    if thread.is_alive():
        raise TimeoutError("Function call timed out")

    if "exception" in error:
        raise error["exception"]

    
    return result.get("value")
