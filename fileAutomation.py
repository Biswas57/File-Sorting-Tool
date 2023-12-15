
from os.path import splitext, exists, join
from shutil import move
from time import sleep
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from os import rename, scandir 

# Paths
SOURCE_DIR = "/Users/biswas.simk/Downloads"
DEST_DIR_SFX = "/Users/biswas.simk/Downloads/Sounds"
DEST_DIR_MUSIC = "/Users/biswas.simk/Downloads/Sounds/Music"
DEST_DIR_VIDEO = "/Users/biswas.simk/Downloads/Media/Videos"
DEST_DIR_IMAGE = "/Users/biswas.simk/Downloads/Media/Images"
DEST_DIR_DOCUMENTS = "/Users/biswas.simk/Downloads/Documents"
DEST_DIR_CODE = "/Users/biswas.simk/Downloads/Documents/Code"

# File extensions
IMAGE_EXT = [".jpg", ".jpeg", ".jpe", ".jif", ".jfif", ".jfi", ".png", ".gif", ".webp", ".tiff", ".tif", ".psd", ".raw", ".arw", ".cr2", ".nrw",
                    ".k25", ".bmp", ".dib", ".heif", ".heic", ".ind", ".indd", ".indt", ".jp2", ".j2k", ".jpf", ".jpf", ".jpx", ".jpm", ".mj2", 
                    ".svg", ".svgz", ".ai", ".eps", ".ico"]
VIDEO_EXT = [".webm", ".mpg", ".mp2", ".mpeg", ".mpe", ".mpv", ".ogg",
                    ".mp4", ".mp4v", ".m4v", ".avi", ".wmv", ".mov", ".qt", ".flv", ".swf", ".avchd"]
AUDIO_EXT = [".m4a", ".flac", "mp3", ".wav", ".wma", ".aac"]
DOCUMENT_EXT = [".doc", ".docx", ".odt", ".pdf", ".xls", ".xlsx", ".ppt", ".pptx", ".csv"]
CODE_EXT = [".c", ".cpp", ".py", ".java", ".js", ".html", ".css", ".php", ".rb", ".go", ".swift", ".kt", ".ts", ".json", ".xml", ".yml", 
                    ".yaml", ".md", ".txt", ".out", ".sh", ".bat", ".ps1", ".psm1", ".psd1", ".ps1xml", ".psc1", ".pssc", ".cdxml", ".xaml", 
                    ".xsl", ".xsd", ".s"]

def make_unique(dest, name):
    filename, extension = splitext(name)
    counter = 1
    while exists(join(dest, f"{filename}({counter}){extension}")):
        counter += 1
    return f"{filename}({counter}){extension}" if counter > 1 else name

def move_file(dest, entry, name):
    if exists(join(dest, name)):
        unique_name = make_unique(dest, name)
        rename(entry, join(dest, unique_name))
    else:
        move(entry, join(dest, name))

class fileMover(FileSystemEventHandler):
    def on_modified(self, event):
        if not event.is_directory:
            return
        with scandir(SOURCE_DIR) as entries:
            for entry in entries:
                if entry.is_file(): 
                    name = entry.name
                    self.check_audio_files(entry, name)
                    self.check_video_files(entry, name)
                    self.check_image_files(entry, name)
                    self.check_document_files(entry, name)
                    self.check_code_files(entry, name)

    def check_audio_files(self, entry, name):
        for audio_extension in AUDIO_EXT:
            if name.lower().endswith(audio_extension):
                dest = DEST_DIR_SFX if entry.stat().st_size < 10_000 or "SFX" in name else DEST_DIR_MUSIC
                move_file(dest, entry.path, name)
                logging.info(f"Moved audio file: {name}")

    def check_video_files(self, entry, name):
        for video_extension in VIDEO_EXT:
            if name.lower().endswith(video_extension):
                move_file(DEST_DIR_VIDEO, entry.path, name)
                logging.info(f"Moved video file: {name}")

    def check_image_files(self, entry, name):
        for image_extension in IMAGE_EXT:
            if name.lower().endswith(image_extension):
                move_file(DEST_DIR_IMAGE, entry.path, name)
                logging.info(f"Moved image file: {name}")

    def check_document_files(self, entry, name):
        for document_extension in DOCUMENT_EXT:
            if name.lower().endswith(document_extension):
                move_file(DEST_DIR_DOCUMENTS, entry.path, name)
                logging.info(f"Moved document file: {name}")
    
    def check_code_files(self, entry, name):
        for code_extension in CODE_EXT:
            if name.lower().endswith(code_extension):
                move_file(DEST_DIR_CODE, entry.path, name)
                logging.info(f"Moved code file: {name}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    event_handler = fileMover()
    observer = Observer()
    observer.schedule(event_handler, SOURCE_DIR, recursive=True)
    observer.start()
    try:
        while True:
            sleep(10)
    except KeyboardInterrupt:
        observer.stop()
        observer.join()
