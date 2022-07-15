from django.contrib.auth import get_user_model
from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from .models import Post, Reply

User = get_user_model()

@registry.register_document
class PostDocument(Document):
    user = fields.ObjectField(properties={
        'id': fields.IntegerField(),
        'username': fields.TextField(),
    })

    class Index:
        name = 'posts'
        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}

    class Django:
        model = Post

        fields = [
            'title',
            'content',
            'created_at',
            'likes',
            'draft',
            'slug',
        ]

    def get_queryset(self):
        return super(PostDocument, self).get_queryset().select_related(
            'user'
        )

    def get_instances_from_related(self, related_instance):
        if isinstance(related_instance, User):
            return related_instance.posts.all()
        elif isinstance(related_instance, Reply):
            return related_instance.post