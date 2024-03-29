import json

from logic.Recipe import Recipe
from logic.Resource import Resource
from logic.dot_wrapper import DotWrapper
from logic.helpers import warning, convert_name, info


class Graph:
    def __init__(self, recipes: str, factories: str):
        self.recipes_filename = recipes
        self.factories_filename = factories
        self.recipes_json: dict = {}
        self.factories: dict = {}
        self.resources: dict = {}
        self.resources_name_map: dict = {}
        self.recipes: dict = {}
        self.reload_factories()
        self.reload_recipes()
        self.construct()

    def reload_factories(self):
        with open(self.factories_filename, 'r') as f:
            s = json.load(f)

        self.factories = s

    def reload_recipes(self):
        with open(self.recipes_filename, 'r') as f:
            s = json.load(f)

        self.recipes_json = s

    def overwrite_factories(self):
        with open(self.factories_filename, 'w') as f:
            json.dump(self.factories, f)
            info("Write into {} successful".format(self.factories_filename))

    def overwrite_recipes(self):
        # TODO: Make sure we have added the recipe to the JSON variable!
        with open(self.recipes_filename, 'w') as f:
            json.dump(self.recipes_json, f)
            info("Write into {} succesful".format(self.recipes_filename))

    def check_integrity(self):
        # TODO: Check if there are no two recipes that have the same inputs/outputs/speed.
        pass

    def get_resource_from_name(self, resource_human_name: str) -> Resource:
        """
        Returns an instance of Resource object for the specified human name. If this Resource was not registered yet, it
        creates a new instance and adds it to the resources list automatically
        :return: Resource object
        """

        resource_converted_name = convert_name(resource_human_name)
        if resource_converted_name not in self.resources:
            # Add a new one to the list
            self.resources[resource_converted_name] = Resource(resource_human_name, resource_converted_name)
            self.resources_name_map[resource_human_name] = resource_converted_name

        return self.resources[resource_converted_name]

    def construct(self):
        def add_resources_to_recipe(r_dict: dict, r_obj: Recipe, do_input: bool):
            io = "inputs" if do_input else "outputs"
            for r in r_dict[io]:
                resource = self.get_resource_from_name(r["resource"])
                amount = float(r["amount"])
                if do_input:
                    r_obj.add_input_resource(resource, amount)
                else:
                    r_obj.add_output_resource(resource, amount)

        for recipe_name in self.recipes_json.keys():
            recipe_dict = self.recipes_json[recipe_name]

            recipe_obj = Recipe("r_" + recipe_name, recipe_dict["time"], recipe_dict["category"])

            add_resources_to_recipe(recipe_dict, recipe_obj, do_input=True)
            add_resources_to_recipe(recipe_dict, recipe_obj, do_input=False)

            self.recipes[recipe_name] = recipe_obj

    def get_resources_list(self):
        res = list(self.resources_name_map.keys())
        res.sort()
        return res

    def get_dot(self, compress_water=True):
        """
        Returns dot object with the whole graph
        """

        dot = DotWrapper(comment="Recipes graph")
        for resource in self.resources.values():
            resource.add_to_dot(dot, compress_water)
        for recipe in self.recipes.values():
            recipe.add_to_dot(dot, compress_water)
        return dot

    def get_dot_with_filter(self, resource_human: str, depth: int, direction_str: str, omit_str: list,
                            compress_water: bool):
        dot = DotWrapper(comment="Recipes graph with filter")
        direction = 1 if direction_str == "UP" else -1 if direction_str == "DOWN" else 0
        omit = list(map(lambda x: self.resources[self.resources_name_map[x]], omit_str))

        def draw_recursive_down(resource, curr_depth):
            if curr_depth > depth:
                return

            if compress_water and resource.is_water():
                return

            if resource in omit:
                return

            for recipe in resource.ingredient_of:
                if any(recipe.is_from_resource(x) for x in omit):
                    continue

                recipe.add_to_dot(dot, compress_water)

                for i in recipe.get_input_resources():
                    i.add_to_dot(dot, compress_water)

                for o in recipe.get_output_resources():
                    o.add_to_dot(dot, compress_water)
                    draw_recursive_down(o, curr_depth + 1)

        def draw_recursive_up(resource, curr_depth):
            if curr_depth > depth:
                return

            if compress_water and resource.is_water():
                return

            if resource in omit:
                return

            for recipe in resource.created_by:
                recipe.add_to_dot(dot, compress_water)

                for o in recipe.get_output_resources():
                    o.add_to_dot(dot, compress_water, o in omit)
                for i in recipe.get_input_resources():
                    i.add_to_dot(dot, compress_water, i in omit)
                    draw_recursive_up(i, curr_depth + 1)

        res = self.resources[self.resources_name_map[resource_human]]
        res.add_to_dot(dot, compress_water)
        if direction >= 0:
            draw_recursive_up(res, 1)
        if direction <= 0:
            draw_recursive_down(res, 1)
        return dot

    def add_factory(self, name, speed):
        if name in self.factories:
            warning("Factory name: {} taken".format(name))

        self.factories[name] = speed

        # Save it...
        self.overwrite_factories()
