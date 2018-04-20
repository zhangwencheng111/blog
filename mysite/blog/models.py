from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from taggit.managers import TaggableManager


class PublishedManager(models.Manager):
	""" 
	objects is the default manager of every model
	自己定义一个‘object’
	两种方法修改model manager： 
	添加manager：Post.objects.my_manager()
	修改初始manager：Post.my_manager.all()
	"""
	def get_queryset(self):
		return super(PublishedManager,
			self).get_queryset()\
			.filter(status='published')


class Post(models.Model):
	""""""
	STATUS_CHOICES = (
		('draft', 'Draft'),
		('published', 'Published'),
	)
	title = models.CharField(max_length=250)
	slug = models.SlugField(max_length=250,
							unique_for_date='publish')
	#unique_for_date要求在某个日期内，该字段值在数据表中是唯一的(就不存在时期和字段值都相同的记录)
	author = models.ForeignKey(User,
								related_name='blog_posts')
	#related_name :User.post_set ==> User.blog_posts
	body = models.TextField()
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	status = models.CharField(max_length=10,
								choices=STATUS_CHOICES,
								default='draft')
	#默认manager
	objects = models.Manager()
	#Post.published.all() ==> Post.objct.filter(status='published')
	published = PublishedManager()
	#添加tag管理器
	tags = TaggableManager()

	class Meta:
		ordering = ('-publish',)

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		""""""
		return reverse('blog:post_detail', args=[self.publish.year,
												 self.publish.strftime('%m'),
												 self.publish.strftime('%d'),
												 self.slug])


class Comment(models.Model):
	"""评论模块"""
	#related_name外键属性的别名 使用post.comments.all()==>post.comment_set.all()获取某个post的所有comments
	post = models.ForeignKey(Post, related_name='comments')
	name = models.CharField(max_length=80)
	email = models.EmailField()
	body = models.TextField()
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	active = models.BooleanField(default=True)
	
	class Meta:
		ordering = ('created',)
		
	def __str__(self):
		return 'Comment by {} on {}'.format(self.name, self.post)
