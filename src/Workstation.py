class Workstation:
    num_total: int = 0
    # 1 is available, 0 is unavailable
    num_available: list = []
    list_jobs: list = []
    # Type 0 is machine, 1 is people
    type: int = 0

    def __init__(self, num: int, jobs: list, type: int):
        self.num_total = num
        self.num_available = [1 for i in range(num)]
        self.list_jobs = jobs
        self.type = type

    # Use one Workstation for a job
    def use_ws(self, no_job: int, no_machine: int) -> int:
        if (self.is_avail(no_machine)):
            self.num_available[no_machine] = 0
            return self.list_jobs[no_job-1]
        return -1

    # Free up the Workstation
    def free_ws(self, no_machine: int):
        self.num_available[no_machine] = 1

    # Check if the Workstation is available
    def is_avail(self, no_machine: int) -> bool:
        return self.num_available[no_machine] == 1


def generate_workstation(num_WS1: int, num_WS2: int, num_WS3: int, num_jobs: int, t1: int, t2: int, t3: int) -> Workstation:
    n_WS1 = num_WS1
    n_WS2 = num_WS2
    n_WS3 = num_WS3
    n_jobs = num_jobs
    job_WS1, job_WS2, job_WS3 = input.generate_list_of_jobs(
        n_WS1, n_WS2, n_WS3, n_jobs)

    # Create a Workstation Object
    WS1 = Workstation(num_WS1, job_WS1, t1)
    WS2 = Workstation(num_WS2, job_WS2, t2)
    WS3 = Workstation(num_WS3, job_WS3, t3)

    return WS1, WS2, WS3
