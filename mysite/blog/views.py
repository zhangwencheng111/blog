from django.shortcuts import render, get_object_or_404
from blog.models import Post, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from blog.forms import EmailPostForm, CommentForm
from django.core.mail import send_mail
from taggit.models import Tag


class PostListView(ListView):
	"""类视图，功能和post_list函数一样"""
	queryset = Post.published.all()
	context_object_name = 'posts'
	paginate_by = 3
	template_name = 'blog/post/list.html'


def post_list(request, tag_slug=None):
	""""""
	object_list = Post.published.all()
	tag = None

	if tag_slug:
		tag = get_object_or_404(Tag, slug=tag_slug)
		object_list = object_list.filter(tags__in=[tag])

	paginator = Paginator(object_list, 3) #3个post一页
	page = request.GET.get('page')
	try:
		posts = paginator.page(page)
	except PageNotAnInteger:
		#如果page不是个整数，就传第一页
		posts = paginator.page(1)
	except EmptyPage:
		#超过最大页数，返回最后一页
		posts = paginator.page(paginator.num_page)
	context = {'posts': posts, 'page':page, 'tag': tag}
	return render(request,
					"blog/post/list.html", 
					context)


from .models import Post, Comment
from .forms import EmailPostForm, CommentForm

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                                   status='published',
                                   publish__year=year,
                                   publish__month=month,
                                   publish__day=day)
    # List of active comments for this post
    comments = post.comments.filter(active=True)
    new_comment = None
        
    if request.method == 'POST':
        # A comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()
    return render(request,
                  'blog/post/detail.html',
                  {'post': post,
                  'comments': comments, 
                  'new_comment': new_comment,
                  'comment_form': comment_form})


"""
def post_detail(request, year, month, day, post):
	""""""
	#get_object_or_404根据提供的参数(model字段为参数名)，便捷获取Post对象
	#没有对象返回404
	#filter(publish__year=year)
	post_o = get_object_or_404(Post, slug=post,
									status='published',
									publish__year=year,
									publish__month=month,
									publish__day=day)
	# post里活跃的评论
	comments = post_o.comments.filter(active=True)
	new_comment = None

	if request == 'POST':
		#提交评论
		comment_form = CommentForm(data=request.POST)
		if comment_form.is_valid():
			#获取表单，但是不把表单存入数据库
			new_comment = comment_form.save(commit=False)
			#指定当前的这条评论的post
			new_comment.post = post_o
			#保存
			new_comment.save()
	else:
		comment_form = CommentForm()
	context = {'post': post_o, 'comments':comments, 'comment_form':comment_form, 'new_comment':new_comment}
	return render(request,
					'blog/post/detail.html',
					context)
"""


def post_share(request, post_id):
	"""获取post对象的id"""
	post = get_object_or_404(Post, id=post_id, status='published')
	sent = False

	if request.method == 'POST':
		"""提交表格"""
		form = EmailPostForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			print(cd)
			post_url = request.build_absolute_uri(
											post.get_absolute_url())
			subject = '{} ({}) recommends you reading "{}"'.format(cd['name'], cd['email'], post.title)
			message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(post.title, post_url, cd['name'], cd['comments'])
			send_mail(subject, message, 'admin@myblog.com', [cd["to"]])
			sent = True
	else:
		form = EmailPostForm()
	return render(request, 'blog/post/share.html', {"post":post, "form":form, "sent":sent})