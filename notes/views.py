from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.views import APIView
from .models import Note
from django.http import Http404
from rest_framework import status
from rest_framework.decorators import api_view
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from users.models import User
from .serializers import NoteSerializer

# Create your views here.
class NotesList(generics.ListCreateAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer

    def get_queryset(self):
        user = self.request.user
        return Note.objects.filter(author=user).order_by("-created_at")

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(author=user)
        return Response(status=status.HTTP_201_CREATED)


class DetailUpdateDeletNote(APIView):
    def get_object(self, pk):
        try:
            return Note.objects.get(pk=pk)
        except Note.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        note = self.get_object(pk)
        serializer = NoteSerializer(note)
        return Response(serializer.data)

    def delete(self, request, pk, format=None):
        note = self.get_object(pk)
        note.delete()
        user = request.user
        notes = Note.objects.filter(author=user).order_by("-created_at")
        serializer = NoteSerializer(data=notes)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.data)


class SearchNote(APIView):
    def get_object(self, pk):
        try:
            return Note.objects.get(pk=pk)
        except Note.DoesNotExist:
            raise Http404

    def get(self, search):
        notes = Note.objects.filter(Q(title=search) | Q(body=search))
        serializer = NoteSerializer(notes, many=True)
        return Response(serializer.data)


@api_view(["GET"])
def search(request, search):
    if request.method == "GET":
        note_by_search = Note.objects.filter(
            Q(title__icontains=search) | Q(body__icontains=search)
        )
        serializer = NoteSerializer(note_by_search, many=True)
        return Response(serializer.data)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)