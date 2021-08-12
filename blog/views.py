import random

from django.http import Http404
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from blog.models import blogPost

# Create your views here.

def blog_view(request, id):
    '''Show Blog depending on "id" '''

    try:
        first_name = request.session.get('first_name', default="Guest")
        all_post_ids = list(blogPost.objects.all().values_list('id', flat=True))
        except_current_page = [ids for ids in all_post_ids if ids != id] 
        random_posts = random.sample(except_current_page, 4)

        posts = blogPost.objects.get(id=id)
        other_posts1 = blogPost.objects.get(id=int(random_posts[0]))
        other_posts2 = blogPost.objects.get(id=int(random_posts[1]))
        other_posts3 = blogPost.objects.get(id=int(random_posts[2]))
        other_posts4 = blogPost.objects.get(id=int(random_posts[3]))

        list_other_posts = [other_posts1, other_posts2, other_posts3, other_posts4]
        context = {
            'first_name': first_name,
            'posts': posts,
            'random_posts': random_posts,
            'other_posts_list': list_other_posts,
        }
        return render(request, 'blog/blog_posts.html', context)

    except blogPost.DoesNotExist:
        raise Http404("Blog Page not found....")


def blog_home_view(request):
    '''Blog Home'''

    return HttpResponse("type /1 beside blog to start reading blogs")
    # return render(request, 'blog/blog.html', context)