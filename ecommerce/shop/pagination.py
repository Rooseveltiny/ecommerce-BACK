from rest_framework.pagination import PageNumberPagination
from collections import OrderedDict
from rest_framework.response import Response
import re


class CatalogProductsPagination(PageNumberPagination):

    page_size = 4
    page_size_query_param = 'page_size'
    max_page_size = 1000
    amplitude = 3

    def get_page_links(self):

        count = self.page.paginator.num_pages
        current_page_number = self.page.number
        start_page = 0
        end_page = 0
        if current_page_number - self.amplitude <= 0:
            start_page = 1
        else:
            start_page = current_page_number - self.amplitude

        if current_page_number + self.amplitude >= count:
            end_page = count
        else:
            end_page = current_page_number + self.amplitude

        current_page_link = self.request.build_absolute_uri()
        if not re.findall(r'page=\d', current_page_link):
            connect_page = '?page=0'
            if re.findall(r'\?', current_page_link):
                connect_page = '&page=0'
            current_page_link += connect_page

        pages_links = []
        while not start_page > end_page:

            new_link = current_page_link
            new_link = re.sub(
                r'page=\d*', 'page={}'.format(start_page), new_link)
            new_page = {
                'link': new_link,
                'is_active': start_page == current_page_number,
                'number': start_page
            }
            pages_links.append(new_page)
            start_page += 1

        return pages_links

    def get_paginated_response(self, data):

        result = Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('page_links', self.get_page_links()),
            ('current_page_number', self.page.number),
            ('results', data)
        ]))

        return result
