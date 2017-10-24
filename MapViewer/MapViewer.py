import argparse

from MapParser import MapParser

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Parse .map-file')
    parser.add_argument("map_file", metavar="f", type=str,
                        help="file path to .map-file")

    args = parser.parse_args()

    m_parser = MapParser()
    with open(args.map_file, 'r') as map_file:
        m_parser.parse(map_file)
    print("Finished parsing")
