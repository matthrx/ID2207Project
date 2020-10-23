from tkinter import Label, Button, Canvas, W, E, FLAT, \
    Frame, Menu, DISABLED, NORMAL, Entry, END, Radiobutton, LabelFrame, GROOVE, StringVar, SOLID, \
    messagebox, Scrollbar, BOTTOM, X, BooleanVar
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
        button1 = Button(self.cav, text="Deconnect", command=self.deconnect,
                         anchor=W, padx=10, bd=0)
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
        event_application.add_command(label="Create", state=self.accesses_mapped[2])
        event_application.add_command(label="Retrieve & more", state=self.accesses_mapped[3])
        menu_bar.add_cascade(menu=event_application, label="Application")

        event_tasks = Menu(menu_bar)
        event_tasks.add_command(label="Create", state=self.accesses_mapped[4], command=self.task_request)
        event_tasks.add_command(label="Retrieve & more", state=self.accesses_mapped[5])
        menu_bar.add_cascade(menu=event_tasks, label="Tasks")

        human_resource_request = Menu(menu_bar)
        human_resource_request.add_command(label="Create", state=self.accesses_mapped[6], command=self.hr_request)
        human_resource_request.add_command(label="Retrieve & more", state=self.accesses_mapped[7])
        menu_bar.add_cascade(menu=human_resource_request, label="HR")

        financial_request = Menu(menu_bar)
        financial_request.add_command(label="Create", state=self.accesses_mapped[8], command=self.fm_request)
        financial_request.add_command(label="Retrieve & more", state=self.accesses_mapped[9])
        menu_bar.add_cascade(menu=financial_request, label="Financial Requests")

        self.master.config(menu=menu_bar)

    def create_event_request(self):
        token = self.token
        update_frame(self.additional_fr)
        sub_frame = Frame(self.additional_fr)
        sub_frame.grid(row=0, column=0)
        label_record_number = Label(sub_frame, text="Record Number")
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
        messagebox.showinfo(title="Success", message="Information received and validation by server")

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
            print(decoded_response)
            return decoded_response["events"]

    def retrieve_event_request_ui(self):
        update_frame(self.additional_fr)
        data = self.retrieve_event_request()
        headers = ["record_number", "client_name", "event_type", "from_date", "to_date", "preferences", "feedback_fm"]
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
        label_required_amount = Label(frame_hr, text="Required Amount")
        label_reason = Label(frame_hr, text="Reason")

        button_submit = Button(frame_hr, text="Submit", width=10, height=1)

        requesting_department_labelframe = LabelFrame(frame_hr, text='Requesting Department',
                                                      relief=GROOVE, bd=2)
        entry_project_reference = Entry(frame_hr)
        entry_required_amount = Entry(frame_hr)
        entry_reason = Entry(frame_hr)

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
        entry_reason.grid(row=5, column=2, pady=20)

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

        requesting_priority = LabelFrame(frame_hr, text='Priority',
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
        requesting_priority.grid(row=8, column=1, pady=20)

        button_submit.grid(row=9, column=1, pady=20)
        label_error = Label(frame_hr, text="", fg="red", font="Helvetica 9 bold")

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



