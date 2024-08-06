import os
from libraries import get_app_path


def main():
    # full path to the config file. works because the config file is in the same directory as the running file
    full_path = os.path.abspath(get_app_path.config())

    # open the config file and prepare for translation
    conf_file = open(full_path, "r")
    conf = {}

    # read all the lines and add them to a list
    lines = conf_file.readlines()
    parent_dict_name = None

    # loop over each line to translate it
    for line in lines:
        if line != "\n":
            # if there is [] in the line that means we need to create a new dictionary for the new section
            if "[" in line:
                line = line.removesuffix("\n")
                line = line.removesuffix("]")
                line = line.removeprefix("[")
                parent_dict_name = line

                conf[parent_dict_name] = {}

            else:
                # every line ends with \n which we want to ignore to get clean bools
                line = line.removesuffix("\n")

                # we then want to remove the spaces and the equal sign
                line = line.split(" = ")

                # the values inside the flags section are always bools
                if parent_dict_name == "Flags":
                    # the first value is the key, the second is the value
                    conf[parent_dict_name][line[0]] = str_to_bool(line[1])
                # we need to do tha same thing except the values inside the general section are always ints
                elif parent_dict_name == "General":
                    # the first value is the key, the second is the value
                    conf[parent_dict_name][line[0]] = int(line[1])

    return conf


def str_to_bool(string):
    if string == "True":
        return True
    elif string == "False":
        return False
    else:
        return None
