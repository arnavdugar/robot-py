import json


def save(item, filename="model.txt"):
    try:
        string = build_string(item)
    except Exception as e:
        raise e
    else:
        with open(filename, 'w') as f:
            f.write(string)


def build_string(item, indent='    ', indent_count=0):
    if isinstance(item, (list, tuple)):
        return "[" + ', '.join(build_string(child, indent, indent_count) for child in item) + "]"
    elif hasattr(item, "properties"):
        indent_count += 1
        string = "{\n" + indent * indent_count + "\"class\": \"" + type(item).__name__ + "\""
        for key in item.properties:
            if hasattr(item, key):
                string += ",\n" + indent * indent_count + "\"" + key + "\": "
                string += build_string(getattr(item, key), indent, indent_count)
        indent_count -= 1
        string += "\n" + indent * indent_count + "}"
        return string
    elif isinstance(item, str):
        return "\"" + item + "\""
    else:
        return str(item)


def load(globals, filename="model.txt"):
    with open(filename, 'r') as f:
        data = json.loads(f.read())
    return build_object(globals, data)


def build_object(globals, data, parent=None):
    if isinstance(data, dict):
        item = globals[data["class"]]()
        item.parent = parent
        for key in data:
            child = build_object(globals, data[key], item)
            setattr(item, key, child)
        if hasattr(item, "init"):
            item.init()
        return item
    elif isinstance(data, (list, tuple)):
        item, index = [], 0
        for child_data in data:
            child = build_object(globals, child_data, parent)
            item.append(child)
            if hasattr(child, "__dict__"):
                child.index = index
            index += 1
        return tuple(item)
    else:
        return data