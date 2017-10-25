import argparse

from MapParser import MapParser

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Parse .map-file')
    parser.add_argument("map_file", metavar="i", type=str,
                        help="file path to .map-file")
    parser.add_argument("out_file", metavar="o", type=str,
                        help="file path to output-file")
    parser.add_argument("-f", "--format", type=str,
                        help="format of output-file", default="html")

    args = parser.parse_args()

    m_parser = MapParser()
    with open(args.map_file, 'r') as map_file:
        m_parser.parse(map_file)

    if args.format == "html":
        m_parser.to_html(args.out_file)

    print("Finished parsing")
