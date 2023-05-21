import json
import zlib
import base64


def decode(data):
    return json.loads(zlib.decompress(base64.b64decode(data[1:])).decode('UTF-8'))


def encode(data):
    return '0' + base64.b64encode(zlib.compress(bytes(json.dumps(data), 'UTF-8'))).decode('UTF-8')


def sheet(entities, name):
    return {
        "blueprint": {
            "icons": [
                {
                    "signal": {
                        "type": "item",
                        "name": "train-stop"
                    },
                    "index": 1
                }
            ],
            "entities": entities,
            "item": "blueprint",
            "label": name,
            "version": 281479273316352  # factorio version 1.1.15
        }
    }


def book(sheets):
    prints = []
    i = 0
    for sheet in sheets:
        sheet["index"] = i
        prints.append(sheet)
        i += 1

    return {
        "blueprint_book": {
            "blueprints": prints,
            "item": "blueprint-book",
            "active_index": 0,
            "version": 281479273316352
        }
    }

def from_file(path):
    with open(path) as data:
        return json.load(data)
