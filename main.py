import numpy as np
import os
import re
from Transcript.transcript import Transcript


def main() -> None:
    transcript = Transcript()
    if not transcript.path:
        print("No transcript found.")
        return
    
    print("Enter q to quit at any time.")
    while True:
        courses = []
        print("Enter the course subject(s) -- for all subjects, press enter: ")
        while True:
            course = input("> ")
            if not course:
                break
            if course.lower() == "q":
                return
            course = course.lower()
            print(f"You entered: {course}. To stop entering courses, press enter.")
            courses.append(course)
        print("Enter lower bound of course number (ie: to include 3rd year courses and above, enter 300).: ")
        try:
            lower = input("> ")
            if not lower:
                lower = 0
            elif lower.lower() == "q":
                return
            else:
                lower = int(lower)
        except ValueError:
            print("Please enter a number. Exiting.")
            return
        
        print("Enter upper bound of course number (ie: to include up until 4th year courses, enter 499): ")
        try:
            upper = input("> ")
            if not upper:
                # Arbitrary large number, not 499 in case grad classes :)
                upper = 900
            elif upper.lower() == "q":
                return
            else:
                upper = int(upper)
        except ValueError:
            print("Please enter a number. Exiting.")
            return
        
        grades = transcript.get_grades(courses, lower, upper)
        average_grade = np.mean(np.concatenate(list(grades.values())))
        print(f"Average Grade for classes with lower bound {lower} and upper bound {upper}: {average_grade:2.2f}")
        
if __name__ == '__main__':
    main()
 