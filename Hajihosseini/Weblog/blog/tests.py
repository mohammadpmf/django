from django.test import TestCase
from django.contrib.auth.models import User
# from django.shortcuts import reverse
from django.urls import reverse

from .models import BlogPost

class BlogPostTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user1 = User.objects.create(username='admin')
        cls.post1 = BlogPost.objects.create(
            title='Post 1',
            text="First Post of site Lorem ipsum dolor sit, amet consectetur adipisicing elit. Provident cum voluptas, necessitatibus enim natus soluta quia dignissimos commodi dolores quam facere iste, quos, architecto aut modi odit ea! Pariatur, minus! Lorem ipsum dolor sit amet consectetur, adipisicing elit. Asperiores, pariatur incidunt debitis corrupti officia quae explicabo est sapiente autem obcaecati necessitatibus expedita esse eos voluptatum quos, blanditiis rerum beatae itaque!",
            author = cls.user1,
            status=BlogPost.STATUS_CHOICES[0][0]
        )
        cls.post2 = BlogPost.objects.create(
            title='Post 2',
            text="Second Post of site Lorem ipsum dolor sit, amet consectetur adipisicing elit. Provident cum voluptas, necessitatibus enim natus soluta quia dignissimos commodi dolores quam facere iste, quos, architecto aut modi odit ea! Pariatur, minus! Lorem ipsum dolor sit amet consectetur, adipisicing elit. Asperiores, pariatur incidunt debitis corrupti officia quae explicabo est sapiente autem obcaecati necessitatibus expedita esse eos voluptatum quos, blanditiis rerum beatae itaque!",
            author = cls.user1,
            status=BlogPost.STATUS_CHOICES[1][0]
        )
        cls.post3 = BlogPost.objects.create(
            title='Post 3',
            text="Third Post of site Lorem ipsum dolor sit, amet consectetur adipisicing elit. Provident cum voluptas, necessitatibus enim natus soluta quia dignissimos commodi dolores quam facere iste, quos, architecto aut modi odit ea! Pariatur, minus! Lorem ipsum dolor sit amet consectetur, adipisicing elit. Asperiores, pariatur incidunt debitis corrupti officia quae explicabo est sapiente autem obcaecati necessitatibus expedita esse eos voluptatum quos, blanditiis rerum beatae itaque!",
            author = cls.user1,
            status=BlogPost.STATUS_CHOICES[0][0]
        )
  
    def test_post_list_url(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_post_list_url_by_name(self):
        response = self.client.get(reverse('posts_list'))
        self.assertEqual(response.status_code, 200)

    def test_post_title_in_home_page(self):
        response = self.client.get(reverse('posts_list'))
        self.assertContains(response, self.post1.title)
    
    def test_post_detail_url(self):
        response = self.client.get(f'/detail/{self.post1.id}/')
        self.assertEqual(response.status_code, 200)

    def test_post_detail_url_by_name(self):
        response = self.client.get(reverse('post_detail', args=[self.post1.id]))
        self.assertEqual(response.status_code, 200)

    def test_status_404_if_post_not_exists(self):
        response = self.client.get(reverse('post_detail', args=[50]))
        self.assertEqual(response.status_code, 404)

    def test_post_detail_in_post_detail_page(self):
        response = self.client.get(reverse('post_detail', args=[self.post1.id]))
        self.assertContains(response, self.post1.text)

    def test_post_all_things_in_post_detail_page(self):
        response = self.client.get(reverse('post_detail', args=[self.post1.id]))
        self.assertContains(response, self.post1.title)
        self.assertContains(response, self.post1.text)
        self.assertContains(response, self.post1.author.first_name)
        self.assertContains(response, self.post1.author.last_name)
        self.assertContains(response, self.post1.likes)
        self.assertContains(response, self.post1.datetime_created.year)
        self.assertContains(response, self.post1.datetime_created.month)
        self.assertContains(response, self.post1.datetime_created.day)
        self.assertContains(response, self.post1.datetime_created.hour)
        # self.assertContains(response, self.post1.datetime_created.minute)
        self.assertContains(response, self.post1.datetime_created.second)
        self.assertContains(response, self.post1.datetime_modified.year)
        self.assertContains(response, self.post1.datetime_modified.month)
        self.assertContains(response, self.post1.datetime_modified.day)
        self.assertContains(response, self.post1.datetime_modified.hour)
        # self.assertContains(response, self.post1.datetime_modified.minute)
        self.assertContains(response, self.post1.datetime_modified.second)
    
    def test_draft_post_not_show_in_post_list(self):
        response = self.client.get(reverse('posts_list'))
        self.assertContains(response, self.post1.title)
        self.assertNotContains(response, self.post2.title)

    def test_post_model_str(self):
        self.assertIn(self.post1.title, str(self.post1))

    def test_post_delete_view_render_if_method_is_get(self):
        response = self.client.get(reverse('post_delete', args=[self.post1.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Yes')
        self.assertContains(response, f'No. Back to post {self.post1.title}')

    def test_post_delete_view_get_404_if_not_exists(self):
        response = self.client.post(reverse('post_delete', args=[1000]))
        self.assertEqual(response.status_code, 404)

    def test_post_delete_view_redirect_after_delete(self):
        response = self.client.post(reverse('post_delete', args=[self.post1.pk]))
        self.assertEqual(response.status_code, 302)

    def test_post_create_view_render_if_method_is_get(self):
        response = self.client.get(reverse('post_create'))
        self.assertEqual(response.status_code, 200)

    def test_post_create_view_if_everything_is_ok(self):
        response = self.client.post(reverse('post_create'), {
            'title': 'New Post',
            'text': 'New text',
            'author': self.user1.id,
            'status': BlogPost.STATUS_CHOICES[0][0],
            'likes': 0,
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(BlogPost.objects.last().title, 'New Post')
        self.assertEqual(BlogPost.objects.last().text, 'New text')
    
    def test_post_update_view_render_if_method_is_get(self):
        response = self.client.get(reverse('post_update', args=[self.post1.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.post1.title)
        self.assertContains(response, self.post1.text)
        self.assertContains(response, self.post1.author)
        self.assertContains(response, self.post1.status)
        self.assertContains(response, self.post1.likes)

    def test_post_update_view_get_404_if_not_exists(self):
        response = self.client.post(reverse('post_update', args=[1000]), {
            'title': 'Post 1 Updated!',
            'text': 'Text 1 Updated!',
            'author': self.post1.author.pk,
            'status': self.post1.status,
            'likes': self.post1.likes,
        })
        self.assertEqual(response.status_code, 404)

    def test_post_update_view_confirm_if_method_is_post_and_everything_is_ok(self):
        response = self.client.post(reverse('post_update', args=[self.post1.pk]), {
            'title': 'Post 1 Updated!',
            'text': 'Text 1 Updated!',
            'author': self.post1.author.pk,
            'status': self.post1.status,
            'likes': self.post1.likes
        })
        self.assertEqual(response.status_code, 302)
