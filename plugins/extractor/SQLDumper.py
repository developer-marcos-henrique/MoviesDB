import sqlite3
import os

class dumper:
    def __init__(self, mode="cache"):
        self.mode = mode
        self.caching_path = os.getcwd()+"/data/cache/"
        self.configuraiton_path = os.getcwd()+"/data/configuration/"
        self.pointer = object

    def __enter__(self):

        while True:
            try:
                match self.mode:
                    case "cache":
                        self.connect = sqlite3.connect(self.caching_path+"cache.db")

                    case "configuration":
                        self.connect = sqlite3.connect(self.configuraiton_path+"configuration.db")     
                break  

            except sqlite3.OperationalError as e:
                match str(e):
                    case "unable to open database file":
                        self._check_file_system()

                    case _:
                        print(e, type(e))

        return self

    def __exit__(self, x, y, z, b):
        self.connect.close()


    def _check_file_system(self):
        if os.path.exists(self.caching_path) == False:
            os.makedirs(self.caching_path)
            print("gerado")

        if os.path.exists(self.configuraiton_path) == False:
            os.makedirs(self.configuraiton_path)
            print("gerado")



with dumper() as x:
    pass

