import time
import sys

# ANSI escape codes for colors
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
RESET = "\033[0m"

# Spinner characters & colors
SPINNER = ["|", "/", "-", "\\"]
COLORS = [RED, YELLOW, GREEN, BLUE, MAGENTA, CYAN]

def colorful_spinner(duration=5):
    """Displays a cool color-changing spinner for the given duration."""
    start_time = time.time()
    
    while time.time() - start_time < duration:
        for i in range(len(SPINNER)):
            color = COLORS[i % len(COLORS)]  # Cycle colors
            char = SPINNER[i]  # Cycle spinner characters
            sys.stdout.write(f"\r{color}✨ Waiting for messages {char} {RESET}")  
            sys.stdout.flush()
            time.sleep(0.2)
    
    sys.stdout.write("\r" + " " * 30 + "\r")
    sys.stdout.flush()

def print_success(message):
    """Prints a success message in green."""
    print(f"\n{GREEN}✅ {message}{RESET}")

def print_error(message):
    """Prints an error message in red."""
    print(f"\n{RED}❌ {message}{RESET}")

def print_info(message):
    """Prints an info message in blue."""
    print(f"\n{BLUE}ℹ️  {message}{RESET}")

def print_kawaii_smiling_face():
    """Prints a super cute, otaku-style smiling face in ASCII art."""
    kawaii_face = """
   (\ ^_^ /)
    (  ︶︶  ) 
    ( っ ｡◕‿◕｡)っ
    """
    print(kawaii_face)