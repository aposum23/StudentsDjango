from rest_framework import serializers
from students_api.models import Students, Sections, StudentsSections


class StudentsSerialize(serializers.ModelSerializer):
    class Meta:
        model = Students
        fields = '__all__'


class SectionSerialize(serializers.ModelSerializer):
    class Meta:
        model = Sections
        fields = '__all__'


class StudentSectionsReadSerialize(serializers.ModelSerializer):
    section = SectionSerialize()
    student = StudentsSerialize()
    class Meta:
        model = StudentsSections
        fields = '__all__'


class StudentSectionsWriteSerialize(serializers.ModelSerializer):
    class Meta:
        model = StudentsSections
        fields = '__all__'
