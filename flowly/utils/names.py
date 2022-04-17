import os
from pathlib import Path


def path_to_identity(contained_path, root_path, root_module):
    relative_path = contained_path[len(root_path + os.path.sep):]
    return f'{root_module}.{".".join(relative_path.split(os.path.sep))}'


def find_yaml_files(namespace):
    root_path = Path(namespace.path)
    root_module = namespace.unique_name
    return _find_yaml_files(root_path, str(root_path), root_module, list())

def _find_yaml_files(dir_path, root_path, root_module, results):
    from flowly.stores.names import NameStore
    for contained in dir_path.iterdir():
        if contained.is_dir():
            identity = path_to_identity(str(contained), root_path, root_module)
            if not NameStore.exists(identity):
                _find_yaml_files(contained, root_path, root_module, results)
        else:
            if contained.suffix == '.yaml':
                results.append(str(contained))
            # print_indented(contained.name, level+1)
    return results
