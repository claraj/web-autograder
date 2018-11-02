from rest_framework import serializers
from rest_framework.serializers import PrimaryKeyRelatedField
from .models import Assignment, Student, ProgrammingClass, GradingBatch, Grade

class AssignmentSerializer(serializers.ModelSerializer):
    programming_classes = PrimaryKeyRelatedField(many=True, required=False, queryset=ProgrammingClass.objects.all())
    class Meta:
        model = Assignment
        fields = '__all__'
        extra_kwargs = {'programming_classes': {'required': False, 'allow_empty': True}}


class StudentSerializer(serializers.ModelSerializer):
    programming_classes = PrimaryKeyRelatedField(many=True, required=False, queryset=ProgrammingClass.objects.all())
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
