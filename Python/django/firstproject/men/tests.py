from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from men.models import Men


class GetPagesTestCase(TestCase):
    fixtures = ['men_men.json', 'men_category.json', 'men_wife.json', 'men_tagpost.json']

    def setUp(self):
        ''

    def test_mainpage(self):
        path = reverse('home')
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'men/index.html')
        self.assertEqual(response.context_data['title'], 'Главная страница')

    def test_redirect_addpage(self):
        path = reverse('add_page')
        redirect_url = reverse('users:login') + '?next=' + path
        response = self.client.get(path)
        self.assertRedirects(response, redirect_url)

    def test_data_mainpage(self):
        m = Men.published.all().select_related('cat')
        path = reverse('home')
        response = self.client.get(path)
        self.assertQuerysetEqual(response.context_data['posts'], m)

    # def test_paginate_mainpage(self):
    #     path = reverse('home')
    #     page = 2
    #     paginate_by = 5
    #     response = self.client.get(path + f'?page={page}')
    #     m = Men.published.all().select_related('cat')
    #     self.assertQuerysetEqual(response.context_data['posts'], m[(page - 1) * paginate_by: page * paginate_by])

    def test_content_post(self):
        m = Men.objects.get(pk=1)
        path = reverse('post', args=[m.slug])
        response = self.client.get(path)
        self.assertEqual(m.content, response.context_data['post'].content)

    def tearDown(self):
        ''