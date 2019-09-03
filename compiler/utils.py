class Utils:

    @staticmethod
    def find_string_in_string_array(string_to_look_up, array):
        for i in range(len(array)):
            if string_to_look_up == array[i]:
                return i

    @staticmethod
    def contains_string_array(string_array, array):
        # check if the the string_array exist in the array (array of string_array)
        for i in range(len(array)):
            if len(string_array) != len(array[i]):
                continue

            matched = True
            for j in range(len(array[i])):
                if string_array[j] != array[i][j]:
                    matched = False
                    break

            if matched:
                return True

        return False
