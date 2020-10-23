from tkinter import Label, Canvas, TOP
from front.config import ADDRESS, PORT
import http.client
from front.login import LoginPage

import time


http_request = http.client.HTTPConnection(
            host=ADDRESS,
            port=PORT
        )


class ServerInit:
    def __init__(self, master):
        cav = Canvas(master, width=400, height=50)
        cav.pack_propagate(0)
        self.lab = Label(master=cav, text="Test connection server ...", font='Helvetica 12 bold', anchor="center", pady=20)
        self.lab.pack()
        cav.pack()
        status = server_state()
        if status > 200:
            self.lab.configure(text="Test connection server ... FAILED", fg="red")
            master.after(5000, lambda: cav.destroy())
            master.destroy()

        else:
            master.after(1000, self.lab.configure(text="Test connection server ... SUCCESS", fg="green"))
            master.after(1500, lambda: cav.destroy())
            master.after(1750, lambda: LoginPage(master))



def server_state():
    try:
        http_request.request("GET", "/health/")
        response = http_request.getresponse()
        return response.status
    except (ConnectionError, ConnectionAbortedError, ConnectionRefusedError):
        return 500
