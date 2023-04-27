# Using openpyxl library to read from the file
import openpyxl

workbook = openpyxl.load_workbook("../data/DATA.xlsx")

# Define variable to read the active sheet:
ws = workbook.active


def print_active_ws():
    # Iterate the loop to read the cell values
    for i in range(0, ws.max_row):
        for col in ws.iter_cols(1, ws.max_column):
            if i == 0:
                string = "" if col[i].value == "None" else col[i].value
                print(string, end="\t")
            else:
                print(col[i].value, end="\t")
        print('')


n_WS1 = 3
n_WS2 = 2
n_WS3 = 12
n_job = 20

start_WS1 = ["B", 3]
start_WS2 = [chr(ord(start_WS1[0]) + n_WS1), 3]
start_WS3 = [chr(ord(start_WS2[0]) + n_WS2), 3]

print(start_WS1)
print(start_WS2)
print(start_WS3)

job_WS1 = []
job_WS2 = []
job_WS3 = []


def get_jobs(job_WS, start_WS, n_job):
    all_num = []
    for i in range(n_job):
        all_num.append(str(start_WS[1] + i))
    print(all_num)
    all_cell = []
    for i in range(n_job):
        all_cell.append([start_WS[0], all_num[i]])
    print(all_cell)
    all_string = ["".join(x) for x in all_cell]
    print(all_string)


get_jobs(job_WS1, start_WS1, n_job)
