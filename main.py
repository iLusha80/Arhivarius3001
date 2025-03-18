import tkinter as tk
from iqt.ui import JSONAppUI

def main():
    root = tk.Tk()
    app = JSONAppUI(root)
    root.mainloop()

if __name__ == '__main__':
    main()
