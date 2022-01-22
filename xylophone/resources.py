import os


class ResourceLoader:
    def __init__(self):
        self._root = os.path.abspath('resources/')
        self._cached_resources = {}

    def read(self, path):
        path = self._root + "/" + path

        if path in self._cached_resources:
            modified_date, data = self._cached_resources[path]
            last_modified_date = os.path.getmtime(path)

            if modified_date != last_modified_date:
                new_data = open(path).read()
                self._cached_resources[path] = last_modified_date, new_data
                return new_data

            return data

        modified_date = os.path.getmtime(path)
        data = open(path).read()
        self._cached_resources[path] = modified_date, data

        return data


_loader = ResourceLoader()
read = _loader.read
