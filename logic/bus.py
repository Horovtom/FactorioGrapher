import os

from logic import Resource


class Bus:
    def __init__(self, file, graph):
        self.file = file
        self.graph = graph
        self.resources_on_bus = []
        self.load_data()

    def load_data(self):
        with open(self.file, "r") as f:
            for line in f.readlines():
                if line not in self.resources_on_bus:
                    self.resources_on_bus.append(self.graph.get_resource_from_name(line))

    def is_on_bus(self, resource: Resource):
        return resource in self.resources_on_bus

    def add_all(self, list):
        for resource in self.resources_on_bus:
            if resource not in list:
                list.append(resource.converted_name)
        return list

    def add_to_bus(self, resource):
        if resource in self.resources_on_bus:
            return
        self.resources_on_bus.append(resource)

    def save(self):
        with open(self.file, "w") as f:
            f.write("\n".join([i.human_name for i in self.resources_on_bus]))


