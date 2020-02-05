import json

recipes: dict
with open("resources/recipes_exported.json", 'r') as recipes_file:
    recipes = json.load(recipes_file)

done = {}
for key in recipes.keys():
    if "-barrel" in key:
        continue
    done[key] = {
        "category": recipes[key]["category"],
        "time": recipes[key]["energy"]
    }

    if "products" not in recipes[key]:
        print("FUCK")

    # Get outputs
    outs = []
    for res in recipes[key]["products"]:
        if "amount" not in res:
            if "amount_min" not in res or "amount_max" not in res:
                print("FUCK")

            amount = (res["amount_min"]+res["amount_max"])/2
        else:
            amount = res["amount"]

        if "probability" in res:
            amount *= res["probability"]

        r = {
            "resource": res["name"],
            "amount": amount
        }
        outs.append(r)

    done[key]["outputs"] = outs
    # Get inputs
    ins = []
    for res in recipes[key]["ingredients"]:
        r = {
            "resource": res["name"],
            "amount": res["amount"]
        }
        ins.append(r)
    done[key]["inputs"] = ins

with open("resources/recipes_exported_edited.json", "w") as file:
    json.dump(done, file)
