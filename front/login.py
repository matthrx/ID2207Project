from tkinter import Button, Label, CENTER, Entry, Frame, StringVar, NE
from cachetools import TTLCache
from front.config import ADDRESS, PORT
import http.client
import json

import time


http_request = http.client.HTTPConnection(
            host=ADDRESS,
            port=PORT

        )


class LoginPage:
    def __init__(self, master):
        fr = Frame(master, width=400, height=800)
        Label(fr, text="Please enter login details").pack()
        Label(fr, text="").pack()
        Label(fr, text="Username").pack()
        self.username_login_entry = Entry(fr, textvariable="username")
        self.username_login_entry.pack()
        Label(fr, text="").pack()
        Label(fr, text="Password").pack()
        self.password__login_entry = Entry(fr, textvariable="password", show='*')
        self.password__login_entry.pack()
        Label(fr, text="").pack()
        self.content_error = StringVar()
        self.error_label = Label(fr, textvariable=self.content_error, fg="red", font=("Helvetica", 9))
        self.error_label.pack()

        def validate_form(event):
            username = self.username_login_entry.get()
            password = self.password__login_entry.get()
            if username != str() and password != str():
                request_status, response = send_authenticate_request(username, password)
                if request_status > 400:
                    self.content_error.set("Credentials error")
                    master.after(3000, lambda: self.content_error.set(""))
                    # self.error_label.configure(text="Credentials error")
                else:
                    fr.pack_forget()
                    fr.destroy()
                    from front.dashboard import Dashboard
                    _ = Dashboard(master, username, response["role"], response["token"])

        button = Button(fr, text="Login", width=10, height=1, )
        button.pack()
        button.bind("<Button-1>", validate_form)
        fr.place(y=1, x=.5, anchor=NE)
        master.bind("<Return>", validate_form)
        fr.pack(fill=None, expand=True)


def send_authenticate_request(username, password):
    body = {
        "username": username,
        "password": password
    }
    body_json = json.dumps(body)
    http_request.request('GET', '/authenticate/', body=body_json)
    response = http_request.getresponse()
    decoded_response = json.loads(response.read().decode())
    return response.status, decoded_response

