"""
Author - O
Purpose - script for converting itermcolors theme to mobaxterm colors
"""

import xmltodict
import argparse
from sys import argv


ANSI_TO_MOBA = {
"Ansi 0 Color"  : "Black",
"Ansi 1 Color"  : "Red",
"Ansi 2 Color"  : "Green",
"Ansi 3 Color"  : "Yellow",
"Ansi 4 Color"  : "Blue",
"Ansi 5 Color"  : "Magenta",
"Ansi 6 Color"  : "Cyan",
"Ansi 7 Color"  : "White",
"Ansi 8 Color"  : "BoldBlack",
"Ansi 9 Color"  : "BoldRed",
"Ansi 10 Color" : "BoldGreen",
"Ansi 11 Color" : "BoldYellow",
"Ansi 12 Color" : "BoldBlue",
"Ansi 13 Color" : "BoldMagenta",
"Ansi 14 Color" : "BoldCyan",
"Ansi 15 Color" : "BoldWhite",
"Background Color" : "BackgroundColour",
"Foreground Color" : "ForegroundColour",
"Cursor Color" : "CursorColour",
}

def get_rgb(colors):
    """
    @param colors  dict of {color: data}
    @return  list that looks like this [(color, rgb), (color, rgb), ...]
    """
    res = []
    for color, data in colors.items():
        true_color = [float(val) for val in data['real'][1:]] # b,g,r
        true_color = [int(val * 256) for val in true_color]
        res.append((color, f"{true_color[2]},{true_color[1]},{true_color[0]}"))
    return res


def dictify(colors):
    res = {}
    for i in range(len(colors['key'])):
        res[colors['key'][i]]  = colors['dict'][i]
    return res


def print_res(result):
    for color, rgb in result:
        print(f"{color} = {rgb}")

def save_res(output_path, result):
    with open(output_path, "w") as f:
        f.write("[Colors]\n")
        for color, rgb in result:
            try:
                f.write(f"{ANSI_TO_MOBA[color]}={rgb}\n")
            except:
                pass
        f.write("DefaultColorScheme=0\nSyntaxType=1\n")  # default?


def parse_arguments():
    parser = argparse.ArgumentParser(description="Parse XML and generate xterm style INI file.")
    parser.add_argument("--xml_path", default="colors.xml", help="Path to the input XML file, this should be output of exporting termcolor colorscheme")
    parser.add_argument("--output_path", default="xterm_style.ini", help="Path to the output INI file")
    return parser.parse_args()


def main(xml_path, output_path):

    with open(xml_path, "r") as f:
        content = f.read()

    parsed = xmltodict.parse(content)
    colors = parsed['plist']['dict']

    colors = dictify(colors)
    res = get_rgb(colors)
    print_res(res)
    save_res(output_path, res)


if __name__ == "__main__":
    args = parse_arguments()
    main(args.xml_path, args.output_path)
