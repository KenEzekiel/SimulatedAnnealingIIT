class Workstation:
    num_total: int = 0
    num_available: int = 0
    list_jobs: list = []

    def __init__(self, num: int, jobs: list):
        self.num_total = num
        self.num_available = num
        self.list_jobs = jobs

    # Use one Workstation for a job
    def use_ws(self, no_job: int) -> int:
        if (self.is_avail()):
            self.num_available -= 1
            return self.list_jobs[no_job-1]
        return 0

    # Check if the workstation is available
    def is_avail(self) -> bool:
        return self.num_available > 0


def generate_workstation(num_WS1: int, num_WS2: int, num_WS3: int, num_jobs: int) -> Workstation:
    n_WS1 = num_WS1
    n_WS2 = num_WS2
    n_WS3 = num_WS3
    n_jobs = num_jobs
    job_WS1, job_WS2, job_WS3 = input.generate_list_of_jobs(
        n_WS1, n_WS2, n_WS3, n_jobs)

    # Create a Workstation Object
    WS1 = Workstation(num_WS1, job_WS1)
    WS2 = Workstation(num_WS2, job_WS2)
    WS3 = Workstation(num_WS3, job_WS3)

    return WS1, WS2, WS3
