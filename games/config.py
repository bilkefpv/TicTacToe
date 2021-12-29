from configparser import ConfigParser

class help_config:
    def __init__(self):
        self.config = ConfigParser()
        self.read()

    def set(self, section, key, value):
        self.config.set(section, key, value)
        self.write()

    def write(self):
        with open('agent/config.ini', 'w') as f:
            self.config.write(f)

    def read(self):
        self.config.read('agent/config.ini')

    def get(self,section, key):
        self.read()
        return self.config.get(section, key)
