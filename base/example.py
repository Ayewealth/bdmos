from .models import Result

# Assuming you have a student object (e.g., student_id) for which you want to retrieve the result
student_id = 1  # Replace with the actual student ID

# Retrieve the result object for the student
result = Result.objects.filter(student_id=student_id).first()

# Now you have the result object, you can access its related SubjectResult objects
if result:
    # Get all SubjectResult objects related to this result
    subject_results = result.subjectresult_set.all()
    # Now you can iterate over subject_results and access the scores for each subject
    for subject_result in subject_results:
        print(f"Subject: {subject_result.subject.name}")
        print(f"C.A. Score: {subject_result.total_ca}")
        print(f"Exam Score: {subject_result.exam}")
        print(f"Total Score: {subject_result.total}")
        print(f"Grade: {subject_result.grade}")
        print(f"Position: {subject_result.position}")
        print("-------------")
else:
    print("No result found for the student.")
