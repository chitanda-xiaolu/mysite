from django.shortcuts import redirect, reverse
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from .models import Comment
from .forms import CommentForm

# Create your views here.

def comment_update(request):
    # referer = request.META.get('HTTP_REFERER', reverse('homepage'))
    print('成功联通')
    comment_form = CommentForm(request.POST, user=request.user)
    if comment_form.is_valid():
        comment = Comment()
        comment.user = comment_form.cleaned_data['user']
        comment.comment_text = comment_form.cleaned_data['text']
        comment.content_object = comment_form.cleaned_data['content_object']

        parent = comment_form.cleaned_data['parent']
        if not parent is None:
            comment.root = parent.root if not parent.root is None else parent
            comment.parent = parent
            comment.reply_to = parent.user

        comment.save()

        # 发送邮件通知
        comment.send_mail()

        # 返回数据
        username = comment.user.get_nickname_or_username()
        comment_time = comment.comment_time.timestamp()
        comment_text = comment.comment_text
        img_src = str(comment.user.profile.user_head.url)
        # print(img_src)
        if not parent is None:
            reply_to = comment.reply_to.get_nickname_or_username()
        else:
            reply_to = ''
        pk = comment.pk
        root_pk = comment.root.pk if not comment.root is None else ''
        data = {'status': 'success', 'username': username, 'comment_time': comment_time, \
                'comment_text': comment_text, 'reply_to': reply_to, 'pk': pk, 'root_pk': root_pk, 'img_src': img_src}
    else:
        # 评论对象不存在时的处理
        message = list(comment_form.errors.values())[0][0]
        data = {'status': 'failed', 'message': message}
    return JsonResponse(data)

