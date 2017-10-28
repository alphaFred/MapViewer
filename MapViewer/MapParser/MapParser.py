import re
from .ParserObjects import Section


class MapParser(object):
    def __init__(self):
        self.regex_start_sec = r"^\."
        self.regex_sec = r"^\s*\d"
        self.regex_fill = r"^\s\*"
        self.regex_start_subsec = r"^\s\."
        self.regex_ws_split = r"\s\s+"
        self.sections = []
        self.latestSection = None
        self.active_line = ""
        self.map_file = None
        self.line_iter = None

    def __get_line(self):
        for line in self.map_file:
            yield line

    def __update_line(self):
        if self.line_iter is None:
            self.line_iter = self.__get_line()
            next(self.line_iter)
            self.active_line = next(self.line_iter)
        else:
            self.active_line = next(self.line_iter)

    def parse(self, map_file):
        try:
            self.map_file = map_file
            self.__update_line()
            while True:
                if re.match(self.regex_start_sec, self.active_line):
                    section = Section()
                    self.__parse_section(section)
                    self.sections.append(section)
                else:
                    self.__update_line()
        except StopIteration:
            pass
        [s.parse() for s in self.sections]
        print("finished parsing")

    def __parse_section(self, section):
        try:
            section.append(self.active_line)
            self.__update_line()
            while True:
                if re.match(self.regex_sec, self.active_line):
                    section.append(self.active_line)
                    self.__update_line()
                elif re.match(self.regex_fill, self.active_line):
                    self.__update_line()
                elif re.match(self.regex_start_subsec, self.active_line):
                    sub_section = Section()
                    self.__parse_subsection(sub_section)
                    section.add_subsection(sub_section)
                    self.__update_line()
                else:
                    return
        except StopIteration:
            return

    def __parse_subsection(self, section):
        try:
            section.append(self.active_line)
            self.__update_line()
            while True:
                if re.match(self.regex_sec, self.active_line):
                    section.append(self.active_line)
                    self.__update_line()
                elif re.match(self.regex_fill, self.active_line):
                    self.__update_line()
                else:
                    return
        except StopIteration:
            return

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
            out_file.write(
                "<style>a { color: black; text-decoration: none; font-family:"
                "monospace }</style>")
            out_file.write("<body>")
            out_file.write("<table cellspacing='1px'>")
            for i, sec in enumerate(self.sections[1:]):
                height = (total_height / total_size) * len(sec)
                font_size = 1.0 if height > 1.0 else height
                out_file.write(
                    "<tr style='background-color:#%s;height:%gem;line-height:"
                    "%gem;font-size:%gem'><td style='overflow:hidden'>" % (
                        colors[i % len(colors)], height, height, font_size))
                out_file.write("<a href='#%s'>%s</a>" % (str(sec), str(sec)))
                out_file.write("</td></tr>")
            out_file.write("</table>")
            out_file.write("</body></html>")
