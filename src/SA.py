import builtins
from Workstation import Workstation, generate_workstation, algo
from numpy import random
import math
from copy import deepcopy
from colors import bcolors


def run_sequence(sequence: list, routing: list, WS1, WS2, WS3, machine_algo, worker_algo) -> int:
    for i in sequence:
        init = 0
        for j in routing[i-1]:
            # print(i, j, init)
            if (j == 1):
                [s, e] = WS1.use_on_algo(
                    i, init, machine_algo) if WS1.type == 0 else WS1.use_on_algo(i, init, worker_algo)
                init = e
            elif (j == 2):
                [s, e] = WS2.use_on_algo(
                    i, init, machine_algo) if WS2.type == 0 else WS2.use_on_algo(i, init, worker_algo)
                init = e
            elif (j == 3):
                [s, e] = WS3.use_on_algo(
                    i, init, machine_algo) if WS3.type == 0 else WS3.use_on_algo(i, init, worker_algo)
                init = e

    # WS1.show_workspace()
    # WS2.show_workspace()
    # WS3.show_workspace()
    # WS3.visualize_workspace(100)
    # WS2.visualize_workspace(100)
    # WS1.visualize_workspace(100)

    # returns makespan
    end1 = (WS1.get_last_end_duration())
    end2 = (WS2.get_last_end_duration())
    end3 = (WS3.get_last_end_duration())

    return max(end1, end2, end3)


def start(T0: int, M: int, alpha: float, N: int, machine_algorithm: algo, worker_algorithm: algo, show: str = "N"):

    sequence = [1, 2, 3, 4, 5, 6]
    min_sequence = sequence
    T = T0

    init_makespan = run_sequence(sequence, routing, WS1, WS2,
                                 WS3, machine_algorithm, worker_algorithm)
    # Brought out from run_sequence function to also show the state of the workstations at minimal makespan
    WS1.reset()
    WS2.reset()
    WS3.reset()

    print("initial makespan:", init_makespan, "\ninitial sequence:", sequence)
    min_makespan = init_makespan

    m = T0
    while m > M:
        for n in range(N):
            #  random swap a job
            success = False
            while not success:
                # Pick a number
                idx_1 = random.randint(100) % len(sequence)
                idx_2 = random.randint(100) % len(sequence)
                if (idx_1 != idx_2):
                    success = True
                    print(sequence, end=" -> ")
                    temp = sequence[idx_1]
                    sequence[idx_1] = sequence[idx_2]
                    sequence[idx_2] = temp
                    print(
                        sequence, f"swapped index {idx_1} with index {idx_2}")

            makespan = run_sequence(
                sequence, routing, WS1, WS2, WS3, machine_algorithm, worker_algorithm)
            # print(sequence, makespan)
            deltaE = makespan - min_makespan
            if (deltaE < 0):
                min_makespan = makespan
                min_sequence = sequence
                min_ws1 = deepcopy(WS1)
                min_ws2 = deepcopy(WS2)
                min_ws3 = deepcopy(WS3)
            else:
                p = math.e**(((-1) * deltaE)/m)
                r = random.randint(100)/100
                if (p > r):
                    min_makespan = makespan
                    min_sequence = sequence
                    min_ws1 = deepcopy(WS1)
                    min_ws2 = deepcopy(WS2)
                    min_ws3 = deepcopy(WS3)
            WS1.reset()
            WS2.reset()
            WS3.reset()

        m = alpha * m
    print("min makespan:", min_makespan, "\nmin sequence:", min_sequence)
    # show = builtins.input("show workstation status? (Y/N) : ")
    if show == "Y" or show == "y":
        print(bcolors.OKGREEN + bcolors.BOLD +
              "\n======================== Workstation Status ========================\n" + bcolors.ENDC)
        min_ws1.show_workspace()
        min_ws2.show_workspace()
        min_ws3.show_workspace()
        min_ws3.visualize_workspace(min_makespan)
        min_ws2.visualize_workspace(min_makespan)
        min_ws1.visualize_workspace(min_makespan)
        print("")
    return min_makespan, min_sequence


# algo 1 : Random, 2 : Weight, 3: Smaller number

# show = "Y" would show the workstations status at the min makespan
# a, b = start(500, 400, 0.9, 2, machine_algorithm=algo(3),
#              worker_algorithm=algo(1), show="Y")
n_WS1 = int(builtins.input("Masukkan jumlah workspace pada WS1: "))
n_WS2 = int(builtins.input("Masukkan jumlah workspace pada WS2: "))
n_WS3 = int(builtins.input("Masukkan jumlah workspace pada WS3: "))
n_jobs = int(builtins.input("Masukkan jumlah job: "))
t1 = int(builtins.input("Masukkan tipe WS1 (0: Mesin, 1: Pekerja): "))
t2 = int(builtins.input("Masukkan tipe WS2 (0: Mesin, 1: Pekerja): "))
t3 = int(builtins.input("Masukkan tipe WS3 (0: Mesin, 1: Pekerja): "))


WS1, WS2, WS3, routing = generate_workstation(
    n_WS1, n_WS2, n_WS3, n_jobs, t1, t2, t3)

T0 = int(builtins.input("T0: "))
M = int(builtins.input("M: "))
alpha = float(builtins.input("alpha: "))
N = int(builtins.input("N: "))
show = builtins.input("show: ")

print(bcolors.FAIL + bcolors.BOLD +
      "\nMachine : random, worker: random\n" + bcolors.ENDC)
a1, b1 = start(T0, M, alpha, N, machine_algorithm=algo(1),
               worker_algorithm=algo(1), show=show)
print(bcolors.FAIL + bcolors.BOLD +
      "\nMachine : random, worker: weight\n" + bcolors.ENDC)
a2, b2 = start(T0, M, alpha, N, machine_algorithm=algo(1),
               worker_algorithm=algo(2), show=show)
print(bcolors.FAIL + bcolors.BOLD +
      "\nMachine : weight, worker: random\n" + bcolors.ENDC)
a3, b3 = start(T0, M, alpha, N, machine_algorithm=algo(2),
               worker_algorithm=algo(1), show=show)
print(bcolors.FAIL + bcolors.BOLD +
      "\nMachine : weight, worker: weight\n" + bcolors.ENDC)
a4, b4 = start(T0, M, alpha, N, machine_algorithm=algo(2),
               worker_algorithm=algo(2), show=show)
print(bcolors.FAIL + bcolors.BOLD +
      "\nMachine : smaller, worker: random\n" + bcolors.ENDC)
a5, b5 = start(T0, M, alpha, N, machine_algorithm=algo(3),
               worker_algorithm=algo(1), show=show)
print(bcolors.FAIL + bcolors.BOLD +
      "\nMachine : smaller, worker: weight\n" + bcolors.ENDC)
a6, b6 = start(T0, M, alpha, N, machine_algorithm=algo(3),
               worker_algorithm=algo(2), show=show)
