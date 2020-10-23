from tkinter import Tk
from front.server_init import ServerInit

if __name__ == '__main__':
    root = Tk()
    root.title("SEC Interface")
    root.geometry("1200x900")
    Test_server = ServerInit(root)
    root.mainloop()

