from tkinter import Label, Button, Canvas, W, E, FLAT, \
    Frame, Menu, DISABLED, NORMAL, Entry, END, Radiobutton, LabelFrame, GROOVE, StringVar, SOLID, \
    messagebox, Scrollbar, BOTTOM, X, BooleanVar, Text
from front.mapper import ROLES_MAPPER
from front.config import ADDRESS, PORT
import http.client
import json

http_request = http.client.HTTPConnection(
    host=ADDRESS,
    port=PORT
)


def update_frame(frame: Frame):
    if frame.winfo_children():
        if isinstance(frame.winfo_children()[-1], (Canvas, Frame)):
            frame.winfo_children()[-1].destroy()


class Dashboard:
    def __init__(self, master, username, role, token):
        # Frame.__init__(self, master)
        self.preferences_name = StringVar()
        self.contract_type = BooleanVar()
        self.requesting_department = StringVar()
        self.token = token
        self.accesses = ROLES_MAPPER[role]
        self.accesses_mapped = list()
        for bool_value in self.accesses:
            self.accesses_mapped.append(NORMAL if bool_value else DISABLED)
        self.master = master
        self.menu_bar = Menu(self.master)
        self.init_ui(self.menu_bar)
        self.cav = Canvas(master, width=master.winfo_width(), height=master.winfo_height() / 15, bg="white")
        self.cav.create_text(.99 * master.winfo_width(), int(master.winfo_height() / 30),
                             text="Logged as {}".format(username), anchor=E, font="Helvetica 10 bold")
        button1 = Button(self.cav, text="Disconnect", command=self.deconnect,
                         anchor=W, bd=0)
        button1.configure(width=15, background="white",
                          relief=FLAT, height=int(master.winfo_height() / 30))
        button1.pack()
        self.cav.create_window(20, int(master.winfo_height() / 30), anchor=W, window=button1)
        self.cav.pack()
        self.additional_fr = Frame(self.master)
        self.error_response = str()
        self.status_response = str()
        self.priority = StringVar()

    def deconnect(self):
        self.cav.destroy()
        self.menu_bar.destroy()
        self.additional_fr.destroy()
        from front.login import LoginPage
        _ = LoginPage(master=self.master)

    def init_ui(self, menu_bar):
        event_request_menu = Menu(menu_bar)
        event_request_menu.add_command(label="Create", state=self.accesses_mapped[0], command=self.create_event_request)
        event_request_menu.add_command(label="Retrieve & more", state=self.accesses_mapped[1],
                                       command=self.retrieve_event_request_ui)
        menu_bar.add_cascade(menu=event_request_menu, label="Event Creation")

        event_application = Menu(menu_bar)
        event_application.add_command(label="Create", state=self.accesses_mapped[2], command=self.create_application)
        event_application.add_command(label="Retrieve & more", state=self.accesses_mapped[3], command=self.retrieve_application_ui)
        menu_bar.add_cascade(menu=event_application, label="Application")

        event_tasks = Menu(menu_bar)
        event_tasks.add_command(label="Create", state=self.accesses_mapped[4], command=self.task_request)
        event_tasks.add_command(label="Retrieve & more", state=self.accesses_mapped[5],
                                command=self.retrieve_task_ui)
        menu_bar.add_cascade(menu=event_tasks, label="Tasks")

        human_resource_request = Menu(menu_bar)
        human_resource_request.add_command(label="Create", state=self.accesses_mapped[6], command=self.hr_request)
        human_resource_request.add_command(label="Retrieve & more", state=self.accesses_mapped[7], command=self.retrieve_hr_ui)
        menu_bar.add_cascade(menu=human_resource_request, label="HR")

        financial_request = Menu(menu_bar)
        financial_request.add_command(label="Create", state=self.accesses_mapped[8], command=self.fm_request)
        financial_request.add_command(label="Retrieve & more", state=self.accesses_mapped[9], command=self.retrieve_fm_ui)
        menu_bar.add_cascade(menu=financial_request, label="Financial Requests")

        self.master.config(menu=menu_bar)

    def create_event_request(self):
        token = self.token
        update_frame(self.additional_fr)
        sub_frame = Frame(self.additional_fr)
        sub_frame.grid(row=0, column=0)
        label_record_number = Label(sub_frame, text="Record Number (Client)")
        label_client_name = Label(sub_frame, text="Client Name")
        label_event_type = Label(sub_frame, text="Event Type")
        label_from_date = Label(sub_frame, text="From Date")
        label_to_date = Label(sub_frame, text="To Date")
        label_number_attendees = Label(sub_frame, text="Expected number of attendees")
        label_excepted_budget = Label(sub_frame, text="Expected Budget (SEK)")

        entry_number_attendees = Entry(sub_frame)
        entry_expected_budget = Entry(sub_frame)
        preferences_labelframe = LabelFrame(sub_frame, text='Preferences', relief=GROOVE, bd=2)
        preferences_name = self.preferences_name
        entry_to_date = Entry(sub_frame)
        entry_from_date = Entry(sub_frame)
        entry_event_type = Entry(sub_frame)
        entry_client_name = Entry(sub_frame)
        entry_record_number = Entry(sub_frame)
        entry_from_date.insert(END, "yyyy/mm/dd")
        entry_to_date.insert(END, "yyyy/mm/dd")
        button_submit = Button(sub_frame, text="Submit", width=10, height=1)
        label_error = Label(sub_frame, text="", fg="red", font="Helvetica 9 bold")

        Radiobutton(preferences_labelframe, variable=preferences_name, value="decorations",
                    text="Decoration").grid(row=1, column=0, pady=20)
        Radiobutton(preferences_labelframe, variable=preferences_name, value="parties", text="Parties").grid(
            row=2, column=0, pady=10)
        Radiobutton(preferences_labelframe, variable=preferences_name, value="photos_filming",
                    text="Photos/filming").grid(row=3, column=0, pady=10)
        Radiobutton(preferences_labelframe, variable=preferences_name, value="breakfast_launch_dinner",
                    text="Breakfast, launch, dinner").grid(row=1, column=1, pady=20, padx=20)
        Radiobutton(preferences_labelframe, variable=preferences_name, value="drinks",
                    text="Soft/hot drinks").grid(row=2, column=1, pady=10, padx=20)

        label_record_number.grid(row=1, column=0, pady=20)
        entry_record_number.grid(row=1, column=1, padx=10, pady=20)
        label_client_name.grid(row=2, column=0, pady=20)
        entry_client_name.grid(row=2, column=1, padx=10, pady=20)
        label_event_type.grid(row=3, column=0, pady=20)
        entry_event_type.grid(row=3, column=1, padx=10, pady=20)
        label_from_date.grid(row=4, column=0, pady=20)
        entry_from_date.grid(row=4, column=1, pady=20, padx=10)
        label_to_date.grid(row=4, column=4, pady=20)
        entry_to_date.grid(row=4, column=5, pady=20, padx=10)
        label_number_attendees.grid(row=5, column=0, pady=20)
        entry_number_attendees.grid(row=5, column=1, padx=10, pady=20)
        preferences_labelframe.grid(row=6, column=1, pady=20)
        label_excepted_budget.grid(row=7, column=0, pady=20)
        entry_expected_budget.grid(row=7, column=1, pady=20, padx=10)
        button_submit.grid(row=8, column=1, pady=20)
        label_error.grid(row=8, column=2)

        def send_form(*args):
            body = {
                "record_number": entry_record_number.get(),
                "client_name": entry_client_name.get(),
                "event_type": entry_event_type.get(),
                "from_date": entry_from_date.get(),
                "to_date": entry_to_date.get(),
                "expected_number_attendees": entry_number_attendees.get(),
                "preferences": preferences_name.get()
            }
            print(body)
            header = {
                'Authorization': 'Bearer {}'.format(token)
            }
            http_request.request("POST", "/event_creation/", headers=header, body=json.dumps(body))
            response = http_request.getresponse()
            if response.status > 200:
                sub_frame.config(highlightcolor="red", highlightbackground="red", highlightthickness=3,
                                          relief=SOLID, bd=0)
                label_error.config(text="Error click here to get details")
                sub_frame.after(3000, lambda: label_error.config(text=""))
                sub_frame.after(2000, lambda: sub_frame.config(relief=FLAT))
                try:
                    decoded_response = json.loads(response.read().decode())
                    self.error_response = decoded_response["error"]
                except (KeyError, json.decoder.JSONDecodeError):
                    self.status_response = "400 or 500"
                    self.error_response = "No information given by server, information were not properly given"
                label_error.bind("<Button-1>", self.display_error)
            else:
                self.display_validation()

        button_submit.bind("<Button-1>", send_form)
        self.additional_fr.bind("<Return>", send_form)
        self.additional_fr.pack()

    def display_error(self, event):
        messagebox.showerror(title="Error",
                             message="Status : {}, error: {}".format(self.status_response, self.error_response))

    def display_validation(self):
        messagebox.showinfo(title="Success", message="Information received and validated by server")

    def retrieve_event_request(self):
        header = {
            'Authorization': 'Bearer {}'.format(self.token)
        }
        http_request.request("GET", "/review_event_creation/", headers=header)
        response = http_request.getresponse()
        if response.status > 200:
            try:
                decoded_response = json.loads(response.read().decode())
                self.error_response = decoded_response["error"]
            except (KeyError, json.decoder.JSONDecodeError):
                self.status_response = "400 or 500"
                self.error_response = "No information given by server, unknown error"
            self.display_error(None)
            return []
        else:
            decoded_response = json.loads(response.read().decode())
            return decoded_response["events"]

    def retrieve_event_request_ui(self):
        update_frame(self.additional_fr)
        data = self.retrieve_event_request()
        headers = ["event_request_id", "client_name", "event_type", "from_date", "to_date", "preferences", "feedback_fm"]
        canvas = Canvas(self.additional_fr)
        canvas.grid(column=0, row=0)
        for i in range(len(data)):
            for j, head in enumerate(headers):
                width = 15 if j > 0 else 45
                l = Label(canvas, text="{}".format(data[i][head]), width=width, relief=SOLID, bd=2, font="Helevetica 9 bold")
                l.grid(row=i+2, column=j)
        for j, head in enumerate(headers):
            width = 15 if j > 0 else 45
            Label(canvas, text="{}".format(head), width=width, relief=SOLID, bd=2, pady=30, font="Helevetica 9 bold").grid(row=1, column=j)
        Label(canvas, text="Event Request waiting for your approval", font="Helvetica 13 bold",
              underline=True).grid(row=0, column=0)
        self.additional_fr.pack_propagate(0)
        self.additional_fr.pack()

    def hr_request(self):
        token = self.token
        update_frame(self.additional_fr)
        frame_hr = Frame(self.additional_fr)
        frame_hr.grid(row=0, column=0)
        label_year = Label(frame_hr, text="Year(s) (Integer)")
        label_job_title = Label(frame_hr, text="Job title")
        label_job_description = Label(frame_hr, text="Job description")

        button_submit = Button(frame_hr, text="Submit", width=10, height=1)

        requesting_department_labelframe = LabelFrame(frame_hr, text='Requesting Department',
                                                           relief=GROOVE, bd=2)
        contract_type_labelframe = LabelFrame(frame_hr, text='Contract Type', relief=GROOVE, bd=2)
        entry_years = Entry(frame_hr)
        entry_job_title = Entry(frame_hr)
        entry_job_description = Entry(frame_hr)
        entry_job_description.grid(ipady=50, ipadx=35)

        Radiobutton(contract_type_labelframe, variable=self.contract_type, value=True,
                    text="Full Time").grid(row=1, column=0, pady=20)
        Radiobutton(contract_type_labelframe, variable=self.contract_type, value=False, text="Part Time").grid(
            row=1, column=1, pady=10)

        Radiobutton(requesting_department_labelframe, variable=self.requesting_department, value="administration",
                    text="Administration").grid(row=2, column=0, pady=20)
        Radiobutton(requesting_department_labelframe, variable=self.requesting_department, value="services",
                    text="Services").grid(row=2, column=1, pady=20, padx=20)
        Radiobutton(requesting_department_labelframe, variable=self.requesting_department, value="production",
                    text="Production").grid(row=3, column=0, pady=10, padx=20)
        Radiobutton(requesting_department_labelframe, variable=self.requesting_department, value="financial",
                    text="Financial").grid(row=3, column=1, pady=10, padx=20)

        contract_type_labelframe.grid(row=1, column=2, pady=20)
        requesting_department_labelframe.grid(row=2, column=2, pady=20)
        label_year.grid(row=3, column=1, pady=20)
        entry_years.grid(row=3, column=2, pady=20)
        label_job_title.grid(row=4, column=1, pady=20)
        entry_job_title.grid(row=4, column=2, pady=20)
        label_job_description.grid(row=5, column=1, pady=20)
        entry_job_description.grid(row=5, column=2, pady=20)
        button_submit.grid(row=6, column=1, pady=20)
        label_error = Label(frame_hr, text="", fg="red", font="Helvetica 9 bold")
        contract_type = self.contract_type
        requesting_department = self.requesting_department

        def send_form(*args):
            body = {
                "is_full_time": contract_type.get(),
                "request_department": requesting_department.get(),
                "year_experience_min": int(entry_years.get()),
                'job_title': entry_job_title.get(),
                'job_description': entry_job_description.get()
            }
            header = {
                'Authorization': 'Bearer {}'.format(token)
            }
            http_request.request("POST", "/create_staff_request/", headers=header, body=json.dumps(body))
            response = http_request.getresponse()
            if response.status > 200:
                frame_hr.config(highlightcolor="red", highlightbackground="red", highlightthickness=3,
                                          relief=SOLID, bd=0)
                label_error.config(text="Error click here to get details")
                frame_hr.after(3000, lambda: label_error.config(text=""))
                frame_hr.after(2000, lambda:frame_hr.config(relief=FLAT))
                try:
                    decoded_response = json.loads(response.read().decode())
                    self.error_response = decoded_response["error"]
                except (KeyError, json.decoder.JSONDecodeError):
                    self.status_response = "400 or 500"
                    self.error_response = "No information given by server, information were not properly given"
                label_error.bind("<Button-1>", self.display_error)
            else:
                self.display_validation()

        button_submit.bind("<Button-1>", send_form)
        # self.additional_fr.bind("<Return>", self.send_form)
        frame_hr.bind("<Return>", send_form)
        self.additional_fr.pack()

    def fm_request(self):
        token = self.token
        update_frame(self.additional_fr)
        frame_hr = Frame(self.additional_fr)
        frame_hr.grid(row=0, column=0)
        label_project_reference = Label(frame_hr, text="Project Reference")
        label_required_amount = Label(frame_hr, text="Required Amount (SEK)")
        label_reason = Label(frame_hr, text="Reason")

        button_submit = Button(frame_hr, text="Submit", width=10, height=1)

        requesting_department_labelframe = LabelFrame(frame_hr, text='Requesting Department',
                                                      relief=GROOVE, bd=2)
        entry_project_reference = Entry(frame_hr)
        entry_required_amount = Entry(frame_hr)
        entry_reason = Text(frame_hr, height=20, width=10)

        Radiobutton(requesting_department_labelframe, variable=self.requesting_department, value="administration",
                    text="Administration").grid(row=2, column=0, pady=20)
        Radiobutton(requesting_department_labelframe, variable=self.requesting_department, value="services",
                    text="Services").grid(row=2, column=1, pady=20, padx=20)
        Radiobutton(requesting_department_labelframe, variable=self.requesting_department, value="production",
                    text="Production").grid(row=3, column=0, pady=10, padx=20)
        Radiobutton(requesting_department_labelframe, variable=self.requesting_department, value="financial",
                    text="Financial").grid(row=3, column=1, pady=10, padx=20)

        requesting_department_labelframe.grid(row=1, column=2, pady=20)
        label_project_reference.grid(row=3, column=1, pady=20)
        entry_project_reference.grid(row=3, column=2, pady=20)
        label_required_amount.grid(row=4, column=1, pady=20)
        entry_required_amount.grid(row=4, column=2, pady=20)
        label_reason.grid(row=5, column=1, pady=20)
        entry_reason.grid(row=5, column=2, pady=20, ipady=60, ipadx=35)

        button_submit.grid(row=6, column=1, pady=20)
        label_error = Label(frame_hr, text="", fg="red", font="Helvetica 9 bold")
        requesting_department = self.requesting_department

        def send_form(*args):
            body = {
                "request_department": requesting_department.get(),
                "project_reference": entry_project_reference.get(),
                'required_amount': entry_required_amount.get(),
                'reason': entry_reason.get()
            }
            header = {
                'Authorization': 'Bearer {}'.format(token)
            }
            http_request.request("POST", "/create_financial_request/", headers=header, body=json.dumps(body))
            response = http_request.getresponse()
            if response.status > 200:
                frame_hr.config(highlightcolor="red", highlightbackground="red", highlightthickness=3,
                                          relief=SOLID, bd=0)
                label_error.config(text="Error click here to get details")
                frame_hr.after(3000, lambda: label_error.config(text=""))
                frame_hr.after(2000, lambda: frame_hr.config(relief=FLAT))
                try:
                    decoded_response = json.loads(response.read().decode())
                    self.error_response = decoded_response["error"]
                except (KeyError, json.decoder.JSONDecodeError):
                    self.status_response = "400 or 500"
                    self.error_response = "No information given by server, information were not properly given"
                label_error.bind("<Button-1>", self.display_error)
            else:
                self.display_validation()

        button_submit.bind("<Button-1>", send_form)
        # self.additional_fr.bind("<Return>", self.send_form)
        frame_hr.bind("<Return>", send_form)
        self.additional_fr.pack()

    def task_request(self):
        token = self.token
        update_frame(self.additional_fr)
        frame_hr = Frame(self.additional_fr)
        frame_hr.grid(row=0, column=0)
        label_project_reference = Label(frame_hr, text="Project Reference")
        label_assigned_to = Label(frame_hr, text="Assigned To")
        label_description = Label(frame_hr, text="Description")

        button_submit = Button(frame_hr, text="Submit", width=10, height=1)

        requesting_priority = LabelFrame(frame_hr, text='Priority', width=75, height=40,
                                                      relief=GROOVE, bd=2)

        entry_project_reference = Entry(frame_hr)
        entry_assigned_to = Entry(frame_hr)
        entry_description = Entry(frame_hr)

        Radiobutton(requesting_priority, variable=self.priority, value="very_high",
                    text="Very High").grid(row=2, column=0, padx=20)
        Radiobutton(requesting_priority, variable=self.priority, value="high",
                    text="High").grid(row=3, column=0, padx=20)
        Radiobutton(requesting_priority, variable=self.priority, value="medium",
                    text="Medium").grid(row=4, column=0, padx=20)

        label_project_reference.grid(row=5, column=1, pady=20)
        entry_project_reference.grid(row=5, column=2, pady=20)
        label_description.grid(row=6, column=1, pady=20)
        entry_description.grid(row=6, column=2, pady=20)
        label_assigned_to.grid(row=7, column=1, pady=20)
        entry_assigned_to.grid(row=7, column=2, pady=20)
        requesting_priority.grid(row=8, column=1, pady=20, padx=20)

        button_submit.grid(row=9, column=1, pady=20)
        label_error = Label(frame_hr, text="", fg="red", font="Helvetica 9 bold")
        label_error.grid(row=9, column=2, pady=20)

        def send_form(*args):
            body = {
                "project_reference": entry_project_reference.get(),
                'description': entry_description.get(),
                "user_assigned": entry_assigned_to.get(),
                "priority": self.priority.get()
            }
            header = {
                'Authorization': 'Bearer {}'.format(token)
            }
            http_request.request("POST", "/create_task/", headers=header, body=json.dumps(body))
            response = http_request.getresponse()
            if response.status > 200:
                frame_hr.config(highlightcolor="red", highlightbackground="red", highlightthickness=3,
                                relief=SOLID, bd=0)
                label_error.config(text="Error click here to get details")
                frame_hr.after(3000, lambda: label_error.config(text=""))
                frame_hr.after(2000, lambda: frame_hr.config(relief=FLAT))
                try:
                    decoded_response = json.loads(response.read().decode())
                    self.error_response = decoded_response["error"]
                except (KeyError, json.decoder.JSONDecodeError):
                    self.status_response = "400 or 500"
                    self.error_response = "No information given by server, information were not properly given"
                label_error.bind("<Button-1>", self.display_error)
            else:
                self.display_validation()

        button_submit.bind("<Button-1>", send_form)
        # self.additional_fr.bind("<Return>", self.send_form)
        frame_hr.bind("<Return>", send_form)
        self.additional_fr.pack()

    def retrieve_financial_request(self):
        header = {
            'Authorization': 'Bearer {}'.format(self.token)
        }
        http_request.request("GET", "/review_financial_request/", headers=header, body=json.dumps(dict()))
        response = http_request.getresponse()
        if response.status > 200:
            try:
                decoded_response = json.loads(response.read().decode())
                self.error_response = decoded_response["error"]
            except (KeyError, json.decoder.JSONDecodeError):
                self.status_response = "400 or 500"
                self.error_response = "No information given by server, unknown error"
            self.display_error(None)
            return []
        else:
            decoded_response = json.loads(response.read().decode())
            return decoded_response["financial_requests"]

    def retrieve_task_ui(self):
        update_frame(self.additional_fr)
        frame_hr = Frame(self.additional_fr)
        frame_hr.grid(row=0, column=0)
        Label(frame_hr, text="Project reference").grid(row=1, column=1)
        entry_project_reference = Entry(frame_hr)
        entry_project_reference.grid(row=1, column=2)

        def submit_data(*args):
            data = self.retrieve_task_request(entry_project_reference.get())
            headers = ["project_reference", "description", "assign_to_user", "priority", "status"]
            canvas = Canvas(frame_hr)
            canvas.grid(column=0, row=5)
            for i in range(len(data)):
                for j, head in enumerate(headers):
                    width = 15 if j > 0 else 45
                    l = Label(canvas, text="{}".format(data[i][head]), width=width, relief=SOLID, bd=2,
                              font="Helevetica 9 bold")
                    l.grid(row=i + 2, column=j)
            for j, head in enumerate(headers):
                width = 15 if j > 0 else 45
                Label(canvas, text="{}".format(head), width=width, relief=SOLID, bd=2, pady=30,
                      font="Helevetica 9 bold").grid(row=1, column=j)
            Label(canvas, text="Tasks for your project id", font="Helvetica 13 bold",
                  underline=True).grid(row=0, column=0)
        Button(frame_hr, text="Submit", command=submit_data).grid(row=1, column=3)
        frame_hr.pack()
        self.additional_fr.pack()

    def retrieve_task_request(self, project_reference):
        header = {
            'Authorization': 'Bearer {}'.format(self.token)
        }
        body = {
            "project_reference": project_reference
        }
        http_request.request("GET", "/retrieve_task/", headers=header, body=json.dumps(body))
        response = http_request.getresponse()
        if response.status > 200:
            try:
                decoded_response = json.loads(response.read().decode())
                self.error_response = decoded_response["error"]
            except (KeyError, json.decoder.JSONDecodeError):
                self.status_response = "400 or 500"
                self.error_response = "No information given by server, unknown error"
            self.display_error(None)
            return []
        else:
            decoded_response = json.loads(response.read().decode())
            return decoded_response["tasks"]

    def retrieve_fm_ui(self):
        update_frame(self.additional_fr)
        data = self.retrieve_financial_request()
        headers = ["id", "department", "project_reference", "required_amount", "reason", "status"]
        canvas = Canvas(self.additional_fr)
        canvas.grid(column=0, row=0)
        for i in range(len(data)):
            for j, head in enumerate(headers):
                width = 15 if j > 0 else 45
                l = Label(canvas, text="{}".format(data[i][head]), width=width, relief=SOLID, bd=2,
                          font="Helevetica 9 bold")
                l.grid(row=i + 2, column=j)
        for j, head in enumerate(headers):
            width = 15 if j > 0 else 45
            Label(canvas, text="{}".format(head), width=width, relief=SOLID, bd=2, pady=30,
                  font="Helevetica 9 bold").grid(row=1, column=j)
        Label(canvas, text="Financial Requests", font="Helvetica 13 bold",
              underline=True).grid(row=0, column=0)
        self.additional_fr.pack_propagate(0)
        self.additional_fr.pack()

    def retrieve_hr_request(self):
        header = {
            'Authorization': 'Bearer {}'.format(self.token)
        }
        http_request.request('GET', "/review_staff_request/", headers=header, body=json.dumps(dict()))
        response = http_request.getresponse()
        if response.status > 200:
            try:
                decoded_response = json.loads(response.read().decode())
                self.error_response = decoded_response["error"]
            except (KeyError, json.decoder.JSONDecodeError):
                self.status_response = "400 or 500"
                self.error_response = "No information given by server, unknown error"
            self.display_error(None)
            return []
        else:
            decoded_response = json.loads(response.read().decode())
            return decoded_response["hr"]

    def retrieve_hr_ui(self):
        update_frame(self.additional_fr)
        data = self.retrieve_hr_request()
        headers = ["staff_request_id", "is_full_time", "department", "year_min", "job_title", "job_description", "status"]
        canvas = Canvas(self.additional_fr)
        canvas.grid(column=0, row=0)
        for i in range(len(data)):
            for j, head in enumerate(headers):
                width = 15 if j > 0 else 45
                l = Label(canvas, text="{}".format(data[i][head]), width=width, relief=SOLID, bd=2,
                          font="Helevetica 9 bold")
                l.grid(row=i + 2, column=j)
        for j, head in enumerate(headers):
            width = 15 if j > 0 else 45
            Label(canvas, text="{}".format(head), width=width, relief=SOLID, bd=2, pady=30,
                  font="Helevetica 9 bold").grid(row=1, column=j)
        Label(canvas, text="HR Requests", font="Helvetica 13 bold",
              underline=True).grid(row=0, column=0)
        self.additional_fr.pack_propagate(0)
        self.additional_fr.pack()

    def create_application(self):
        token = self.token
        update_frame(self.additional_fr)
        sub_frame = Frame(self.additional_fr)
        sub_frame.grid(row=0, column=0)
        label_record_number = Label(sub_frame, text="Record Number (Client)")
        label_client_name = Label(sub_frame, text="Client Name")
        label_event_type = Label(sub_frame, text="Event Type")
        label_description = Label(sub_frame, text='Description')
        label_number_attendees = Label(sub_frame, text="Expected Number")
        label_excepted_budget = Label(sub_frame, text="Planned Budget (SEK)")
        label_from_date = Label(sub_frame, text="From")
        label_to_date = Label(sub_frame, text="To")
        label_decorations = Label(sub_frame, text="Decorations")
        label_food_drinks = Label(sub_frame, text="Food/Drinks")
        label_filming_photos = Label(sub_frame, text="Filming/Photos")
        label_music = Label(sub_frame, text="Music")
        label_posters_artwork = Label(sub_frame, text="Posters/Art Work")
        label_computer_related_issues = Label(sub_frame, text="Computer-Related Issues")
        label_other_needs = Label(sub_frame, text="Other Needs")

        entry_number_attendees = Entry(sub_frame)
        entry_expected_budget = Entry(sub_frame)
        entry_to_date = Entry(sub_frame)
        entry_from_date = Entry(sub_frame)
        entry_event_type = Entry(sub_frame)
        entry_client_name = Entry(sub_frame)
        entry_record_number = Entry(sub_frame)
        entry_description = Entry(sub_frame)
        entry_from_date.insert(END, "yyyy/mm/dd")
        entry_to_date.insert(END, "yyyy/mm/dd")
        text_decorations = Text(sub_frame, width=40, height=5)
        text_food_drinks = Text(sub_frame, width=40, height=5)
        text_filming_photos = Text(sub_frame, width=40, height=5)
        text_music = Text(sub_frame, width=40, height=5)
        text_poster_art_work = Text(sub_frame, width=40, height=5)
        text_computer = Text(sub_frame, width=40, height=5)
        text_other_needs = Text(sub_frame, width=80, height=2)

        button_submit = Button(sub_frame, text="Submit", width=10, height=1)
        label_error = Label(sub_frame, text="", fg="red", font="Helvetica 9 bold")

        label_record_number.grid(row=1, column=0, pady=20, sticky='nsew')
        entry_record_number.grid(row=1, column=1, pady=20, sticky='nsew')
        label_client_name.grid(row=2, column=0)
        entry_client_name.grid(row=2, column=1)
        label_event_type.grid(row=3, column=0)
        entry_event_type.grid(row=3, column=1)
        label_description.grid(row=4, column=0)
        entry_description.grid(row=4, column=1)
        label_from_date.grid(row=5, column=0)
        entry_from_date.grid(row=5, column=1)
        label_to_date.grid(row=5, column=2)
        entry_to_date.grid(row=5, column=3)
        label_number_attendees.grid(row=2, column=2)
        entry_number_attendees.grid(row=2, column=3)
        label_excepted_budget.grid(row=3, column=2)
        entry_expected_budget.grid(row=3, column=3)

        label_decorations.grid(row=6, column=0, pady=20)
        text_decorations.grid(row=6, column=1, pady=20)
        label_food_drinks.grid(row=6, column=2, pady=20)
        text_food_drinks.grid(row=6, column=3, pady=20)

        label_filming_photos.grid(row=7, column=0, pady=20)
        text_filming_photos.grid(row=7, column=1, pady=20)
        label_music.grid(row=7, column=2, pady=20)
        text_music.grid(row=7, column=3, pady=20)

        label_posters_artwork.grid(row=8, column=0, pady=20)
        text_poster_art_work.grid(row=8, column=1, pady=20)
        label_computer_related_issues.grid(row=8, column=2, pady=20)
        text_computer.grid(row=8, column=3, pady=20)

        label_other_needs.grid(row=9, column=0, pady=20)
        text_other_needs.grid(row=9, column=0, pady=20, columnspan=4)

        button_submit.grid(row=11, column=1, pady=20)
        label_error.grid(row=10, column=2)

        def send_form(*args):
            body = {
                "record_number": entry_record_number.get(),
                'client_name': entry_client_name.get(),
                "event_type": entry_event_type.get(),
                "description": entry_description.get(),
                "from_date": entry_from_date.get(),
                "to_date": entry_to_date.get(),
                "expected_number_attendees": entry_number_attendees.get(),
                "planned_budget": entry_expected_budget.get(),
                "decorations": text_decorations.get("1.0",END),
                "food_drinks": text_food_drinks.get("1.0",END),
                "filming_photos": text_filming_photos.get("1.0",END),
                "music": text_music.get("1.0",END),
                "posters_art_work": text_poster_art_work.get("1.0",END),
                "computer_related_issues": text_computer.get("1.0",END),
                "other_needs": text_other_needs.get("1.0",END)
            }
            header = {
                'Authorization': 'Bearer {}'.format(token)
            }
            http_request.request("POST", "/event_application_creation", headers=header, body=json.dumps(body))
            response = http_request.getresponse()
            if response.status > 200:
                sub_frame.config(highlightcolor="red", highlightbackground="red", highlightthickness=3,
                                relief=SOLID, bd=0)
                label_error.config(text="Error click here to get details")
                sub_frame.after(3000, lambda: label_error.config(text=""))
                sub_frame.after(2000, lambda: sub_frame.config(relief=FLAT))
                try:
                    decoded_response = json.loads(response.read().decode())
                    self.error_response = decoded_response["error"]
                except (KeyError, json.decoder.JSONDecodeError):
                    self.status_response = "400 or 500"
                    self.error_response = "No information given by server, information were not properly given"
                label_error.bind("<Button-1>", self.display_error)
            else:
                self.display_validation()

        button_submit.bind("<Button-1>", send_form)
            # self.additional_fr.bind("<Return>", self.send_form)
        sub_frame.bind("<Return>", send_form)
        self.additional_fr.pack()

    def retrieve_application_ui(self):
        update_frame(self.additional_fr)
        data = self.retrieve_application_request()
        headers = ["project_reference", "client_name", "event_type", "description", "from_date", "to_date", "number_attendees"]
        canvas = Canvas(self.additional_fr)
        canvas.grid(column=0, row=0)
        for i in range(len(data)):
            for j, head in enumerate(headers):
                width = 15 if j > 0 else 45
                # if head == "details":
                #     text = str()
                #     for (key,value) in data[i]["details"].items():
                #         if len(value)>1:
                #             text += "{}: {}\n".format(key, value)
                #     l = Label(canvas, text=text, width=width, relief=SOLID, bd=2, font="Helevetica 9 bold")
                # else:
                l = Label(canvas, text="{}".format(data[i][head]), width=width, relief=SOLID, bd=2,
                      font="Helevetica 9 bold")
                l.grid(row=i + 2, column=j)
        for j, head in enumerate(headers):
            width = 15 if j > 0 else 45
            Label(canvas, text="{}".format(head), width=width, relief=SOLID, bd=2, pady=30,
                  font="Helevetica 9 bold").grid(row=1, column=j)
        Label(canvas, text="Applications", font="Helvetica 13 bold",
              underline=True).grid(row=0, column=0)
        self.additional_fr.pack_propagate(0)
        self.additional_fr.pack()

    def retrieve_application_request(self):
        header = {
            'Authorization': 'Bearer {}'.format(self.token)
        }
        http_request.request("GET", "/event_application_retrieve/", headers=header, body=json.dumps(dict()))
        response = http_request.getresponse()
        if response.status > 200:
            try:
                decoded_response = json.loads(response.read().decode())
                self.error_response = decoded_response["error"]
            except (KeyError, json.decoder.JSONDecodeError):
                self.status_response = "400 or 500"
                self.error_response = "No information given by server, unknown error"
            self.display_error(None)
            return []
        else:
            decoded_response = json.loads(response.read().decode())
            return decoded_response["applications"]


