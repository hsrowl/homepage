import markdown

from django.shortcuts import render, get_object_or_404
from comments.forms import CommentForm
from .models import Post, Category, Tag
from django.views.generic import ListView, DetailView
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models.aggregates import Count
from .libs.tag_cloud import TagCloud
import pdb;

class IndexView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    paginate_by = 14
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = context.get('paginator')
        page = context.get('page_obj')
        is_paginated = context.get('is_paginated')
      
        pagination_data = self.pagination_data(paginator, page, is_paginated)

        context.update(pagination_data)

        return context

    def pagination_data(self, paginator, page, is_paginated):
        if not is_paginated:
            
            return {}

        left = []

        right = []

        left_has_more = False

        right_has_more = False

        first = False

        last = False

        page_number = page.number

        total_pages = paginator.num_pages

        page_range = paginator.page_range

        if page_number == 1:
            right = page_range[page_number:page_number + 2]

            if right[-1] < total_pages - 1:
                right_has_more = True

            if right[-1] < total_pages:
                last = True

        elif page_number == total_pages:
            left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]

            if left[0] > 2:
                left_has_more = True

            if left[0] > 1:
                first = True
        else:
            left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]
            right = page_range[page_number:page_number + 2]

            if right[-1] < total_pages - 1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True

            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True

        data = {
            'left': left,
            'right': right,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'first': first,
            'last': last,
        }

        return data

class CategoryView(IndexView):
    def get_queryset(self):
        cate = get_object_or_404(Category, name=self.kwargs.get('name'))
        return super(CategoryView, self).get_queryset().filter(category=cate)
'''
class ArchivesView(ListView):
    model = Post
    template_name = 'archives.html'
    context_object_name = 'post_list'
    def get_queryset(self):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')
        return super(ArchivesView, self).get_queryset().filter(created_time__year=year,created_time__month=month,created_time__day=day)
'''
# 记得在顶部导入 DetailView
class PostDetailView(DetailView):
    # 这些属性的含义和 ListView 是一样的
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'
    slug_field = 'url_slug' # モデルのフィールドの名前
    slug_url_kwarg = 'url_slug' # urls.pyでのキーワードの名前
    def get(self, request, *args, **kwargs):
        # 覆写 get 方法的目的是因为每当文章被访问一次，就得将文章阅读量 +1
        # get 方法返回的是一个 HttpResponse 实例
        # 之所以需要先调用父类的 get 方法，是因为只有当 get 方法被调用后，
        # 才有 self.object 属性，其值为 Post 模型实例，即被访问的文章 post
        response = super(PostDetailView, self).get(request, *args, **kwargs)

        # 将文章阅读量 +1
        # 注意 self.object 的值就是被访问的文章 post
        self.object.increase_views()

        # 视图必须返回一个 HttpResponse 对象
        return response

    def get_object(self, queryset=None):
        # 覆写 get_object 方法的目的是因为需要对 post 的 body 值进行渲染
        post = super(PostDetailView, self).get_object(queryset=None)
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            # 记得在顶部引入 TocExtension 和 slugify
            TocExtension(slugify=slugify),
        ])
        post.body = md.convert(post.body)
        post.toc = md.toc
        return post

    def get_context_data(self, **kwargs):
        # 覆写 get_context_data 的目的是因为除了将 post 传递给模板外（DetailView 已经帮我们完成），
        # 还要把评论表单、post 下的评论列表传递给模板。
        context = super(PostDetailView, self).get_context_data(**kwargs)
        form = CommentForm()
        comment_list = self.object.comment_set.all()
        context.update({
            'form': form,
            'comment_list': comment_list
        })
        return context


class ArchivesView(IndexView):
    model = Post
    template_name = 'archives.html'
    post_list = Post.objects.all().order_by('-created_time')
    context_object_name = 'post_list'

class TagcloudView(ListView):
    model = Tag
    template_name = 'tagcloud.html'
    context_object_name = 'tag_list'

    def get_context_data(self, **kwargs):
        context = super(TagcloudView, self).get_context_data(**kwargs)
        tag_list = context.get("tag_list")


        for tag in tag_list:
            blog_count = Post.objects.filter(tags__pk=tag.id).count()
            tag.blog_count = blog_count


        max_count = min_count = 0
        if len(tag_list) > 0:
            max_count = max(tag_list, key=lambda tag: tag.blog_count).blog_count
            min_count = min(tag_list, key=lambda tag: tag.blog_count).blog_count

        tag_cloud = TagCloud(min_count, max_count)

        for tag in tag_list:
            tag_font_size = tag_cloud.get_tag_font_size(tag.blog_count)
            color = tag_cloud.get_tag_color(tag.blog_count)
            tag.color = color
            tag.font_size = tag_font_size
       # pdb.set_trace()
        return context

class TagsView(IndexView):
    def get_queryset(self):
   #    pdb.set_trace()
        tag = get_object_or_404(Tag, name=self.kwargs.get('name'))
        
        return super(TagsView, self).get_queryset().filter(tags=tag)

class AboutView(IndexView):
    template_name = 'about.html'



