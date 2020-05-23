## UNUSED, COULD BE DEVELOPED FURTHER IF YOU WANTED A PROGRAM THAT LISTENS WHEN TO RUN WOW.PY

import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        print("Got it!")
event_handler = MyHandler()
observer = Observer()
observer.schedule(event_handler, path='Z:/peleej/World of Warcraft tbc/WTF/Account/LADEOWNAA/SavedVariables/aux-addon.lua', recursive=False)
observer.start()
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()
observer.join()