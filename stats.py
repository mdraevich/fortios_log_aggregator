# /usr/bin/python3 

"""

INPUT:
- FortiGate logs in CSV format 

OUTPUT:
- returns the percentage occurence of 
  log messages grouped by logid 

"""

import os
import sys



class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def percent(part, whole):
    if whole == 0:
        return 0
    else: 
        return "%.2f" % (part / whole * 100)


def color_print(text, color=bcolors.ENDC, *args, **kwargs):
    if text is None:
        text = ""
    #
    print(color + text + bcolors.ENDC, *args, **kwargs)


def update_status(current_value, max_value):
    print("\033[2A")
    color_print("Status: {}%       [{}/{}]".format(
                                            percent(current_value, max_value), 
                                            current_value, 
                                            max_value), 
                                        bcolors.OKBLUE + bcolors.BOLD)


def increment(dict_obj, key):
    if key in dict_obj:
        dict_obj[key] += 1
    else:
        dict_obj[key] = {
            "count": 1,
            "description": None,
            "type": None,
            "subtype": None,
        }


assert len(sys.argv) == 2  # only program name & input csv file 


try: 
    csv_file_path = os.path.abspath(sys.argv[1])
    number_lines = sum(1 for line in open(csv_file_path, "r", errors="replace"))
except Exception as e: 
    print("ERROR: Failed to determine the path to file...")
    print(e)
    exit()


color_print("Filepath:       {}".format(csv_file_path), bcolors.HEADER + bcolors.BOLD)
color_print("Size (lines):   {}".format(number_lines), bcolors.HEADER + bcolors.BOLD)
print()
print()



stats = {}
description = {}
processed_lines = 0
with open(csv_file_path, "r", errors="replace") as csv_file:
    for line in csv_file:
        try:
            parsed_line = line
            parsed_line = [ el.replace('"', "").strip().split("=", 1) for el in parsed_line.split(",") ] 
            parsed_line = [ el for el in parsed_line if len(el) == 2 ]
            #
            entry = {}
            for key, value in parsed_line:
                entry[key] = value
            #
            #
            #
            logid = entry["logid"] 
            if logid not in stats.keys():
                stats[logid] = {
                    "count": 1,
                    "description": entry.get("logdesc"),
                    "subtype": entry.get("subtype"),
                    "type": entry.get("type"),
                } 
            else:
                stats[logid]["count"] += 1

            processed_lines += 1
            if processed_lines % 300 == 0 or processed_lines == number_lines:
                update_status(processed_lines, number_lines)
        except Exception as e:
            color_print(str(e), bcolors.FAIL)





report = [ [key, value] for key, value in stats.items()  ]
report.sort(reverse=True, key=lambda x: x[1]["count"])



print()
color_print("Finished! Check this out...", bcolors.OKGREEN + bcolors.BOLD)
print()


pos = 1
for line in report:
    # top position and logid
    color_print("{}  [{}]:".format(line[0], pos), bcolors.OKBLUE + bcolors.BOLD)


    # percentage of logid
    color_print("    Percent: {}%    ".format(percent(line[1]["count"], number_lines)), 
                                                bcolors.HEADER + bcolors.BOLD, end="")
    color_print("[{}/{}]".format(line[1]["count"], number_lines), bcolors.HEADER)


    # type & subtype 
    color_print("    Type: ", bcolors.HEADER + bcolors.BOLD, end="")
    color_print(line[1]["type"], bcolors.HEADER)

    color_print("    Subtype: ", bcolors.HEADER + bcolors.BOLD, end="")
    color_print(line[1]["subtype"], bcolors.HEADER)


    # description 
    color_print("    Description: ", bcolors.HEADER + bcolors.BOLD, end="")
    color_print(line[1]["description"], bcolors.HEADER)


    print()

    pos += 1
