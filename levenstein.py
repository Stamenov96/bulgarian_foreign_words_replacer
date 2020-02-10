import numpy as np


def levenshtein_ratio_and_distance(source, target, ratio_calc=False):
    rows = len(source)+1
    cols = len(target)+1
    distance = np.zeros((rows, cols), dtype=int)

    # Populate matrix of zeros with the indeces of each character of both strings
    for i in range(1, rows):
        for k in range(1, cols):
            distance[i][0] = i
            distance[0][k] = k

    for col in range(1, cols):
        for row in range(1, rows):
            if source[row-1] == target[col-1]:
                cost = 0
            else:
                # In order to align the results with those of the Python Levenshtein package,
                # if we choose to calculate the ratio
                # the cost of a substitution is 2. If we calculate just distance, then the cost of a substitution is 1.
                if ratio_calc is True:
                    cost = 2
                else:
                    cost = 1
            distance[row][col] = min(distance[row-1][col] + 1,      # Cost of deletions
                                 distance[row][col-1] + 1,          # Cost of insertions
                                 distance[row-1][col-1] + cost)     # Cost of substitutions
    if ratio_calc is True:
        ratio = ((len(source)+len(target)) - distance[row][col]) / (len(source)+len(target))
        return ratio
    else:
        print(f'{source} and {target}')
        print(distance)
        return distance[row][col]


def match_strings(string, file_name_map, preprocess_method):
    max_raito = -1
    best_key = ""
    best_value = ""
    boost = 0.0
    processed_str = preprocess_method(string)
    for key, value in file_name_map.items():
        # flag = True
        preprocessed_value = preprocess_method(value)
        # for i in processed_str:
        #     flag = flag and (i in preprocessed_value)
        # if flag:
        #     boost = 0.1
        # else:
        #     boost = 0.0
        ratio = levenshtein_ratio_and_distance(processed_str, preprocessed_value, ratio_calc=True)+boost

        if ratio > max_raito:
            max_raito = ratio
            best_key = key
            best_value = value
        elif ratio == max_raito:
            if levenshtein_ratio_and_distance(processed_str, preprocess_method(value), ratio_calc=False) < levenshtein_ratio_and_distance(processed_str, preprocess_method(best_value), ratio_calc=False):
                best_key = key
                best_value = value
    return best_key, best_value


