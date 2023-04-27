# Using openpyxl library to read from the file
import openpyxl


def print_active_worksheet(worksheet):
    # Iterate the loop to read the cell values
    for i in range(0, worksheet.max_row):
        for col in worksheet.iter_cols(1, worksheet.max_column):
            if i == 0:
                string = "" if col[i].value == "None" else col[i].value
                print(string, end="\t")
            else:
                print(col[i].value, end="\t")
        print('')


def generate_list_of_jobs(num_WS1, num_WS2, num_WS3, num_job):
    # workbook = openpyxl.load_workbook("../data/DATA.xlsx")
    workbook = openpyxl.load_workbook("../data/test_data.xlsx")

    # Define variable to read the active sheet:
    ws = workbook.active

    # Number of workspaces in a WS and number of jobs
    n_WS1 = num_WS1
    n_WS2 = num_WS2
    n_WS3 = num_WS3
    n_job = num_job
    start_col = "B"
    start_row = 3

    start_WS1 = [start_col, start_row]
    start_WS2 = [chr(ord(start_WS1[0]) + n_WS1), 3]
    start_WS3 = [chr(ord(start_WS2[0]) + n_WS2), 3]

    # Check all start cells
    # print(start_WS1)
    # print(start_WS2)
    # print(start_WS3)

    job_WS1 = []
    job_WS2 = []
    job_WS3 = []

    def get_jobs(job_WS, start_WS, n_job):
        all_num = []
        all_cell = []
        for i in range(n_job):
            all_num.append(str(start_WS[1] + i))
            all_cell.append([start_WS[0], all_num[i]])
        all_string = ["".join(x) for x in all_cell]
        return all_string

    # Get all job data value from worksheet with all job cells
    job_WS1 = [round(ws[x].value, 2)
               for x in get_jobs(job_WS1, start_WS1, n_job)]
    job_WS2 = [round(ws[x].value, 2)
               for x in get_jobs(job_WS2, start_WS2, n_job)]
    job_WS3 = [round(ws[x].value, 2)
               for x in get_jobs(job_WS3, start_WS3, n_job)]

    print(job_WS1)
    print(job_WS2)
    print(job_WS3)

    return job_WS1, job_WS2, job_WS3
