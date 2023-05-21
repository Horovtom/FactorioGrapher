import json
import blueprint


def generate_mall(recipie_left, recipie_right):
    left_requester_requests = []
    right_requester_requests = []
    for ingredient in recipie_left["ingredients"]:
        left_requester_requests.append({
            "index": len(left_requester_requests) + 1,
            "name": ingredient["name"],
            "count": ingredient["stack_size"]
        })
    for ingredient in recipie_right["ingredients"]:
        right_requester_requests.append({
            "index": len(right_requester_requests) + 1,
            "name": ingredient["name"],
            "count": ingredient["stack_size"]
        })

    return [
            {
                "entity_number": 1,
                "name": "automated-factory-mk01",
                "position": {
                    "x": -235.5,
                    "y": -120.5
                },
                "recipe": recipie_left["name"]
            },
            {
                "entity_number": 2,
                "name": "automated-factory-mk01",
                "position": {
                    "x": -225.5,
                    "y": -120.5
                },
                "recipe": recipie_right["name"]
            },
            {
                "entity_number": 3,
                "name": "medium-electric-pole",
                "position": {
                    "x": -230.5,
                    "y": -120.5
                }
            },
            {
                "entity_number": 4,
                "name": "logistic-chest-requester",
                "position": {
                    "x": -230.5,
                    "y": -119.5
                },
                "request_filters": right_requester_requests
            },
            {
                "entity_number": 5,
                "name": "logistic-chest-passive-provider",
                "position": {
                    "x": -230.5,
                    "y": -118.5
                }
            },
            {
                "entity_number": 6,
                "name": "fast-inserter",
                "position": {
                    "x": -231.5,
                    "y": -118.5
                },
                "direction": 6,
                "control_behavior": {
                    "logistic_condition": {
                        "first_signal": {
                            "type": "item",
                            "name": recipie_left["result"]["name"]
                        },
                        "constant": recipie_left["result"]["stack_size"] * 2,
                        "comparator": "<"
                    },
                    "connect_to_logistic_network": True
                }
            },
            {
                "entity_number": 7,
                "name": "stack-inserter",
                "position": {
                    "x": -229.5,
                    "y": -119.5
                },
                "direction": 6
            },
            {
                "entity_number": 8,
                "name": "fast-inserter",
                "position": {
                    "x": -229.5,
                    "y": -118.5
                },
                "direction": 2,
                "control_behavior": {
                    "logistic_condition": {
                        "first_signal": {
                            "type": "item",
                            "name": recipie_right["result"]["name"]
                        },
                        "constant": recipie_right["result"]["stack_size"] * 2,
                        "comparator": "<"
                    },
                    "connect_to_logistic_network": True
                }
            },
            {
                "entity_number": 9,
                "name": "logistic-chest-requester",
                "position": {
                    "x": -230.5,
                    "y": -117.5
                },
                "request_filters": left_requester_requests
            },
            {
                "entity_number": 10,
                "name": "stack-inserter",
                "position": {
                    "x": -231.5,
                    "y": -117.5
                },
                "direction": 2
            }
        ]


if __name__ == "__main__":
    # with open("./template.blueprint") as data:
    #     template = blueprint.decode(data.read())
    # # save template as json
    # with open("./template.json", "w") as data:
    #     data.write(json.dumps(template))

    stack_size_table = {}
    with open("./stack_size.json") as data:
        template = json.loads(data.read())
        for item in template:
            stack_size_table[item["name"]] = item["stack_size"]
    
    recipies_table = {}
    with open("./recipes_py.json") as data:
        template = json.loads(data.read())
        for name, recipe in template.items():
            if len(recipe["products"]) != 1:
                continue

            if recipe["products"][0]["type"] != "item":
                continue

            ingredients = []
            for ingredient in recipe["ingredients"]:
                if ingredient["type"] != "item":
                    continue
                ingredients.append({
                    "name": ingredient["name"],
                    "stack_size": stack_size_table[ingredient["name"]]
                })
            
            product = {
                "name": recipe["products"][0]["name"],
                "stack_size": stack_size_table[recipe["products"][0]["name"]]
            }

            recipies_table[recipe["products"][0]["name"]] = {
                "name": name,
                "ingredients": ingredients,
                "result": product
            }
    
    with open("./wanted.json", "r") as f:
        wanted_recipies = json.loads(f.read())

    # group wanted recipies into pairs
    recipies_pairs = []
    for i in range(0, len(wanted_recipies), 2):
        recipies_pairs.append((wanted_recipies[i], wanted_recipies[i+1]))
    
    pages = []
    # generate mall for each pair
    for recipie_pair in recipies_pairs:
        entities = generate_mall(recipies_table[recipie_pair[0]], recipies_table[recipie_pair[1]])
        pages.append(blueprint.sheet(entities, recipie_pair[0] + " + " + recipie_pair[1]))

    # generate blueprint book
    book = blueprint.book(pages)
    with open("./book.blueprint", "w") as f:
        f.write(blueprint.encode(book))
