from django.shortcuts import render


def index(request):
    return "Hello world!"


def create_upload(request):
    return "Create new upload!"


def read_upload(request):
    return "Read existing upload!"
