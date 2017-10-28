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

    @staticmethod
    def out_file_writeln(out_file, content, indentation):
        indent = "\t" * indentation
        out_file.write(indent + content + "\n")

    def to_html(self, out_file_path):
        colors = ['9C9F84', 'A97D5D', 'F7DCB4', '5C755E']
        indent = 0
        total_height = 64.0
        total_size = len(self.sections[0])

        with open(out_file_path, "w") as out_file:
            self.out_file_writeln(out_file, "<html>", indent)
            indent += 1
            self.out_file_writeln(out_file, "<head>", indent)
            self.out_file_writeln(out_file, "<style>a { color: black; "
                                            "text-decoration: none; "
                                            "font-family:monospace }</style>",
                                  indent)
            self.out_file_writeln(out_file, "<body>", indent)
            indent += 1
            for section in self.sections:
                self.out_file_writeln(out_file, "<table cellspacing='1px'>",
                                      indent)
                indent += 1
                self.out_file_writeln(out_file, "<thead>", indent)
                indent += 1
                self.out_file_writeln(out_file, "<tr>", indent)
                indent += 1
                self.out_file_writeln(out_file,
                                      "<th>{0}</th>".format(section.section),
                                      indent)
                indent -= 1
                self.out_file_writeln(out_file, "</tr>", indent)
                indent -= 1
                self.out_file_writeln(out_file, "</thead>", indent)
                self.out_file_writeln(out_file, "<tbody>", indent)

                for i, sec in enumerate(section.sub_sections):
                    height = (total_height / total_size) * len(sec)
                    font_size = 1.0 if height > 1.0 else height
                    cell_color = colors[i % len(colors)]

                    indent += 1
                    self.out_file_writeln(out_file, "<tr style='background-color:#{color};height:{height}em;line-height:{height}em;font-size:{font_size}em'>".format(color=cell_color,height=height,font_size=font_size), indent)
                    indent += 1
                    self.out_file_writeln(out_file, "<td style='overflow:hidden'>{name}</td>".format(name=str(sec)), indent)
                    indent -= 1
                    self.out_file_writeln(out_file, "</tr>", indent)
                    indent -= 1
                self.out_file_writeln(out_file, "</tbody>", indent)
                indent -= 1
                self.out_file_writeln(out_file, "</table>", indent)
            indent -= 1
            self.out_file_writeln(out_file, "</body>", indent)
            indent -= 1
            self.out_file_writeln(out_file, "</html>", indent)
