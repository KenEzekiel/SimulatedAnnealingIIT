from numpy import random
from input import generate_list_of_jobs


class Workstation:
    # Number of total workspaces in the workstation
    # Workstation numbering starts from 0
    num_total: int = 0
    # list of job duration done in workspaces, starts at 0 but sheets start from 1, so -1 every access
    list_jobs: list = []
    # Type 0 is machine, 1 is people
    type: int = 0
    # matrix with n row = n workspaces, filled with [x,y] with x start busy duration and y end busy duration
    busy_duration: list = []

    def __init__(self, num: int, jobs: list, type: int):
        self.num_total = num
        self.list_jobs = jobs
        self.type = type
        self.busy_duration = [[] for i in range(self.num_total)]

    # Use one Workstation for a job
    def use_ws(self, no_job: int, w_number: int, start: int):
        end = start + self.list_jobs[no_job-1]
        if (self.is_avail_at_time(w_number, start, end)):
            self.busy_duration[w_number].append([start, end])

    # Check if the Workstation is available at a time
    def is_avail_at_time(self, w_number: int, start: int, end: int) -> bool:
        not_busy = False
        count = 0
        # start time is not included in all busy time
        for i in self.busy_duration[w_number]:
            if (start < i[0] and end < i[0]) or start > i[1]:
                count += 1
        if count == len(self.busy_duration[w_number]):
            not_busy = True
        return not_busy

    # Count all available workspaces
    def count_available(self, start: int, no_job: int):
        count_avail = 0
        for i in range(self.num_total):
            end = start + self.list_jobs[no_job-1]
            if (self.is_avail_at_time(i, start, end)):
                count_avail += 1
        return count_avail

    # Get total of busy duration
    def get_total_busy_duration(self, w_number: int) -> int:
        ret = 0
        for i in self.busy_duration[w_number]:
            ret += i[1] - i[0]
        return ret

    # Abstraction of use_ws with random ws selection if available > 1 ws
    def use_random(self, no_job: int, start: int):
        count_avail = self.count_available(start, no_job)
        if (count_avail > 1):
            # pick random number between 0 and self.num_total which is available
            success = False
            while not success:
                num = random.randint(100) % self.num_total
                if self.is_avail_at_time(num, start, start + self.list_jobs[no_job-1]):
                    success = True
            # num is the chosen workspace
            self.use_ws(no_job, num, start)
        elif (count_avail == 1):
            # Get the available one
            for i in range(self.num_total):
                end = start + self.list_jobs[no_job-1]
                if (self.is_avail_at_time(i, start, end)):
                    num = i
            self.use_ws(no_job, num, start)
        else:
            # No ws available currently, get the ws with fastest availability
            min_idx = 0
            min = self.busy_duration[0][len(self.busy_duration[0])-1][1]
            for i in range(self.num_total):
                if self.busy_duration[i][len(self.busy_duration[i])-1][1] < min:
                    min = self.busy_duration[i][len(
                        self.busy_duration[i])-1][1]
                    min_idx = i
            # min_idx is the chosen workspace
            self.use_ws(no_job, min_idx, min+1)

    # Abstraction of use_ws with small ws selection if available > 1 ws

    def use_small(self, no_job: int, start: int):
        count_avail = self.count_available(start, no_job)
        if (count_avail > 1):
            for i in range(self.num_total):
                end = start + self.list_jobs[no_job-1]
                if (self.is_avail_at_time(i, start, end)):
                    num = i
                    break
            # num is the chosen workspace
            self.use_ws(no_job, num, start)
        elif (count_avail == 1):
            # Get the available one
            for i in range(self.num_total):
                end = start + self.list_jobs[no_job-1]
                if (self.is_avail_at_time(i, start, end)):
                    num = i
            self.use_ws(no_job, num, start)
        else:

            # No ws available currently, get the ws with fastest availability
            min_idx = 0
            min = self.busy_duration[0][len(self.busy_duration[0])-1][1]
            for i in range(self.num_total):
                if self.busy_duration[i][len(self.busy_duration[i])-1][1] < min:
                    min = self.busy_duration[i][len(
                        self.busy_duration[i])-1][1]
                    min_idx = i
            # min_idx is the chosen workspace
            self.use_ws(no_job, min_idx, min+1)

    # Abstraction of use_ws with lesser weight ws selection if available > 1 ws
    def use_lesser(self, no_job: int, start: int):
        count_avail = self.count_available(start, no_job)
        if (count_avail > 1):
            # calculate weight then get the smallest weight
            total_duration = []
            total = 0
            for i in range(self.num_total):
                total_duration.append(self.get_total_busy_duration(i))
                total += total_duration[i]
            weight = [[i, total_duration[i]/total]
                      for i in range(len(total_duration))]
            # print("weight:", weight)
            # num is the chosen workspace
            i = 0
            num = weight[i][0]
            while not self.is_avail_at_time(num, start, start + self.list_jobs[no_job-1]):
                i += 1
                num = weight[i][0]
            self.use_ws(no_job, num, start)
        elif (count_avail == 1):
            # Get the available one
            for i in range(self.num_total):
                end = start + self.list_jobs[no_job-1]
                if (self.is_avail_at_time(i, start, end)):
                    num = i
            self.use_ws(no_job, num, start)
        else:
            # No ws available currently, get the ws with fastest availability
            min_idx = 0
            min = self.busy_duration[0][len(self.busy_duration[0])-1][1]
            for i in range(self.num_total):
                if self.busy_duration[i][len(self.busy_duration[i])-1][1] < min:
                    min = self.busy_duration[i][len(
                        self.busy_duration[i])-1][1]
                    min_idx = i
            # min_idx is the chosen workspace
            self.use_ws(no_job, min_idx, min+1)


def generate_workstation(num_WS1: int, num_WS2: int, num_WS3: int, num_jobs: int, t1: int, t2: int, t3: int) -> Workstation:
    n_WS1 = num_WS1
    n_WS2 = num_WS2
    n_WS3 = num_WS3
    n_jobs = num_jobs
    job_WS1, job_WS2, job_WS3 = generate_list_of_jobs(
        n_WS1, n_WS2, n_WS3, n_jobs)

    # Create a Workstation Object
    WS1 = Workstation(num_WS1, job_WS1, t1)
    WS2 = Workstation(num_WS2, job_WS2, t2)
    WS3 = Workstation(num_WS3, job_WS3, t3)

    return WS1, WS2, WS3


WS1, WS2, WS3 = generate_workstation(1, 2, 3, 6, 0, 0, 0)
WS1.use_random(1, 0)
print(WS1.busy_duration)
WS2.use_random(1, 0)
WS2.use_random(2, 0)
WS2.use_random(3, 11)
print(WS2.busy_duration)
# print(WS2.get_total_busy_duration(0), WS2.get_total_busy_duration(1))
WS3.use_small(1, 0)
WS3.use_small(2, 0)
WS3.use_small(3, 0)
WS3.use_lesser(4, 17)
print(WS3.busy_duration)
