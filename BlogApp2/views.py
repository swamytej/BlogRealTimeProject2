from django.shortcuts import render,get_object_or_404,redirect,HttpResponse
from BlogApp2.models import Post,Comment
from BlogApp2.forms import CommentForm
from taggit.models import Tag
from django.contrib.auth.models import User
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail

# Create your views here.

def post_list_view(request):
     postlist =Post.objects.all()
     return render(request,'BlogApp2/post_list.html',{'postlist':postlist})

from django.db.models import Count

def post_detailview(request,post,year,month,day):
    post = get_object_or_404(Post, slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.objects.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', 'publish')[:4]
    comments = post.comments.filter(active=True)
    csubmit = False
    if request.method == 'POST':
        form = CommentForm(data=request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.post = post
            new_comment.save()
            csubmit = True
    else:
        form = CommentForm()
    return render(request, 'BlogApp2/post_detail.html',{"post": post, 'form': form, 'comments': comments, 'csubmit': csubmit,'similar_posts':similar_posts})

'''
def post_detailview(request,year,month,day,post):
    post=get_object_or_404(Post,slug = post,
                           status = 'published',
                           publish__year=year,
                           publish__month = month,
                           publish__day = day)
    post_tags_ids = post.tags.values_list('id',flat=True)
    similar_posts = Post.objects.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags'))
    comments = post.comments.filter(active=True)
    csubmit = False
    if request.method=='POST':
        form=CommentForm(data=request.POST)
        if form.is_valid():
            new_comment=form.save(commit=False)
            new_comment.post = post
            new_comment.save()
            csubmit =True
    else:
        form = CommentForm()
    return render(request,'BlogApp2/post_detail.html',{'post':post,'form':form,'comments':comments,'csubmit':csubmit,'similar_posts':similar_posts})
'''

@login_required
def post_list_view(request,tag_slug=None):
    print('post_list_view with paginator')
    postlist=Post.objects.all()
    for post in postlist:
        print(post.images.name)
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        postlist= postlist.filter(tags__in=[tag])
    paginator = Paginator(postlist,2)
    page_number = request.GET.get('page')
    try:
        postlist =paginator.page(page_number)
    except PageNotAnInteger:
        postlist= paginator.page(1)
    except EmptyPage:
        postlist= paginator.page(paginator.num_pages)
    return render(request,'BlogApp2/post_list.html',{"postlist":postlist,'tag':tag})

from django.views.generic import ListView

class postlistview(ListView):
    model=Post
    paginate_by = 1



#send_mail('Hello', "Iam swamy..",'swamytirumani13@gmail.com',['varunsai0089@gmail.com','uppalakavitha904@gmail.com','srinivas.kosuru456@gmail.com'])
from  BlogApp2.forms import Emailsendform



def mailsendview(request,id):
    post = get_object_or_404(Post,id=id, status='Published')
    sent = False
    form = Emailsendform()
    if request.method=='POST':
        form =Emailsendform(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url =request.build_absolute_uri(post.get_absolute_url())
            Subject ='{}({}) recommends you to read "{}"'.format(cd['name'],cd['email'],post.title)
            message ="Read post At: \n{}\n\n{}".format(post_url,cd['name'],cd['comments'])
            send_mail(Subject,message,'swamytirumani13@gmail.com',[cd['to']])
            sent =True
    else:
         form = Emailsendform()
    return render(request,'BlogApp2/sharebymail.html',{'post':post,'form':form,'sent':sent})

from django.contrib.auth.decorators import login_required

#@login_required
def home_page(request):
    return render(request,'BlogApp2/home.html')

from BlogApp2.forms import postform
def postview(request):
    form = postform()

    print('welcome')
    if request.method=='POST':
        form = postform(request.POST, request.FILES)
        if form.is_valid():
            print('hi')
            user = form.save(commit=True)
            return HttpResponseRedirect('/thank/')
    return render(request,'BlogApp2/postmain.html',{'form':form})

def logout_view(request):
    request.session.clear()
    return render(request,'BlogApp2/logout.html')

from BlogApp2.forms import signupform
from django.http import HttpResponseRedirect

def signupview(request):
    sent = False
    form = signupform()
    if request.method=='POST':
        form = signupform(request.POST)
        if form.is_valid():
            user = form.save()
            user.set_password(user.password)
            user.save()
            sent = True
            return HttpResponseRedirect('/accounts/login/')
    else:
        form = signupform()
    return render(request,'BlogApp2/signup.html',{'form':form ,'sent':sent})


('\n'
 'from django.views.generic import CreateView\n'
 '\n'
 'class post(CreateView):\n'
 '    model = Post\n'
 '    fields = \'__all__\'\n'
 '    template_name = \'BlogApp/postmain.html\'\n')


def thankyou1(request):
    return render(request, 'BlogApp2/thankyou1.html')

from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView,DeleteView,UpdateView
from django.core.files.storage import FileSystemStorage

class commentview(CreateView):
    model = Comment
    fields= ['name','email','body']
    template_name = 'BlogApp2/comment.html'


class commentdelete(DeleteView):
    model = Comment
    success_url = reverse_lazy('succ')

def commentdelsucc(request):
    return render(request, 'BlogApp2/delete.html')

class postupdateview(UpdateView):
    model = Post
    fields = ('title','slug','author','body','images')

def profileview(request):
    return render(request, 'BlogApp2/user_details.html')


#username  | first_name | last_name | email
def profileupdate(request,pk):
    user = User.objects.get(id=pk)
    print('hi')
    if request.method=="POST":
        print('hello')
        form = signupform(request.POST,instance=user)
        print('welcome')
        if form.is_valid():
            ser = user.username()
            print('nice')
            user.save(commit=True)
            return redirect('/update/')
    print('ok')
    return render(request,'BlogApp2/user_form.html',{'user':user,})
'''
def profileupdate(request,pk):
    user = User.objects.get(id=pk)
    print('hi')
    if request.method=="POST":
        print('hello')
        form = signupform(request.POST,instance=user)
        print('welcome')
        if form.is_valid():
            print('nice')
            form.save(commit=True)
            return redirect('/update/')
    print('ok')
    return render(request,'BlogApp2/user_form.html',{'user':user})
'''

class Postdeleteview(DeleteView):
    model = Post
    success_url = reverse_lazy('succ')

def postsuccview(request):
    return render(request,'BlogApp2/delete.html')

def contactview(request):
    return render(request, 'BlogApp2/contact.html')