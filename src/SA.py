import builtins
from Workstation import Workstation, generate_workstation, algo
from numpy import random
import math
from copy import deepcopy
from colors import bcolors
from JobRouting import JobRouting


def run_sequence(sequence: list, routing: list, WS1, WS2, WS3, machine_algo, worker_algo) -> int:
    listjobs = []
    for i in sequence:
        init = 0
        job = JobRouting(i, routing[i-1])
        for j in routing[i-1]:
            # print(i, j, init)
            if (j == 1):
                [s, e], w_num = WS1.use_on_algo(
                    i, init, machine_algo) if WS1.type == 0 else WS1.use_on_algo(i, init, worker_algo)
                init = e
                job.set_WS_num(1, w_num+1)
            elif (j == 2):
                [s, e], w_num = WS2.use_on_algo(
                    i, init, machine_algo) if WS2.type == 0 else WS2.use_on_algo(i, init, worker_algo)
                init = e
                job.set_WS_num(2, w_num+1)
            elif (j == 3):
                [s, e], w_num = WS3.use_on_algo(
                    i, init, machine_algo) if WS3.type == 0 else WS3.use_on_algo(i, init, worker_algo)
                init = e
                job.set_WS_num(3, w_num+1)
        listjobs.append(job)

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

    return max(end1, end2, end3), listjobs


def start(T0: float, M: float, alpha: float, N: int, machine_algorithm: algo, worker_algorithm: algo, show: str = "N", start_sequence: list = []):

    sequence = deepcopy(start_sequence)
    min_sequence = deepcopy(sequence)
    T = T0

    init_makespan, init_listjobs = run_sequence(sequence, routing, WS1, WS2,
                                                WS3, machine_algorithm, worker_algorithm)
    init_makespan = round(init_makespan, 3)
    # Brought out from run_sequence function to also show the state of the workstations at minimal makespan
    WS1.reset()
    WS2.reset()
    WS3.reset()

    print("initial makespan:", init_makespan, "\ninitial sequence:", sequence)
    for i in init_listjobs:
        i.print()
    min_makespan = init_makespan
    min_listjobs = init_listjobs

    m = T0
    solution_avail = False
    while m > M:
        print("m:", m)
        for n in range(N):
            acc = False
            prev_sequence = deepcopy(sequence)
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

            makespan, listjobs = run_sequence(
                sequence, routing, WS1, WS2, WS3, machine_algorithm, worker_algorithm)
            makespan = round(makespan, 3)
            # print("sequence makespan", sequence, makespan)
            deltaE = makespan - min_makespan
            if (deltaE < 0):
                acc = True
                solution_avail = True
                min_makespan = deepcopy(makespan)
                min_sequence = deepcopy(sequence)
                min_listjobs = deepcopy(listjobs)
                min_ws1 = deepcopy(WS1)
                min_ws2 = deepcopy(WS2)
                min_ws3 = deepcopy(WS3)
            else:
                p = math.e**(((-1) * deltaE)/m)
                r = random.randint(100)/100
                if (p > r):
                    acc = True
                    # min_makespan = makespan
                    # min_sequence = sequence
                    # min_listjobs = listjobs
                    # min_ws1 = deepcopy(WS1)
                    # min_ws2 = deepcopy(WS2)
                    # min_ws3 = deepcopy(WS3)
            if not acc:
                sequence = deepcopy(prev_sequence)
                print("Solution not accepted, reverting to previous sequence", sequence)
            WS1.reset()
            WS2.reset()
            WS3.reset()

        m = alpha * m
    print("min makespan:", min_makespan, "\nmin sequence:", min_sequence)
    for i in min_listjobs:
        i.print()
    # show = builtins.input("show workstation status? (Y/N) : ")
    if (show == "Y" or show == "y") and solution_avail:
        print(bcolors.OKGREEN + bcolors.BOLD +
              "\n======================== Workstation Status ========================\n" + bcolors.ENDC)
        min_ws1.show_workspace()
        min_ws2.show_workspace()
        min_ws3.show_workspace()
        min_ws3.visualize_workspace(min_makespan)
        min_ws2.visualize_workspace(min_makespan)
        min_ws1.visualize_workspace(min_makespan)
        print("")
    if not solution_avail:
        print(bcolors.WARNING + bcolors.BOLD + "\nNo solution chosen\n" + bcolors.ENDC)
    return min_makespan, min_sequence, min_listjobs


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

T0 = float(builtins.input("T0: "))
M = float(builtins.input("M: "))
alpha = float(builtins.input("alpha: "))
N = int(builtins.input("N: "))
show = builtins.input("show: ")

sequence = [1, 2, 3, 4, 5, 6]
random.shuffle(sequence)

print(bcolors.FAIL + bcolors.BOLD +
      "\nMachine : random, worker: random\n" + bcolors.ENDC)
a1, b1, c1 = start(T0, M, alpha, N, machine_algorithm=algo(1),
                   worker_algorithm=algo(1), show=show, start_sequence=sequence)
print(bcolors.FAIL + bcolors.BOLD +
      "\nMachine : random, worker: weight\n" + bcolors.ENDC)
a2, b2, c2 = start(T0, M, alpha, N, machine_algorithm=algo(1),
                   worker_algorithm=algo(2), show=show, start_sequence=sequence)
print(bcolors.FAIL + bcolors.BOLD +
      "\nMachine : weight, worker: random\n" + bcolors.ENDC)
a3, b3, c3 = start(T0, M, alpha, N, machine_algorithm=algo(2),
                   worker_algorithm=algo(1), show=show, start_sequence=sequence)
print(bcolors.FAIL + bcolors.BOLD +
      "\nMachine : weight, worker: weight\n" + bcolors.ENDC)
a4, b4, c4 = start(T0, M, alpha, N, machine_algorithm=algo(2),
                   worker_algorithm=algo(2), show=show, start_sequence=sequence)
print(bcolors.FAIL + bcolors.BOLD +
      "\nMachine : smaller, worker: random\n" + bcolors.ENDC)
a5, b5, c5 = start(T0, M, alpha, N, machine_algorithm=algo(3),
                   worker_algorithm=algo(1), show=show, start_sequence=sequence)
print(bcolors.FAIL + bcolors.BOLD +
      "\nMachine : smaller, worker: weight\n" + bcolors.ENDC)
a6, b6, c6 = start(T0, M, alpha, N, machine_algorithm=algo(3),
                   worker_algorithm=algo(2), show=show, start_sequence=sequence)

list_result = [a1, a2, a3, a4, a5, a6]

min_idx = 0
min_val = a1
for i in range(1, len(list_result)):
    if (list_result[i] < min_val):
        min_idx = i
        min_val = list_result[i]

if (min_idx == 0):
    print("\nConclusion: minimum on machine: random and worker: random")
    print(f"Minimum makespan: {a1}")
    print(f"Minimum sequence: {b1}")
    print("list of job routing:")
    for i in c1:
        i.print()

elif (min_idx == 1):
    print("\nConclusion: minimum on machine: random and worker: weight")
    print(f"Minimum makespan: {a2}")
    print(f"Minimum sequence: {b2}")
    print("list of job routing:")
    for i in c2:
        i.print()

elif (min_idx == 2):
    print("\nConclusion: minimum on machine: weight and worker: random")
    print(f"Minimum makespan: {a3}")
    print(f"Minimum sequence: {b3}")
    print("list of job routing:")
    for i in c3:
        i.print()

elif (min_idx == 3):
    print("\nConclusion: minimum on machine: weight and worker: weight")
    print(f"Minimum makespan: {a4}")
    print(f"Minimum sequence: {b4}")
    print("list of job routing:")
    for i in c4:
        i.print()

elif (min_idx == 4):
    print("\nConclusion: minimum on machine: smaller and worker: random")
    print(f"Minimum makespan: {a5}")
    print(f"Minimum sequence: {b5}")
    print("list of job routing:")
    for i in c5:
        i.print()

elif (min_idx == 5):
    print("\nConclusion: minimum on machine: smaller and worker: weight")
    print(f"Minimum makespan: {a6}")
    print(f"Minimum sequence: {b6}")
    print("list of job routing:")
    for i in c6:
        i.print()
