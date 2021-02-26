from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Book
from .serializers import BookSerializer
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Explicit implementation of list and individual endpoints


class BookList(APIView):

    books_per_page = 2

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
        query = request.query_params.get("keyword")

        if (not query):
            query = ""
        all_books = Book.objects.all()

        filtered_books = Book.objects.filter(
            title__icontains=query).order_by("id")

        rendered_books = filtered_books

        page = request.query_params.get('page')
        paginator = Paginator(rendered_books, self.books_per_page)

        try:
            books_paginated = paginator.page(page)
        except PageNotAnInteger:
            books_paginated = paginator.page(1)
        except EmptyPage:
            books_paginated = paginator.page(paginator.num_pages)

        # When visit the homepage (no query yet)
        if (page == None):
            page = 1

        # serializer = BookSerializer(books, many=True)
        serializer = BookSerializer(books_paginated, many=True)
        return Response({'books': serializer.data, 'pages': paginator.num_pages, 'page': page})


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
