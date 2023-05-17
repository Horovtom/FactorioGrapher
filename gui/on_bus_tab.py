import tkinter
from tkinter import ttk


class OnBusTab:
    def __init__(self, parent, graph, bus):
        self.parent = parent
        self.graph = graph
        self.bus = bus
        self.master = ttk.Frame(self.parent)
        # Add to parent
        self.parent.add(self.master, text="Resources On Bus")

        ttk.Label(self.master, text="Resource:").grid(row=0, column=0)
        self.cmbx_filter_resource = ttk.Combobox(self.master, values=self.graph.get_resources_list())
        self.cmbx_filter_resource.grid(row=0, column=1)

        ttk.Button(self.master, text="Add to bus", command=self.add_pressed).grid(row=1, column=0, columnspan=2)

        self.txt_bus_items = tkinter.Listbox(self.master)
        self.txt_bus_items.grid(row=2, column=0)

        for bus_item in self.bus.resources_on_bus:
            self.txt_bus_items.insert(tkinter.END, bus_item.human_name)

    def add_pressed(self):
        resource = self.graph.get_resource_from_name(self.cmbx_filter_resource.get())
        self.bus.add_to_bus(resource)
        self.bus.save()
        self.reload()

    def reload(self):
        self.txt_bus_items.delete(0, tkinter.END)
        for bus_item in self.bus.resources_on_bus:
            self.txt_bus_items.insert(tkinter.END, bus_item.human_name)
