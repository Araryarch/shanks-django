import { DocPage, CodeBlock } from '@/components/DocPage';

export default function OrmRelationshipsPage() {
  return (
    <DocPage title="Relationships" description="Define and query model relationships using Django's ForeignKey, ManyToMany, and OneToOne.">

      <h2>ForeignKey (Many-to-One)</h2>
      <CodeBlock
        filename="entity/post.py"
        code={`from django.db import models

class Post(models.Model):
    title   = models.CharField(max_length=255)
    author  = models.ForeignKey(
        'entity.User',
        on_delete=models.CASCADE,
        related_name='posts'
    )

    class Meta:
        app_label = 'entity'`}
      />

      <h2>Querying Related Data</h2>
      <CodeBlock
        code={`# All posts by a user
posts = Post.find_many(author_id=user.id)

# Access the related object
post = Post.find_unique(id=1)
author = post.author   # Django-style traversal

# Reverse: all posts for a user
user = User.find_unique(id=1)
posts = user.posts.all()`}
      />

      <h2>ManyToManyField</h2>
      <CodeBlock
        filename="entity/post.py"
        code={`class Post(models.Model):
    title = models.CharField(max_length=255)
    tags  = models.ManyToManyField('entity.Tag', blank=True, related_name='posts')

    class Meta:
        app_label = 'entity'`}
      />
      <CodeBlock
        code={`# Add tags
post = Post.find_unique(id=1)
tag  = Tag.find_unique(name='python')
post.tags.add(tag)

# Query all posts with a tag
tagged_posts = Post.objects.filter(tags__name='python')`}
      />

      <h2>OneToOneField</h2>
      <CodeBlock
        filename="entity/profile.py"
        code={`class Profile(models.Model):
    user   = models.OneToOneField('entity.User', on_delete=models.CASCADE, related_name='profile')
    bio    = models.TextField(blank=True)
    avatar = models.URLField(blank=True)

    class Meta:
        app_label = 'entity'`}
      />
      <CodeBlock
        code={`user    = User.find_unique(id=req.user.id)
profile = user.profile   # direct access via reverse relation`}
      />
    </DocPage>
  );
}
