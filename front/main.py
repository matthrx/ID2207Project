from tkinter import Tk
from front.server_init import ServerInit

if __name__ == '__main__':
    root = Tk()
    root.title("SEP Interface")
    root.geometry("1300x900")
    Test_server = ServerInit(root)
    root.mainloop()

