class Section:
    def __init__(self):
        self.address = ""
        self.size = ""
        self.segment = ""
        self.section = ""
        self.lines = []
        self.sub_sections = []

    def __str__(self):
        if self.segment:
            return ".".join((self.section, self.segment))
        else:
            return self.section

    def __repr__(self):
        if self.segment:
            return ".".join((self.section, self.segment)) + " " + " - ".join((
                self.address, self.size))
        else:
            return self.section + " " + " - ".join((
                self.address, self.size))

    def __len__(self):
        return self.size

    def append(self, line):
        self.lines.append(line)

    def add_subsection(self, section):
        self.sub_sections.append(section)

    def parse(self):
        if len(self.lines[0].split()) == 1:
            self.__parse_name(self.lines[0])
            self.__parse_address(self.lines[1].split()[0])
            self.__parse_size(self.lines[1].split()[1])
        else:
            self.__parse_name(self.lines[0].split()[0])
            self.__parse_address(self.lines[0].split()[1])
            self.__parse_size(self.lines[0].split()[2])
        for sub_section in self.sub_sections:
            sub_section.parse()

    def __parse_name(self, sec_name):
        sec_names = list(filter(None, sec_name.strip().split(".")))
        self.section = sec_names[0]
        if len(sec_names) > 1:
            self.segment = ".".join(sec_names[1:])

    def __parse_address(self, sec_address):
        self.address = int(sec_address, 16)

    def __parse_size(self, sec_size):
        self.size = int(sec_size, 16)
