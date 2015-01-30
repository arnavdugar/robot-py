import json
import code

package = None


def save(item, filename):
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
        string = "{\n" + indent * indent_count + "\"class\": \"" + item.__module__ + "." + type(item).__name__ + "\""
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


def load(filename):
    with open(filename, 'r') as f:
        data = json.loads(f.read())
    return build_item(data)


def build_item(data, parent=None):
    if isinstance(data, dict):
        return build_object(data, parent)
    elif isinstance(data, (list, tuple)):
        return build_list(data, parent)
    else:
        return data


def build_object(data, parent):
    class_name = package
    for part in data["class"].split('.'):
        class_name = getattr(class_name, part)
    item = class_name()
    item.parent = parent
    for key in data:
        child = build_item(data[key], item)
        try:
            setattr(item, key, child)
        except AttributeError as e:
            code.interact(local=locals())
            print(e, type(item), key, child)
    if hasattr(item, "init"):
        item.init()
    return item


def build_list(data, parent):
    item, index, previous = [], 0, None
    for child_data in data:
        child = build_item(child_data, parent)
        item.append(child)
        if hasattr(child, "__dict__"):
            child.index = index
            child.siblings = item
            child.previous = previous
            if previous:
                previous.next = child
        previous = child
        index += 1
    if hasattr(child, "__dict__"):
        child.next = None
    return tuple(item)