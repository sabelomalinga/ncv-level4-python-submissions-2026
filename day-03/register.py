""" GRAPHICAL LEARNER REGISTER SYSTEM Tkinter GUI with learner table, input fields, search, and action buttons. Features: - Add learner (7-digit student number, name) - Add/update mark (10 to 100) - Search by student number or learner name - Delete selected learner - Sort learners alphabetically - Display all learners - Calculate class average - Save records automatically to learner_register.csv """

import csv
import os
import tkinter as tk
from tkinter import ttk, messagebox

FILE_NAME = "learner_register.csv"


class LearnerRegisterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Learner Register System")
        self.root.geometry("1000x650")
        self.root.minsize(850, 550)
        self.learners = []

        self.configure_style()
        self.create_widgets()
        self.load_records()
        self.refresh_table()

    def configure_style(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure("Title.TLabel", font=("Arial", 20, "bold"))
        style.configure("Heading.TLabel", font=("Arial", 10, "bold"))
        style.configure("Treeview", rowheight=28, font=("Arial", 10))
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"))
        style.configure("Action.TButton", font=("Arial", 10, "bold"), padding=7)

    def create_widgets(self):
        heading = ttk.Label(
            self.root, text="LEARNER REGISTER SYSTEM", style="Title.TLabel"
        )
        heading.pack(pady=(15, 10))

        # Learner details section
        details = ttk.LabelFrame(self.root, text="Learner Details", padding=12)
        details.pack(fill="x", padx=18, pady=8)

        ttk.Label(details, text="Student number (7 digits):").grid(
            row=0, column=0, sticky="w", padx=5, pady=6
        )
        self.number_entry = ttk.Entry(details, width=25)
        self.number_entry.grid(row=0, column=1, padx=5, pady=6, sticky="w")

        ttk.Label(details, text="Learner name:").grid(
            row=0, column=2, sticky="w", padx=5, pady=6
        )
        self.name_entry = ttk.Entry(details, width=30)
        self.name_entry.grid(row=0, column=3, padx=5, pady=6, sticky="w")

        ttk.Label(details, text="Mark (10–100):").grid(
            row=1, column=0, sticky="w", padx=5, pady=6
        )
        self.mark_entry = ttk.Entry(details, width=25)
        self.mark_entry.grid(row=1, column=1, padx=5, pady=6, sticky="w")

        ttk.Label(
            details, text="Select a row to edit, update a mark or delete a learner."
        ).grid(row=1, column=2, columnspan=2, sticky="w", padx=5)

        # Action buttons
        actions = ttk.LabelFrame(self.root, text="Register Actions", padding=10)
        actions.pack(fill="x", padx=18, pady=7)

        buttons = [
            ("Add Learner", self.add_learner),
            ("Update Mark", self.update_mark),
            ("Delete Selected", self.delete_selected),
            ("Clear Fields", self.clear_fields),
            ("Sort A–Z", self.sort_learners),
            ("Show All", self.show_all),
            ("Class Average", self.calculate_average),
        ]

        for index, (label, command) in enumerate(buttons):
            ttk.Button(
                actions, text=label, command=command, style="Action.TButton"
            ).grid(row=0, column=index, padx=4, pady=4, sticky="ew")
            actions.columnconfigure(index, weight=1)

        # Search section
        search_frame = ttk.LabelFrame(self.root, text="Search Learners", padding=10)
        search_frame.pack(fill="x", padx=18, pady=7)

        ttk.Label(search_frame, text="Search by student number or name:").pack(
            side="left", padx=(2, 8)
        )
        self.search_entry = ttk.Entry(search_frame, width=35)
        self.search_entry.pack(side="left", padx=5)
        self.search_entry.bind("<KeyRelease>", self.search_live)

        ttk.Button(
            search_frame, text="Search", command=self.search_learners
        ).pack(side="left", padx=5)
        ttk.Button(
            search_frame, text="Reset Search", command=self.reset_search
        ).pack(side="left", padx=5)

        # Table section
        table_frame = ttk.LabelFrame(self.root, text="Learner Records", padding=10)
        table_frame.pack(fill="both", expand=True, padx=18, pady=8)

        columns = ("number", "name", "mark")
        self.table = ttk.Treeview(
            table_frame, columns=columns, show="headings", selectmode="browse"
        )
        self.table.heading("number", text="STUDENT NUMBER")
        self.table.heading("name", text="LEARNER NAME")
        self.table.heading("mark", text="MARK (%)")

        self.table.column("number", width=180, anchor="center")
        self.table.column("name", width=420, anchor="w")
        self.table.column("mark", width=140, anchor="center")

        vertical_scroll = ttk.Scrollbar(
            table_frame, orient="vertical", command=self.table.yview
        )
        horizontal_scroll = ttk.Scrollbar(
            table_frame, orient="horizontal", command=self.table.xview
        )
        self.table.configure(
            yscrollcommand=vertical_scroll.set,
            xscrollcommand=horizontal_scroll.set
        )

        self.table.grid(row=0, column=0, sticky="nsew")
        vertical_scroll.grid(row=0, column=1, sticky="ns")
        horizontal_scroll.grid(row=1, column=0, sticky="ew")

        table_frame.rowconfigure(0, weight=1)
        table_frame.columnconfigure(0, weight=1)
        self.table.bind("<<TreeviewSelect>>", self.select_record)

        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        ttk.Label(
            self.root, textvariable=self.status_var, relief="sunken", anchor="w"
        ).pack(fill="x", side="bottom")

    def find_learner(self, number):
        for learner in self.learners:
            if learner["number"] == number:
                return learner
        return None

    def add_learner(self):
        number = self.number_entry.get().strip()
        name = self.name_entry.get().strip()
        mark_text = self.mark_entry.get().strip()

        if len(number) != 7 or not number.isdigit():
            messagebox.showerror(
                "Invalid Student Number",
                "The student number must contain exactly 7 digits."
            )
            self.number_entry.focus()
            return

        if self.find_learner(number):
            messagebox.showerror(
                "Duplicate Student Number",
                "A learner with this student number already exists."
            )
            return

        if not name:
            messagebox.showerror("Missing Name", "Please enter the learner's name.")
            self.name_entry.focus()
            return

        mark = None
        if mark_text:
            try:
                mark = float(mark_text)
                if not 10 <= mark <= 100:
                    raise ValueError
            except ValueError:
                messagebox.showerror(
                    "Invalid Mark", "Enter a valid mark between 10 and 100."
                )
                self.mark_entry.focus()
                return

        self.learners.append(
            {"number": number, "name": name, "mark": mark}
        )
        self.save_records()
        self.refresh_table()
        self.clear_fields()
        self.status_var.set(f"Learner {name} added successfully.")
        messagebox.showinfo("Success", "Learner added successfully.")

    def update_mark(self):
        number = self.number_entry.get().strip()
        if not number:
            selected = self.table.selection()
            if selected:
                number = self.table.item(selected[0], "values")[0]

        learner = self.find_learner(number)
        if learner is None:
            messagebox.showwarning(
                "Select Learner", "Select a learner or enter a student number."
            )
            return

        mark_text = self.mark_entry.get().strip()
        try:
            mark = float(mark_text)
            if not 10 <= mark <= 100:
                raise ValueError
        except ValueError:
            messagebox.showerror(
                "Invalid Mark", "Enter a valid mark between 10 and 100."
            )
            self.mark_entry.focus()
            return

        learner["mark"] = mark
        self.save_records()
        self.refresh_table()
        self.status_var.set(f"Mark updated for {learner['name']}.")
        messagebox.showinfo("Success", "Learner mark updated successfully.")

    def delete_selected(self):
        selected = self.table.selection()
        if not selected:
            messagebox.showwarning(
                "No Selection", "Please select a learner in the table first."
            )
            return

        values = self.table.item(selected[0], "values")
        number = values[0]
        learner = self.find_learner(number)

        if learner and messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete {learner['name']}?"
        ):
            self.learners.remove(learner)
            self.save_records()
            self.refresh_table()
            self.clear_fields()
            self.status_var.set(f"Learner {learner['name']} deleted.")

    def select_record(self, _event=None):
        selected = self.table.selection()
        if not selected:
            return

        number, name, mark = self.table.item(selected[0], "values")
        self.number_entry.delete(0, tk.END)
        self.number_entry.insert(0, number)
        self.name_entry.delete(0, tk.END)
        self.name_entry.insert(0, name)
        self.mark_entry.delete(0, tk.END)
        if mark != "Not entered":
            self.mark_entry.insert(0, mark)

    def clear_fields(self):
        for entry in (self.number_entry, self.name_entry, self.mark_entry):
            entry.delete(0, tk.END)
        self.table.selection_remove(self.table.selection())
        self.number_entry.focus()

    def refresh_table(self, records=None):
        if records is None:
            records = self.learners

        for item in self.table.get_children():
            self.table.delete(item)

        for learner in records:
            mark = (
                f"{learner['mark']:.1f}"
                if learner["mark"] is not None
                else "Not entered"
            )
            self.table.insert(
                "", tk.END,
                values=(learner["number"], learner["name"], mark)
            )

        self.status_var.set(
            f"Records displayed: {len(records)} | Total registered: {len(self.learners)}"
        )

    def search_learners(self):
        term = self.search_entry.get().strip().lower()
        if not term:
            self.show_all()
            return

        matches = [
            learner for learner in self.learners
            if term in learner["number"].lower()
            or term in learner["name"].lower()
        ]
        self.refresh_table(matches)
        self.status_var.set(f"Search results: {len(matches)}")

    def search_live(self, _event=None):
        self.search_learners()

    def reset_search(self):
        self.search_entry.delete(0, tk.END)
        self.show_all()

    def show_all(self):
        self.refresh_table(self.learners)

    def sort_learners(self):
        self.learners.sort(key=lambda learner: learner["name"].casefold())
        self.save_records()
        self.refresh_table()
        self.status_var.set("Learners sorted alphabetically by name.")

    def calculate_average(self):
        marks = [
            learner["mark"] for learner in self.learners
            if learner["mark"] is not None
        ]

        if not marks:
            messagebox.showinfo(
                "Class Average", "There are no learner marks to calculate."
            )
            return

        average = sum(marks) / len(marks)
        messagebox.showinfo(
            "Class Average",
            f"Number of marks: {len(marks)}\n"
            f"Class average: {average:.2f}%"
        )

    def save_records(self):
        try:
            with open(FILE_NAME, "w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(
                    file, fieldnames=["number", "name", "mark"]
                )
                writer.writeheader()
                for learner in self.learners:
                    writer.writerow(learner)
        except OSError as error:
            messagebox.showerror(
                "Save Error", f"Could not save learner records.\n{error}"
            )

    def load_records(self):
        if not os.path.exists(FILE_NAME):
            return

        try:
            with open(FILE_NAME, "r", newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    number = row.get("number", "").strip()
                    name = row.get("name", "").strip()
                    mark_text = row.get("mark", "").strip()

                    if len(number) == 7 and number.isdigit() and name:
                        try:
                            mark = float(mark_text) if mark_text else None
                            if mark is not None and not 10 <= mark <= 100:
                                mark = None
                        except ValueError:
                            mark = None

                        if self.find_learner(number) is None:
                            self.learners.append(
                                {"number": number, "name": name, "mark": mark}
                            )
        except (OSError, csv.Error) as error:
            messagebox.showerror(
                "Load Error", f"Could not load learner records.\n{error}"
            )


if __name__ == "__main__":
    window = tk.Tk()
    app = LearnerRegisterApp(window)
    window.mainloop()