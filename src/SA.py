import input
from Workstation import Workstation, generate_workstation


def run_sequence(sequence: list, routing: list, WS1, WS2, WS3) -> int:
    for i in sequence:
        init = 0
        for j in routing[i-1]:
            # print(i, j, init)
            if (j == 1):
                [s, e] = WS1.use_random(i, init)
                init = e
            elif (j == 2):
                [s, e] = WS2.use_small(i, init)
                init = e
            elif (j == 3):
                [s, e] = WS3.use_random(i, init)
                init = e

    WS1.show_workspace()
    WS2.show_workspace()
    WS3.show_workspace()
    # WS3.visualize_workspace(100)
    # WS2.visualize_workspace(100)
    # WS1.visualize_workspace(100)

    # returns makespan
    end1 = (WS1.get_last_end_duration())
    end2 = (WS2.get_last_end_duration())
    end3 = (WS3.get_last_end_duration())

    return max(end1, end2, end3)


def start(T0, M, alpha, N):
    # WS1, WS2, WS3 = generate_workstation(3, 2, 12, 20)
    WS1, WS2, WS3, routing = generate_workstation(1, 2, 3, 6, 0, 0, 0)

    sequence = [1, 2, 3, 4, 5, 6]

    makespan = run_sequence(sequence, routing, WS1, WS2, WS3)
    print(makespan)


start(500, 400, 0.9, 2)
