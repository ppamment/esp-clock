# Give NVS and file a common interface

class NVSStore:
    def __init__(self, namespace: str):
        from esp32 import NVS
        self.namespace = namespace
        self.nvs = NVS(namespace)

    def get(self, key = "time") -> int:
        try:
            return self.nvs.get_i32(key)
        except:
            return 0

    def set(self, key: str, value: int):
        self.nvs.set_i32(key, value)
        self.nvs.commit()

class FileStore:
    def __init__(self, filename: str):
        self.filename = filename
        self.file = open(filename, "r+")

    def get(self, key: str) -> int:
        try:
            return int(self.file.read().strip())
        except:
            return 0

    def set(self, key: str, value: int):
        self.file.seek(0)
        self.file.write(f"{value:03}\n")

def get_store():
    try:
        return NVSStore("clock")
    except:
        return FileStore("clock.txt")