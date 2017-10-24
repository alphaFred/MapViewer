import re
from .ParserObjects import Section


class MapParser(object):
    def __init__(self):
        self.regex_start_sec = r"^\."
        self.regex_sec = r"^\s*\d"
        self.regex_start_subsec = r"^\s\."
        self.regex_ws_split = r"\s\s+"
        self.sections = []
        self.latestSection = None

    def parse(self, map_file):
        self.latestSection = Section()
        in_section = False

        for line in map_file:
            if re.match(self.regex_start_sec, line):
                if in_section:
                    self.__finish_section()
                self.latestSection.append(line)
                in_section = True
            elif re.match(self.regex_start_subsec, line):
                if in_section:
                    self.__finish_section()
                self.latestSection.append(line)
                in_section = True
            elif re.match(self.regex_sec, line):
                self.latestSection.append(line)
                in_section = True
            else:
                self.__finish_section()
                in_section = False
        # process each section
        [s.parse() for s in self.sections]
        pass

    def __finish_section(self):
        if len(self.latestSection.lines) != 0:
            self.sections.append(self.latestSection)
            self.latestSection = Section()
