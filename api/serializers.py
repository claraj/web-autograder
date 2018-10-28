from rest_framework import serializers
from .models import Assignment, Student, ProgrammingClass, GradingBatch, Grade, Attributes

class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = '__all__'


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'


class GradingBatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = GradingBatch
        fields = '__all__'


class ProgrammingClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgrammingClass
        fields = '__all__'


class GradeSerializer(serializers.ModelSerializer):

    assignment = AssignmentSerializer()
    student = StudentSerializer()

    class Meta:
        model = Grade
        fields = '__all__'


class AttributesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attributes
        fields = '__all__'
