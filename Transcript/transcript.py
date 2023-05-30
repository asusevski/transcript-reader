from dataclasses import dataclass
import os
import pdfplumber
import re


PATH_TO_COURSE_SUBJECTS = "./data/course_subjects.txt"


@dataclass
class Transcript:
    """
    Transcript class

    This class is used to parse a transcript. It is initialized and searches for a file named SSR_TSRPT.
    The transcript is parsed and the grades are returned as a dictionary with get_grades method.

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

    def get_grades(self, courses, lower, upper) -> dict:
        """
        Get grades from transcript text.

        Args:
            courses: list of courses to search for.
            lower: lower bound of course number.
            upper: upper bound of course number.

        Returns:
            grades: dictionary of grades with the course subject as key and the grades received as a value
        """
        rows = self.text.lower().split('\n')
        
        with open(PATH_TO_COURSE_SUBJECTS) as f:
            all_course_subjects = f.read().splitlines()
        
        if not courses:
            courses = all_course_subjects

        grades = {}
        for course_subject in courses:
            # course regex matches course subject and at least one space after the course subject
            course_regex = re.compile(r'^' + course_subject + r'\s(.*)[0-9]{2}$')
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
