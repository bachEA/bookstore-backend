from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


from .models import Book
from .serializers import BookSerializer
from rest_framework import generics


# class BookList(generics.ListCreateAPIView):

#     queryset = Book.objects.all()
#     serializer_class = BookSerializer


# class BookDetail(generics.RetrieveUpdateDestroyAPIView):

#     queryset = Book.objects.all()
#     serializer_class = BookSerializer


# Explicit implementation of list and individual endpoints
class BookList(APIView):

    """
        View to list all books in the database
    """

    def post(self, request, format=None):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)


class BookDetail(APIView):
    def get_object(self, pk):
        try:
            return Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        book = self.get_object(pk)
        serializer = BookSerializer(book, many=False)
        return Response(serializer.data)
