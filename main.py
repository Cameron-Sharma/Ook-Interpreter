SIZE = 2**10
CMD_LENGTH = len("Ook_ Ook_")

memory = [0 for _ in range(int(SIZE))]
ptr = 0
program_input = ""


def evaluate_char(i, program, open_indices, skip_loop):
    global SIZE, memory, ptr

    if program[i:i+CMD_LENGTH] == "Ook! Ook?":
        open_indices.append(i)

        if skip_loop:
            return i + CMD_LENGTH, open_indices, skip_loop

        if memory[ptr] == 0:
            return i+CMD_LENGTH, open_indices, len(open_indices)

        return i+CMD_LENGTH, open_indices, 0

    if program[i:i+CMD_LENGTH] == "Ook? Ook!":
        matching_open_index = open_indices[-1]
        open_indices = open_indices[:-1]

        if skip_loop or memory[ptr] == 0:
            if len(open_indices) < skip_loop:
                return i+CMD_LENGTH, open_indices, 0

            return i+CMD_LENGTH, open_indices, skip_loop

        return matching_open_index, open_indices, 0

    if skip_loop:
        if (program[i:i+CMD_LENGTH] in
                ("Ook. Ook.", "Ook! Ook!", "Ook. Ook?", "Ook? Ook.", "Ook. Ook!", "Ook! Ook.", "Ook? Ook?")):
            return i+CMD_LENGTH, open_indices, skip_loop

        return i+1, open_indices, skip_loop

    if program[i:i+CMD_LENGTH] == "Ook. Ook.":
        memory[ptr] += 1
        memory[ptr] %= 256
        return i+CMD_LENGTH, open_indices, skip_loop

    if program[i:i+CMD_LENGTH] == "Ook! Ook!":
        memory[ptr] -= 1
        memory[ptr] %= 256
        return i+CMD_LENGTH, open_indices, skip_loop

    if program[i:i+CMD_LENGTH] == "Ook. Ook?":
        ptr += 1
        ptr %= SIZE
        return i+CMD_LENGTH, open_indices, skip_loop

    if program[i:i+CMD_LENGTH] == "Ook? Ook.":
        ptr -= 1
        ptr %= SIZE
        return i+CMD_LENGTH, open_indices, skip_loop

    if program[i:i+CMD_LENGTH] == "Ook. Ook!":
        global program_input

        if program_input == "":
            memory[ptr] = 0
        else:
            memory[ptr] = ord(program_input[0])
            program_input = program_input[1:]

        return i+CMD_LENGTH, open_indices, skip_loop

    if program[i:i+CMD_LENGTH] == "Ook! Ook.":
        print(chr(memory[ptr]), end="")
        return i+CMD_LENGTH, open_indices, skip_loop

    if program[i:i + CMD_LENGTH] == "Ook? Ook?":
        # Give the memory pointer a banana
        return i+CMD_LENGTH, open_indices, skip_loop

    return i+1, open_indices, skip_loop


def main():
    import sys

    filename = sys.argv[1]
    global program_input
    program_input = sys.argv[2]

    fh = open(filename, "r")
    program = fh.read()
    fh.close()

    i = 0
    open_indices = []
    skip_loop = 0

    while i < len(program):
        i, open_indices, skip_loop = evaluate_char(i, program, open_indices, skip_loop)


if __name__ == "__main__":
    main()
