import re

class YamlParser:
    def __init__(self, key, fStream):
        self._regexAllYAML = r'(?<=---\n)(?:.*\n)+(?=---)'
        self._regexFindKey = rf'(?:(?<={key}:).*?\[(.+?)(?=\]))|(?:(?<={key}:).*\n((?:-\s.*\n?)+))'
        self.fStream = fStream
        self.result = None
        
    def _findAllYAML(self):
        match = re.search(self._regexAllYAML, self.fStream)
        #print(match)
        if match != None:
            self.result = match.group()
            #print(self.result)
            return self._findValueInYAML()
        else:
            return None


    def _findValueInYAML(self) -> set:
        """Return a set of all values stored in YAML

        In order to retrieve a value, it must be in one of the 2 formats:
        1. YAML array format
        ```
        key: [value1, value2]
        ```
        2. Yaml list format
        ```
        key:
        - value1
        ```
        """
        # all the values are stored in this set
        self.values = set()


        match = re.search(self._regexFindKey, self.result)
        result1 = None
        result2 = None

        if match != None:
            result1 = match.group(1)
            #print(result1)
            result2 = match.group(2)
            #print(result2)

        # code works as expected until here

        if result1 != None: # Find all values in YAML with format key: [value1, value2,...]
            new_result1 = result1.split(',')
            #print(new_result1)
            for element in new_result1:
                element = element.strip('\"')
                element = element.strip()
                #print(element)
                self.values.add(element)
            #print(self.values)
        # Find all values in YAML with format
        # key:
        # - value1
        # - value2
        # ...
        elif result2 != None:
            #print(result2)
            result2 = result2.split()
            #print(result2)
            for element in result2:
                if element != '-':
                    element = element.strip('\"')
                    self.values.add(element)
            #print(self.values)
        #print(self.values)
        return self.values
