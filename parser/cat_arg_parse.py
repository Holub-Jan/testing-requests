from pydantic import BaseModel


class CatWord(BaseModel):
    name: str
    inputs: int = 0
    children: list = []
    arguments: list = []
    description: str = ''


class CatArgParse:
    def __init__(self, name: str = 'parser'):
        # SIDE PROJECT,  to be completed
        self._cat_dict = dict()
        self._args = list()
        self._arg_cats = list()

        # rework below
        self._cat_stack = CatWord(name=name)

    def return_cats(self, args: list):
        # --repo --edit {repo_name} --name {new_repo_name}
        self._args = args
        self._arg_cats = [arg.strip('-') for arg in args if '-' in arg]

        child_data = self._one_child_present('')

        if isinstance(child_data, str):
            return child_data

        command = list()

        while isinstance(child_data, tuple):
            child, child_inputs = child_data

            arg_inputs = self._check_inputs(child)
            if isinstance(arg_inputs, list):
                command.append((child, arg_inputs))
                child_data = self._one_child_present(child)
            else:
                return arg_inputs

        return command

    def _one_child_present(self, parent: str):
        children = self._get_children(parent)
        children_present = [child for child in children if child in self._arg_cats]

        if len(children) > 0:
            if len(children_present) == 1:
                child = children_present[0]
                children_inputs = self._cat_dict[child]['inputs']
                return child, children_inputs
            else:
                return f'Error: Number of children present is {len(children_present)}, expected one.'

    def edit_or_add_category(self, cat_key: str, inputs: int, func=None, parent: str = '', description: str = ''):
        self._cat_dict[cat_key] = {'parent': parent, 'inputs': inputs, 'function': func, 'description': description}

    def remove_category(self, cat_key: str):
        self._cat_dict.pop(cat_key, None)

    def _get_children(self, parent: str) -> list:
        return [key for key, value in self._cat_dict.items() if value['parent'] == parent]

    def _check_inputs(self, cat: str):
        cat_pos = self._args.index('--' + cat)
        num_of_inputs = self._cat_dict[cat]['inputs']

        input_list = list()

        for num in range(num_of_inputs):
            input_pos = cat_pos+num+1
            if input_pos < len(self._args) and '-' not in self._args[input_pos]:
                input_list.append(self._args[input_pos])
            else:
                return f'Expected {num_of_inputs} number of inputs, got {num}'

        return input_list

    def get_help(self):
        for key, value in self._cat_dict.items():
            print(f'-- Category "{key}" --'
                  f'\nDescription: {value["description"]}'
                  f'\nNumber of inputs {value["inputs"]}'
                  f'\nParent: {value["parent"]}\n')

    def add_cat(self, name: str, inputs: int = 0, description: str = ''):
        cat = CatWord(name=name, inputs=inputs, description=description)
        self._cat_stack.append(cat)
        return cat

    def add_argument(self, name: str, inputs: int = 0, description: str = ''):
        pass

