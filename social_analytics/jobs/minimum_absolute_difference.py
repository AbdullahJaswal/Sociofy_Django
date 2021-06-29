def minimum_absolute_difference(integers_list):
    min_absolute_difference = float("inf")

    sorted_integers_list = sorted(integers_list)

    for index in range(0, len(sorted_integers_list)-1):
        small_num = sorted_integers_list[index]
        large_num = sorted_integers_list[index+1]
        absolute_difference = abs(large_num-small_num)
        if absolute_difference <= min_absolute_difference:
            min_absolute_difference = absolute_difference

    # we have the exact min_absolute_difference
    min_pairs_list = []

    for index in range(0, len(sorted_integers_list)-1):
        small_num = sorted_integers_list[index]
        large_num = sorted_integers_list[index+1]
        absolute_difference = abs(large_num-small_num)
        if absolute_difference == min_absolute_difference:
            min_pairs_list.append([small_num, large_num])
    return min_pairs_list
