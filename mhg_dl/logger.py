class Logger:
    def __init__(self):
        self.verbose = False
        self._last_was_progress = False

    def set_verbose(self, verbose: bool):
        self.verbose = verbose

    def info(self, msg: str, end: str = "\n"):
        if self._last_was_progress and not self.verbose:
             print()
        
        print(msg, end=end)
        self._last_was_progress = False

    def progress(self, msg: str):
        if self.verbose:
            print(msg)
            self._last_was_progress = False
        else:
            print("\033[K", end="") 
            print(f"{msg}", end="\r", flush=True)
            self._last_was_progress = True

    def error(self, msg: str):
        if self._last_was_progress and not self.verbose:
             print()
        
        print(f"Error: {msg}")
        self._last_was_progress = False

log = Logger()
