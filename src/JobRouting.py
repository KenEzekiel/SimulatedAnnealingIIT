class JobRouting:
    job_num: int
    WS1_num: int
    WS2_num: int
    WS3_num: int
    Routing: list

    def __init__(self, job_num: int, Routing: list, WS1_num=0, WS2_num=0, WS3_num=0):
        self.job_num = job_num
        self.WS1_num = WS1_num
        self.WS2_num = WS2_num
        self.WS3_num = WS3_num
        self.Routing = Routing

    def print(self):
        print(str(self.job_num))
        print("Routing: ")
        print(self.Routing)
        if (self.WS1_num != 0):
            print(f"WS1: {self.WS1_num}")
        if (self.WS2_num != 0):
            print(f"WS2: {self.WS2_num}")
        if (self.WS3_num != 0):
            print(f"WS3: {self.WS3_num}")

    def set_WS_num(self, WS: int, num: int):
        if (WS == 1):
            self.WS1_num = num
        elif (WS == 2):
            self.WS2_num = num
        elif (WS == 3):
            self.WS3_num = num


# job = JobRouting(1, [1, 2], 1, 2, 3)

# job.print()
