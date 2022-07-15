import random

from dateutil.tz import tz
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.core.management.base import BaseCommand
from faker import Faker

from home.models import Post, Reply

# https://www.obytes.com/blog/building-a-full-text-search-app-using-django-docker-and-elasticsearch
# https://github.com/obytes/django-elasticsearch-example

# to test in the shell
# docker-compose run web python manage.py shell
# >>> from home.documents import PostDocument
# >>> posts = PostDocument.search()
# >>> for hit in posts:
# ...     print(hit.title)

# common commands:
# search = PostDocument.search()
# # Filter by single field equal to a value
# search = search.query('match', draft=False)
# # Filter by single field containing a value
# search = search.filter('match_phrase', title="value")
# # Add the query to the Search object
# from elasticsearch_dsl import Q
# q = Q("multi_match", query='python django', fields=['title', 'content'])
# search = search.query(q)
# # Query combination
# or_q = Q("match", title='python') | Q("match", title='django')
# and_q = Q("match", title='python') & Q("match", title='django')
# search = search.query(or_q)
# # Exclude items from your query
# search = search.exclude('match', draft=True)
# # Filter documents that contain terms within a provided range.
# # eg: the posts created for the past day
# search = search.filter('range', created_at={"gte": "now-1d"})
# # Ordering
# # prefixed by the - sign to specify a descending order.
# search = search.sort('-likes', 'created_at')

# config
User = get_user_model()


class Command(BaseCommand):
    help = 'Create random posts to test out elasticsearch'

    def add_arguments(self, parser):
        parser.add_argument('count', type=int, help='Indicates the number of posts to be created')
        parser.add_argument('-r', '--replies', action='store_true', help='Creates replies')

    def handle(self, *args, **kwargs):
        count = kwargs['count']
        replies = kwargs['replies']
        faker = Faker()

        # create a super user + other simple users. name="admin" already exists, so set as "admin1"
        User.objects.create_superuser("admin1", "admin@admin.com", "admin")
        [create_profile(faker) for _ in range(4)]

        users_ids = User.objects.values_list('id', flat=True)

        # create posts
        for _ in range(count):
            create_post(faker, users_ids, replies)

        call_command('search_index', '--rebuild', '-f')
        self.stdout.write(self.style.SUCCESS('Successfully ended commands'))


def create_profile(faker, retries=0):
    username = faker.user_name()

    if not User.objects.filter(username=username).exists():
        user = User(username=username, email=faker.email())
        user.set_password(faker.password())
        user.save()
        return user

    elif retries < 3:
        # try again with different random username
        return create_profile(faker, retries + 1)


def create_post(faker, users_ids, replies):
    post = Post(
        title=faker.text(60),
        user_id=random.choice(users_ids),
        content=faker.text(random.randint(100, 1000)),
        created_at=faker.date_time_between(start_date="-10d", end_date="now", tzinfo=tz.gettz('UTC')),
        draft=random.choice([True, False]),
    )
    post.save()

    if replies:
        add_random_replies(faker, post.id, users_ids)


def add_random_replies(faker, post_id, users_ids):
    for _ in range(random.randrange(5)):
        reply = Reply(
            content=faker.text(random.randint(10, 500)),
            user_id=random.choice(users_ids),
            post_id=post_id
        )
        reply.save()
