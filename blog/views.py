from django.core.paginator import Paginator
from django.db.models import Count, Q, F
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.utils import timezone
from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import Post, Comment, SiteAbout, PostView
from .forms import PostForm, CommentForm
from django.shortcuts import redirect
from django.contrib.auth.models import User

# Create your views here.
########################################################################postlist#############################
# @login_required
# def post_list(request):
#     ordering = request.GET.get("ordering", 'newer')
#     type = request.GET.get("type", None)
#     sort = '-published_date'

#     if ordering == 'older':
#         sort = 'published_date'
#         posts = Post.objects.filter(
#             published_date__lte=timezone.now()).order_by(sort)
#     # elif ordering=='newer':
#     #     sort = sort
#     #     posts = Post.objects.filter(published_date__lte=timezone.now()).order_by(sort)
#     if type == 'draft':
#         return post_draft_list(request=request)
#         # posts = Post.objects.filter(~Q(published_date__isnull=True))
#         # return redirect('/drafts?next=')
#     else:
#         posts = Post.objects.filter(
#             published_date__lte=timezone.now()).order_by(sort)
#     return render(request, 'blog/post_list.html', {'myposts': posts})

# the avove code will not work for restframwork#########
@login_required
def post_list(request):
    ordering = request.GET.get('ordering' ,'newer')
    sort = '-published_date' if ordering == 'newer' else 'published_date'
    types = request.GET.get('types', 'published')
    # posts = Post.objects.annotate(
    #     num_views=Count('post_views'), id_2=F('id')*2).all()
    posts = Post.objects.annotate(num_views=Count('post_views')).all()
    if types == 'published':
        posts = posts.filter(published_date__isnull=False)
    else:
        posts = posts.filter(published_date__isnull=True)
    return render(request, 'blog/post_list.html', {'myposts': posts.order_by(sort)})

########################################################################detaillist#############################

# @login_required
# def post_detail(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     if post.published_date is not None:
#         post.visit_count += 1
#         post.save()
#     return render(request, 'blog/post_detail.html', {'post': post})


@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    # if not PostView.objects.filter(post_id=pk, user_id=request.user.id).exists():
    #     PostView.objects.create(post_id=pk, user_id=request.user.id)
    obj, created=PostView.objects.get_or_create(post_id=pk, user_id=request.user.id)
    return render(request, 'blog/post_detail.html', {'post': post})

########################################################################postnew#############################

# @login_required
# def post_new(request):
#     if request.method == "POST":
#         form=PostForm(request.POST)
#         if form.is_valid():
#             post=form.save(commit=False)
#             post.auther = request.user
#             # post.published_date =  timezone.now()
#             post.save()
#             return redirect('post_detail', pk=post.pk)
#     else:
#         form = PostForm()
#     return render(request, 'blog/post_edit.html', {'form': form})

# class for the above def################

class CreatePost(View):
    template_name = 'blog/post_edit.html'
    form_class = PostForm

    def get(self, request):
        # form = self.form_class()
        return render(request, self.template_name, {'form': self.form_class()})

    def post(self, request):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.auther = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
        return render(request, self.template_name, {'form': form})

########################################################################postedit#############################
@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.auther = request.user
            # post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

########################################################################postdraft#############################

@login_required
def post_draft_list(request):
    posts = Post.objects.filter(
        published_date__isnull=True).order_by('-created_date')
    return render(request, 'blog/post_draft_list.html', {'posts': posts})

########################################################################postpublish#############################

@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)

########################################################################postremove#############################

@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')

########################################################################comment#############################

@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})


@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)


@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    print("####", redirect('post_detail', pk=comment.post.pk))
    return redirect('post_detail', pk=comment.post.pk)

########################################################################aboutas#############################

class About_Us(View):
    def get(self, request):
        queryset = SiteAbout.objects.all()
        template_name = 'blog/about_us.html'
        return render(request, template_name, {'data': queryset})





# barai nemoneh boud#####################
# class About_Us(View):
#     template_name = 'blog/about_us.html'
#     queryset = SiteAbout.objects.all()

#     def get(self, request):
#         return render(request, self.template_name, {'data':self.queryset})

# class About_Us(View):
#     template_name = 'blog/about_us.html'
#     model = SiteAbout

#     def get(self, request):
#         return render(request, self.template_name, {'data':self.model.object.all()})

# class About_Us(View):
#     template_name = 'blog/about_us.html'
#     model = SiteAbout

#     def get(self, request):
#         return render(request, self.template_name, {'data':self.model.object.get(pk)})

########################################################################postuniqueview#############################
#  baraye shomaresh view ha
# def post_view_count(request, pk):
#     post_visit = Post.objects.get(pk=pk)
#     return render(request,'blog/post_detail.html', pk=post_visit.pk)
########################################################################postuniqueview#############################
# baraye tarifeh karbar yekta
# def unique_visitor(request, pk):
#     post_visit = Post.objects.get(pk=pk)
#     user = request.user
#     queryset = Post.objects.annotate(num_views=Count('viewers'))
#     if user.is_authenticated and user.username not in queryset:
#         post_visit.visit_count += 1
#         post_visit.save()
#         # add username to viewers list
#         post_visit.visitors+=user.username
#         post_visit.save()
#     else:
#         return redirect('post_detail', pk=post_visit.pk)
#     return render(request, 'blog/post_detail', pk=post_visit.pk)
