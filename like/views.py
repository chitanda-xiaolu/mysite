from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
from django.db.models import ObjectDoesNotExist
from .models import LikeCounter, LikeRecord

# Create your views here.
def SuccessResonse(liked_num):
    data = {}
    data['status'] = 'success'
    data['liked_num'] = liked_num
    return JsonResponse(data)

def ErrorResponse(code, message):
    data = {}
    data['status'] = 'error'
    data['code'] = code
    data['message'] = message
    return JsonResponse(data)

def like_change(request):
    print('链接成功')
    #获取数据
    user = request.user
    if not user.is_authenticated:
        return ErrorResponse(402, '登录了，才能够点赞哦~')
    print('已登录')
    content_type = request.GET.get('content_type')
    object_id = int(request.GET.get('object_id'))
    try:
        content_type = ContentType.objects.get(model=content_type)
        model_class = content_type.model_class()
        model_obj = model_class.objects.get(pk=object_id)
    except ObjectDoesNotExist:
        ErrorResponse(402, 'Object dose not exist')

    is_like = request.GET.get('is_like')
    print(is_like)

    #处理数据
    if is_like == 'true':
        print('点赞成功')
        like_record, created = LikeRecord.objects.get_or_create(content_type=content_type, object_id=object_id, user=user)
        if created:
            # 未点赞，进行点赞
            like_count, created = LikeCounter.objects.get_or_create(content_type=content_type, object_id=object_id)
            like_count.liked_num += 1
            like_count.save()
            return SuccessResonse(like_count.liked_num)
        else:
            #已点赞，不能重复点赞
            return ErrorResponse(402, 'can not repeat')
    if is_like == 'false':
        print('进入取消点赞')
        # 取消点赞
        if LikeRecord.objects.filter(content_type=content_type, object_id=object_id, user=user).exists():
            #有点赞过取消点赞
            like_record = LikeRecord.objects.get(content_type=content_type, object_id=object_id, user=user)
            like_record.delete()
            like_count, created = LikeCounter.objects.get_or_create(content_type=content_type, object_id=object_id)
            if not created:
                like_count.liked_num -= 1
                like_count.save()
                return SuccessResonse(like_count.liked_num)
            else:
                return ErrorResponse(404, 'data error')
        else:
            # 没有点赞过无法取消
            return ErrorResponse(403, 'can not cancel')