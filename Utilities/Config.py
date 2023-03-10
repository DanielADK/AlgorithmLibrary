from os.path import exists


class Config:
    def __init__(self, path: str):
        if not exists(path):
            raise Exception("Config file not found!")

        self.__path: str = path
        self.__options: dict[str, any] = dict()

        with open(path, "r", encoding="utf-8") as f:
            for line in f.read().split("\n"):
                if len(line) == 0:
                    continue
                split = line.split(" = ")
                self.__options[split[0]] = self.__parseValue(split[1])


    def __parseValue(self, value: str):
        return int(value) if value.isnumeric() else str(value)

    def get(self, value: str) -> any:
        return self.__options.get(value)
