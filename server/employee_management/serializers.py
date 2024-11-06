# employee_management/serializers.py
from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import (
    CustomUser,
    Branches,
    Departments,
    Designations,
    DailyWorkReports,
    ApplicationLeave,
)


class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branches
        fields = (
            "id",
            "branch_name",
            "branch_location",
            "branch_contact",
            "branch_email",
        )


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Departments
        fields = ("id", "department_name", "department_status")


class DesignationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Designations
        fields = ("id", "designation_name", "designation_status")


class CustomUserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    profile_picture = serializers.ImageField(required=False)  # Optional profile picture

    class Meta:
        model = CustomUser
        fields = (
            "email",
            "full_name",
            "password",
            "branch",
            "department",
            "designation",
            "profile_picture",
            "salary",
        )

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()

        return user


class CustomUserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")
        user = authenticate(email=email, password=password)
        if user is None:
            raise serializers.ValidationError({"error": "Invalid email or password."})
        data["user"] = user
        return data


class CustomUserSerializer(serializers.ModelSerializer):
    branch = BranchSerializer()
    department = DepartmentSerializer()
    designation = DesignationSerializer()

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "email",
            "full_name",
            "profile_picture",
            "branch",
            "department",
            "designation",
            "date_joined",
        ]


class MinimalUserSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source="department.department_name")
    designation_name = serializers.CharField(source="designation.designation_name")

    class Meta:
        model = CustomUser
        fields = [
            "email",
            "full_name",
            "profile_picture",
            "department_name",
            "designation_name",
        ]


class DailyWorkReportsSerializer(serializers.ModelSerializer):
    user = MinimalUserSerializer(read_only=True)

    class Meta:
        model = DailyWorkReports
        fields = ["id", "user", "work_title", "work_description"]


class ApplicationLeaveSerializer(serializers.ModelSerializer):
    user = MinimalUserSerializer()

    class Meta:
        model = ApplicationLeave
        fields = [
            "id",
            "user",
            "leave_reason",
            "leave_start_date",
            "leave_end_date",
            "leave_status",
        ]
