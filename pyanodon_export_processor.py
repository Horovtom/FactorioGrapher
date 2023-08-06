import json

with open("resources/raw/recipes_py.json", "r") as f:
    recipes = json.load(f)

res = {}
for key in recipes.keys():
    if "-unbarreling" in key or "-barrel" in key or "-pyvoid" in key or "blackhole-fuel-" in key or "-canister" in key:
        continue

    res[key] = {
        "category": recipes[key]["category"],
        "time": recipes[key]["energy"]
    }

    outs = []
    for product in recipes[key]["products"]:
        if "amount" not in product:
            if "amount_min" not in product or "amount_max" not in product:
                print("FUCUCUCUCUCUCUUCCK")

            amount = (product["amount_min"] + product["amount_max"]) / 2
        else:
            amount = product["amount"]

        if "probability" in product:
            amount *= product["probability"]

        r = {
            "resource" : product["name"],
            "amount": amount
        }
        outs.append(r)

    res[key]["outputs"] = outs

    ins = []
    for input in recipes[key]["ingredients"]:
        r = {
            "resource" : input["name"],
            "amount" : input["amount"]
        }
        ins.append(r)

    res[key]["inputs"] = ins

with open("resources/processed/py_recipes.json", "w") as file:
    json.dump(res, file)
