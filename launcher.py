from PyQt6.QtWidgets import QApplication
import sys
import traceback

print("[1] importing ui")

from ui import JarvisUI

print("[2] ui imported")

app = QApplication(sys.argv)

print("[3] QApplication created")

try:
    print("[4] creating JarvisUI")
    jarvis = JarvisUI("face.png")
    print("[5] JarvisUI created")

    print("[6] showing window")
    jarvis._win.show()

    print("[7] entering event loop")
    sys.exit(app.exec())

except Exception:
    traceback.print_exc()
