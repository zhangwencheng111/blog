from django.contrib import admin
from .models import Post, Comment

class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')
admin.site.register(Comment, CommentAdmin)


class PostAdmin(admin.ModelAdmin):
	#在admin界面的post界面显示的字段
	list_display = ('title', 'slug', 'author', 'publish',
					'status')
	#可以在右边过滤数据
	list_filter = ('status', 'created', 'publish', 'author')
	#关键字搜索（在title和body里找）
	search_fields = ('title', 'body')
	#默认slug=title
	prepopulate_fields = {"slug": ('title',)}
	#创建post时候author字段可以通过id找到选项（外键）
	raw_id_fields = ('author',)
	#search框框下面的动态时间
	date_hierarchy = 'publish'
	#默认排序
	ordering = ['status', 'publish']
admin.site.register(Post, PostAdmin)