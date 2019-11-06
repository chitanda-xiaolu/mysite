from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator
from django.contrib.contenttypes.models import ContentType
from .models import Blogtype, Blog, Banner, PhotographyShow
from visitscounter.utils import counterMethod
from comment.models import Comment




# Create your views here
#定义获取Blog共同数据的方程
def get_data_of_comblog(request, blogs_list):
    paginator = Paginator(blogs_list, 15)
    page_num = request.GET.get('page', 1)  # 获取url页面参数(GET请求)
    page = paginator.get_page(page_num)  # 从分页器获取page_num分页对象
    current_page = page.number  # 获取当前页码
    page_range = [x for x in range(current_page - 2, current_page + 3) if x in paginator.page_range]  # 截取当前页面前三页和后三页的页码列表
    # 加上页码省略号标记
    if current_page - 1 > 3:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')
    # 加上首页和尾页
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)

    #统计同一时间内存档的博客数量
    blog_dates = Blog.objects.dates('created_time', 'month', order="DESC")
    blog_dates_dict = {}
    for blog_date in blog_dates:
        print(blog_date.year)
        print(blog_date.month)
        blog_count = Blog.objects.filter(created_time__year=blog_date.year,
                                         created_time__month=blog_date.month).count()
        print(blog_count)
        blog_dates_dict[blog_date] = blog_count
    context = {}
    context['photos'] = PhotographyShow.objects.all()
    context['banners'] = Banner.objects.all()
    context['blogs'] = page.object_list
    context['page'] = page
    context['types'] = Blogtype.objects.all()
    context['page_range'] = page_range
    context['blog_dates_dict'] = blog_dates_dict
    return context



def blog_list(request):
    blogs_list = Blog.objects.all()
    context = get_data_of_comblog(request, blogs_list)
    return render(request, 'blog/chitanda.html', context)


def blog_with_type(request, id):
    blog_type = get_object_or_404(Blogtype, pk=id)
    com_blogs = Blog.objects.filter(blog_type=blog_type)
    context = get_data_of_comblog(request, com_blogs)
    context['blog_type'] = blog_type
    return render(request, 'blog/blogWithType.html', context)


def blog_detail(request, blog_pk):
    blog = get_object_or_404(Blog, pk=blog_pk)
    read_cookie = counterMethod(request, blog)#从visitscounter里引入的统计浏览数的方法
    blog_content_type = ContentType.objects.get_for_model(blog)
    # comments = Comment.objects.filter(content_type=blog_content_type, object_id=blog.pk, parent=None).order_by('-comment_time')#获取顶级评论
    comment_count = Comment.objects.filter(content_type=blog_content_type, object_id=blog.pk).count()#获取评论数
    # comment_form = CommentForm(initial={'content_type': blog_content_type, 'object_id': blog_pk, 'reply_comment_id': 0})#评论表单实例化
    blog_dates = Blog.objects.dates('created_time', 'month', order='DESC')
    # 统计同一时间内存档的博客数量
    blog_dates_dict = {}
    for blog_date in blog_dates:
        blog_count = Blog.objects.filter(created_time__year=blog_date.year,
                                         created_time__month=blog_date.month).count()
        blog_dates_dict[blog_date] = blog_count
    photos = PhotographyShow.objects.all()
    context = {'blog': blog, 'blog_dates_dict': blog_dates_dict, 'comment_count': comment_count, 'photos': photos}
    response = render(request, 'blog/article.html', context)
    response.set_cookie(read_cookie, 'true')#给前端发送一个cookie用于判断用户是否阅读过
    return response

#博客日期存档
def blog_classify_by_date(request, year, month):
    com_blogs = Blog.objects.filter(created_time__year=year, created_time__month=month)
    context = get_data_of_comblog(request, com_blogs)
    context['blog_with_date'] = '%s年%s月' % (year, month)
    return render(request, 'blog/blogWithDate.html', context)
