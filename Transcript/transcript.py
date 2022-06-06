from dataclasses import dataclass
import os
import pdfplumber
import re


PATH_TO_COURSE_SUBJECTS = "./data/course_subjects.txt"


@dataclass
class Transcript:
    """
    Transcript class
    """
    path: str
    text: str

    def __init__(self) -> None:
        transcript_regex = re.compile(r'.*SSR_TSRPT.pdf$')
        path = "."
        files = []
        for r, _, f in os.walk(path):
            for file in f:
                files.append(os.path.join(r, file))
        matches = list(filter(lambda x: transcript_regex.match(x), files))
        if len(matches) == 0:
            self.path = None
            self.text = None
            return
        elif len(matches) == 1:
            self.path = matches[0]
        else:
            print("Multiple transcripts found. Please select one from the following list and delete the rest:")
            for i, match in enumerate(matches):
                print(f"{i+1}: {match}")
            self.path = None
            self.text = None
            return

        txt = ""
        with pdfplumber.open(self.path) as pdf:
            for page in pdf.pages:
                txt += page.extract_text()
            self.text = txt

    def get_grades(self, courses: list[str], lower: int, upper: int) -> dict:
        rows = self.text.lower().split('\n')

        # Loop through each course in course_subjects
        with open(PATH_TO_COURSE_SUBJECTS) as f:
            all_course_subjects = f.read().splitlines()
        
        if not courses:
            courses = all_course_subjects

        #grades = {course_subject: [] for course_subject in courses}
        grades = {}
        for course_subject in courses:
            course_regex = re.compile(r'^' + course_subject + r'(.*)[0-9]{2}$')
            rows_filtered = list(filter(lambda x: course_regex.match(x.lower()), rows))
            # rows filtered only has a non-empty list if the course exists on the transcript.
            if rows_filtered:
                for row in rows_filtered:
                    course_num = int(row.split()[1])
                    if course_num >= lower and course_num <= upper:
                        if course_subject not in grades:
                            grades[course_subject] = [int(row.split()[-1])]
                            continue
                        grades[course_subject].append(int(row.split()[-1]))
        return grades

    def get_average_grade_of_subject(self, subject: str) -> float:
        rows = self.text.lower().split('\n')
        course_regex = re.compile(r'^' + course_subject + r'(.*)[0-9]{2}$')
        rows_filtered = list(filter(lambda x: course_regex.match(x), rows))
        if len(rows_filtered) == 0:
            print("No course found.")
            return
        grades = [int(row[-2:]) for row in rows_filtered]
        return sum(grades) / len(grades)

    def get_average_grade_course_numbers(self, course_lower: int, course_upper: int) -> float:
        rows = self.text.lower().split('\n')

        # Loop through each course in course_subjects
        with open(PATH_TO_COURSE_SUBJECTS) as f:
            course_subjects = f.read().splitlines()
        
        s = 0
        c = 0
        for course_subject in course_subjects:
            course_regex = re.compile(r'^' + course_subject + r'(.*)[0-9]{2}$')
            rows_filtered = list(filter(lambda x: course_regex.match(x.lower()), rows))
            # rows filtered only has a non-empty list if the course exists on the transcript.
            if rows_filtered:
                for row in rows_filtered:
                    course_num = int(row.split()[1])
                    if course_num >= course_lower and course_num <= course_upper:
                        s += int(row.split()[-1])
                        c += 1
        return s / c
                #print(rows_filtered)
                #print(rows_filtered[0].split()[1])
                                                    #                     and \
                                                    # x.split()[1] >= course_lower and \
                                                    # x.split()[1] <= course_upper, rows))
        #for course_subject in course_subjects:

        # regex to find all rows with course numbers larger than course_lower and less than course_upper
        #print(rows)
        # course_regex = re.compile(r'(.*)[0-9]{3}(.*)[0-9]{2}$')
        # #course_regex = re.compile(r'^' + course_subject + r' (.*)[0-9]{2}$')
        # rows_filtered = list(filter(lambda x: course_regex.match(x), rows))
        # if len(rows_filtered) == 0:
        #     print("No course found.")
        #     return
        # print(rows_filtered)
        #grades = [int(row[-2:]) for row in rows_filtered]
        #return sum(grades) / len(grades)
