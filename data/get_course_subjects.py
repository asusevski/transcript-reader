import os


def get_course_subjects(path: str) -> None:
    """
    Given text from course selection offerings page, returns a list of all the unique course subjects.

    Args:
        path: path to the file containing course selection offerings page text.

    Effects:
        Writes unique course subjects to file.
    """
    courses = set()
    with open(path) as f:
        course_subjects = f.read().splitlines()
    for course_subject in course_subjects:
        courses.add(course_subject.split('\t')[0])
    
    with open(os.path.join(os.path.dirname(os.path.abspath(path)), 'course_subjects.txt'), 'w') as f:
        for course in courses:
            if not course:
                continue
            f.write(course.lower() + '\n')
