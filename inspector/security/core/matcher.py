import re


class PatternMatcher:

    def __init__(self):
        self.cache = {}

    def compile(self, pattern):

        if pattern not in self.cache:

            self.cache[pattern] = re.compile(
                pattern,
                re.IGNORECASE,
            )

        return self.cache[pattern]

    def search(self, pattern, text):

        try:

            regex = self.compile(pattern)

            return regex.search(text)

        except re.error:

            return None

    def findall(self, pattern, text):

        try:

            regex = self.compile(pattern)

            return regex.findall(text)

        except re.error:

            return []

    def match(self, pattern, text):

        try:

            regex = self.compile(pattern)

            return regex.match(text)

        except re.error:

            return None