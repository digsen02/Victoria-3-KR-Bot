import inspect
import os

def get_current_file_and_line():
    frame = inspect.currentframe()
    filename = os.path.basename(frame.f_back.f_code.co_filename)
    line_number = frame.f_back.f_lineno

    print(f"File: {filename}, Line: {line_number}")