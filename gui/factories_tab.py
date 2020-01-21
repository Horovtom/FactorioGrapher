import tkinter
from tkinter import ttk

from logic import Graph


class FactoriesTab:
    def __init__(self, parent, graph: Graph):
        self.parent = parent
        self.graph: Graph = graph
        self.master = ttk.Frame(self.parent)
        # Add to parent
        self.parent.add(self.master, text="Factories")

        ttk.Label(self.master, text="Factory name", padding=(3, 3, 10, 10)).grid(row=0, column=0)
        self.name_entry_var = tkinter.StringVar(self.master)
        self.name_entry = tkinter.Entry(self.master, textvariable=self.name_entry_var)
        self.name_entry.grid(row=0, column=1)
        self.name_entry.bind("<FocusOut>", lambda a: self.on_name_changed())
        self.invalid_label_var = tkinter.StringVar(self.master)
        self.invalid_label = ttk.Label(self.master, textvariable=self.invalid_label_var).grid(row=1, column=0,
                                                                                              columnspan=2)

        ttk.Label(self.master, text="Factory speed", padding=(3, 3, 10, 10)).grid(row=2, column=0)

        self.speed_entry_var = tkinter.StringVar(self.master)
        self.speed_entry = tkinter.Entry(self.master, textvariable=self.speed_entry_var)
        self.speed_entry.bind("<FocusOut>", lambda a: self.on_speed_changed())
        self.speed_entry.grid(row=2, column=1)

        self.invalid_speed_label_var = tkinter.StringVar(self.master)
        ttk.Label(self.master, textvariable=self.invalid_speed_label_var).grid(row=3, column=0, columnspan=2)

        self.save_button = ttk.Button(self.master, text="Save", command=self.save_click)
        self.save_button.grid(row=4, column=0, columnspan=2)

    def on_speed_changed(self):
        new_name = self.speed_entry_var.get()
        if new_name.strip() == "":
            return

        try:
            num = float(new_name)
            self.invalid_speed_label_var.set("")
            self.speed_entry.config(bg="white")
            return num
        except ValueError:
            self.invalid_speed_label_var.set("Speed has to be a number")
            self.speed_entry.config(bg="red")
            return None

    def on_name_changed(self):
        new_name = self.name_entry_var.get()
        if new_name.strip() == "":
            return

        if new_name in self.graph.factories:
            self.name_entry.config(bg="red")
            self.invalid_label_var.set("Factory name already taken")
            return None
        else:
            self.name_entry.config(bg="white")
            self.invalid_label_var.set("")
            return new_name

    def save_click(self):
        # TODO

        # Check whether the inputs are valid
        name = self.on_name_changed()
        speed = self.on_speed_changed()
        if name is None or speed is None:
            return

        self.graph.add_factory(name, speed)
