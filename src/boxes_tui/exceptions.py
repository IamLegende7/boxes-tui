# ## Exceptions

#  - `LibraryUsageError`: A simple error caused by not reading the docs (or the docs being like 5 versions behind)
#  - `WindowResizeError`: An error indecating a problem after/while resizing the terminal-emulator window

class LibraryUsageError(Exception):
    pass

class WindowResizeError(Exception):
    pass

