# ##################
# ### Exceptions ###
# ##################

#  - `BoxesTUI_EA_ERROR`: "Everything is on fire, for the love of god: EVERYTHING is broken!"
#  - `BoxesTUI_LibraryUsageError`: A simple error caused by not reading the docs (or the docs being like 5 versions behind)
#  - `BoxesTUI_WindowResizeError`: An error indecating a problem after/while resizing the terminal-emulator window
#  - `BoxesTUI_RemindMeToAddThisCapabilityError`: remind L7 to add the missing feature, that caused this exception to be thrown

class BoxesTUI_EA_ERROR(Exception):
    pass

class BoxesTUI_LibraryUsageError(Exception):
    pass

class BoxesTUI_WindowResizeError(Exception):
    pass

class BoxesTUI_RemindMeToAddThisCapabilityError(Exception):
    pass
