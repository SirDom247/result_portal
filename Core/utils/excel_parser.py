import pandas as pd
from Core.models import StudentProfile, Course, Result

def process_excel(file_path):
    df = pd.read_excel(file_path)
    results = []
    for _, row in df.iterrows():
        try:
            student = StudentProfile.objects.get(matric_number=row['MatricNumber'])
            course = Course.objects.get(code=row['CourseCode'])
            score = float(row['Score'])
            grade = compute_grade(score)
            result, created = Result.objects.update_or_create(
                student=student,
                course=course,
                defaults={'score': score, 'grade': grade}
            )
            results.append(result)
        except Exception as e:
            print(f"Error processing row {row}: {e}")
    return results

def compute_grade(score):
    if score >= 70:
        return 'A'
    elif score >= 60:
        return 'B'
    elif score >= 50:
        return 'C'
    elif score >= 45:
        return 'D'
    elif score >= 40:
        return 'E'
    else:
        return 'F'

