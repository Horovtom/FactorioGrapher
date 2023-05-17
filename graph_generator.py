# TODO: ADD FROM/TO Graph generation

from gui.gui import GUI
from logic.Graph import Graph
from logic.bus import Bus

g = Graph(recipes="resources/processed/py_recipes.json", factories="resources/factories.json")
bus = Bus(file="resources/on_bus.txt", graph=g)

a = GUI(g, bus)
a.run()

# def run():
#     with open("resources{}recipes.json".format(os.sep), 'r') as recipes_file:
#         recipes = json.load(recipes_file)
#
#     g = Graph(recipes)
#
#     compress_water = input("Do you want to compress water into nodes? (y/n): ")
#     compress_water = len(compress_water) == 0 or compress_water.lower() == "y"
#
#     dot = g.get_dot(compress_water)
#
#     dot.render("output", view=True)
#
#
# if __name__ == "__main__":
#     run()
