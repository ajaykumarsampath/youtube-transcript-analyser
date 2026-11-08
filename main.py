import datetime
from datetime import datetime
import os

if __name__ == "__main__":
    cwd = os.getcwd()
    now = datetime.now()
    print("Main function called")
    print("Current time:", now)
    print("Current working directory:", cwd)
