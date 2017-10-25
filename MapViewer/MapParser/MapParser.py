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

    def to_html(self, out_file_path):
        colors = ['9C9F84', 'A97D5D', 'F7DCB4', '5C755E']
        total_height = 32.0
        total_size = len(self.sections[0])

        with open(out_file_path, "w") as out_file:
            out_file.write("<html><head>")
            out_file.write("<style>a { color: black; text-decoration: none; font-family:monospace }</style>")
            out_file.write("<body>")
            out_file.write("<table cellspacing='1px'>")
            for i, sec in enumerate(self.sections[1:]):
                height = (total_height / total_size) * len(sec)
                font_size = 1.0 if height > 1.0 else height
                out_file.write("<tr style='background-color:#%s;height:%gem;line-height:%gem;font-size:%gem'><td style='overflow:hidden'>" % (colors[i % len(colors)], height, height, font_size))
                out_file.write("<a href='#%s'>%s</a>" % (str(sec), str(sec)))
                out_file.write("</td></tr>")
            out_file.write("</table>")
            out_file.write("</body></html>")
