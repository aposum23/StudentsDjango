from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.response import Response
from students_api.serializers import StudentsSerialize, StudentSectionsReadSerialize, StudentSectionsWriteSerialize, SectionSerialize
from students_api.models import Students, StudentsSections, Sections
from Students.settings import MEDIA_URL as media_path
import os


def get_list_of_students(data):
    student = Students.objects.filter()
    try:
        if data['fio'] != '':
            student = student.filter(name=data['fio'])
        if data['individual'] != 'null' and data['individual'] != '':
            if data['individual'] == 'true':
                student = student.filter(individual=True)
            elif data['individual'] == 'false':
                student = student.filter(individual=False)
        if data['cours'] != '':
            student = student.filter(cours=data['cours'])
        serializer = StudentsSerialize(student, many=True)
        return serializer
    except Exception as e:
        print(e)
        serializer = StudentsSerialize(student, many=True)
        return serializer


@csrf_exempt
@api_view(['POST'])
def filter_students(request):
    if request.method == 'POST':
        students = get_list_of_students(request.data)
        print(students)
        return Response(students.data)


@csrf_exempt
@api_view(['GET', 'POST'])
@parser_classes((MultiPartParser,))
def student_list(request):
    if request.method == 'GET':
        students = Students.objects.all()
        serializer = StudentsSerialize(students, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = StudentsSerialize(data=request.data)
        if serializer.is_valid():
            serializer.save()
            students = get_list_of_students({})
            return Response(students.data)
        students = get_list_of_students({})
        return Response(students.data)


@csrf_exempt
@api_view(['POST'])
@parser_classes((MultiPartParser,))
def student_list_update(request):
    if request.method == 'POST':
        print(request.data)
        student = Students.objects.get(id=request.data['id'])
        print(student)
        try:
            if request.data['name'] == '':
                student.delete()
                return Response('Deleted')
            else:
                student.name = request.data['name']
                student.stud_date = request.data['stud_date']
                student.stud_group = request.data['stud_group']
                student.cours = request.data['cours']
                if request.data['individual'] == 'true':
                    student.individual = True
                else:
                    student.individual = False
                if request.data['photography'] != 'undefined':
                    student.photography = request.data['photography']
                else:
                    student.photography = student.photography
                student.save()
                return Response('Sucessful!!!')
        except Exception as e:
            return Response(e)


@csrf_exempt
@api_view(['GET', 'POST'])
@parser_classes((JSONParser,))
def student_sections_list(request):
    if request.method == 'GET':
        stud_sections = StudentsSections.objects.all()
        serializer = StudentSectionsReadSerialize(stud_sections, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = StudentSectionsWriteSerialize(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors)


@csrf_exempt
def sections_list(request):
    if request.method == 'GET':
        sections = Sections.objects.all()
        serializer = SectionSerialize(sections, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = SectionSerialize(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors)

@csrf_exempt
@api_view(['POST'])
def sort_students(request):
    data = request.data
    if data['method'] == 'fio_up':
        students = Students.objects.order_by('name')
    elif data['method'] == 'fio_down':
        students = Students.objects.order_by('-name')
    elif data['method'] == 'date_up':
        students = Students.objects.order_by('stud_date')
    elif data['method'] == 'date_down':
        students = Students.objects.order_by('-stud_date')
    else:
        students = Students.objects.all()
    serializer = StudentsSerialize(students, many=True)
    return Response(serializer.data)

