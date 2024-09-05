from django.core.management.base import BaseCommand
from blog.models import Post, Category, Tag
from django.contrib.auth.models import User
import random
from django.core.files import File
import os


class Command(BaseCommand):
    help = 'Create dummy posts for testing pagination'

    def handle(self, *args, **kwargs):
        user = User.objects.first()
        category = Category.objects.first()
        tags = list(Tag.objects.all())

        default_image_path = os.path.join('static/shop/img/blog/', 'blog-4.jpg')

        for i in range(100):
            post = Post(
                title=f'Dummy Post {i+1}',
                content=f'This is the content for dummy post {i+1}.',
                author=user,
                category=category,
            )

            with open(default_image_path, 'rb') as img:
                post.cover_image.save(f'dummy_image_{i+1}.jpg', File(img), save=False)

            post.save()

            post.tags.set(random.sample(tags, k=random.randint(1, len(tags))))
            post.save()

        self.stdout.write(self.style.SUCCESS('Successfully created 100 dummy posts'))
