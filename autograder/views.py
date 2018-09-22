from django.shortcuts import render
from django.http import JsonResponse, StreamingHttpResponse, HttpResponse


def grader_placeholder(request):
    # return JsonResponse(request.data)
    return HttpResponse('hello')

# Create your views here.
def grade(request):
    if request.method == 'POST':
        # grade the things
        json_data = json.loads(request.body)
        print('the data recd', json_data)

        class GradedAssignments:
            def __init__(self, assignment, students):
                self.student_count = 0
                self.students = students
                self.asgt = assignment
            def __iter__(self):
                return self
            def __next__(self):
                print('iterator sz next')
                if self.student_count >= len(self.students):
                    raise StopIteration

                res = autograder.grade(self.asgt, self.students[self.student_count])
                self.student_count += 1
                return res


        # stream response, cuz it's slow
        streaming_content = GradedAssignments(json_data['assignment'], json_data['students'])

        return StreamingHttpResponse(streaming_content)

    else:
        assignments = Assignment.objects.order_by('week')
        students = Student.objects.order_by('name')
        return render(request, 'autograder/grader.html', { 'students': students, 'assignments': assignments })
