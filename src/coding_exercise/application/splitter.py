import math
from coding_exercise.domain.model.cable import Cable


class Splitter:

    def __validate(self, cable: Cable, times: int):
        if cable is None:
            raise ValueError("Cable cannot be None")

        if not isinstance(times, int):
            raise ValueError("Cannot split non-integer times")

        if times < 1:
            raise ValueError("Cannot split less than once")

        if times > 64:
            raise ValueError("Cannot split more than 64 times")

        if times > cable.length:
            raise ValueError("Cannot split more times than length of Cable")

    def __compute_lengths(self, cable: Cable, times: int):
        longest_len = cable.length // (times + 1)
        remaining_len = cable.length % (times + 1)

        # padding length
        total_cables = (times + 1) + (remaining_len // longest_len)
        if remaining_len % longest_len != 0:
            total_cables += 1
        padding_len = math.floor(math.log10(total_cables)) + 1

        return longest_len, remaining_len, padding_len

    def split(self, cable: Cable, times: int) -> list[Cable]:
        """
        Splits a cable n times into the longest equal integer length cables possible
        Any remaining cable will be cut into that same length until not possible

        args:
            - cable (Cable): The Cable to split
            - times (int): The number of times to split it

        returns:
            - Cables (list[Cable]): the list of split Cables
        """
        self.__validate(cable, times)

        longest_len, remaining_len, padding_len = self.__compute_lengths(cable, times)

        cables = []

        def make_cable(length=longest_len):
            index = str(len(cables))
            name = f"{cable.name}-{index.rjust(padding_len, '0')}"
            cables.append(Cable(length, name))

        # initial cuts
        for _ in range(times + 1):
            make_cable()

        # cutting remainder into equal lengths
        while remaining_len - longest_len >= 0:
            make_cable()
            remaining_len -= longest_len

        # any remaning
        if remaining_len > 0:
            make_cable(remaining_len)

        return cables
