class vm_loader:

    def __init__(self):
        pass

def _parse_line(line):
    # """
    # Do a regex search against all defined regexes and
    # return the key and match result of the first matching regex
    #
    # """
    #
    # for key, rx in rx_dict.items():
    #     match = rx.search(line)
    #     if match:
    #         return key, match
    # # if there are no matches
    # return None, None
    pass

def read_file_v01(file_object):
    line = file_object.readline()

    line = line.lstrip("#")
    line = line.strip("\n")
    x = line.split("#")
    print(x)
    if x[1] == "LANE":
        print(x[1])


def read_file(filepath):
    """
    Parse text at given filepath

    Parameters
    ----------
    filepath : str
        Filepath for file_object to be parsed

    Returns
    -------
    data : pd.DataFrame
        Parsed data

    """

    data = []  # create an empty list to collect the data
    # open the file and read through it line by line
    with open(filepath, 'r') as file_object:
        line = file_object.readline()
        x = line.split("#")
        if float(x[4]) == 0.1:
            read_file_v01(file_object)

    #     while line:
    #         # at each line check for a match with a regex
    #         key, match = _parse_line(line)
    #
    #         # extract school name
    #         if key == 'school':
    #             school = match.group('school')
    #
    #         # extract grade
    #         if key == 'grade':
    #             grade = match.group('grade')
    #             grade = int(grade)
    #
    #         # identify a table header
    #         if key == 'name_score':
    #             # extract type of table, i.e., Name or Score
    #             value_type = match.group('name_score')
    #             line = file_object.readline()
    #             # read each line of the table until a blank line
    #             while line.strip():
    #                 # extract number and value
    #                 number, value = line.strip().split(',')
    #                 value = value.strip()
    #                 # create a dictionary containing this row of data
    #                 row = {
    #                     'School': school,
    #                     'Grade': grade,
    #                     'Student number': number,
    #                     value_type: value
    #                 }
    #                 # append the dictionary to the data list
    #                 data.append(row)
    #                 line = file_object.readline()
    #
    #         line = file_object.readline()
    #
    #     # create a pandas DataFrame from the list of dicts
    #     data = pd.DataFrame(data)
    #     # set the School, Grade, and Student number as the index
    #     data.set_index(['School', 'Grade', 'Student number'], inplace=True)
    #     # consolidate df to remove nans
    #     data = data.groupby(level=data.index.names).first()
    #     # upgrade Score from float to integer
    #     data = data.apply(pd.to_numeric, errors='ignore')
    # return data

if __name__ == '__main__':
    filepath = 'D:\\workspace\\python\\route-planner\\data\\MiniPolygonGraph.namivm'
    data = read_file(filepath)
    # print(data)