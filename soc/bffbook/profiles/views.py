# these for the post and others stuffs
from posts.models import Post
from django.urls import reverse_lazy
from posts.models import Post, Like
from posts.forms import PostModelForm, CommentModelForm
from django.views.generic import UpdateView, DeleteView
from django.contrib import messages
from django.http import JsonResponse
# these is the code for the profile
from django.shortcuts import render, redirect, get_object_or_404
from .models import Profile, Relationship
from .forms import ProfileModelForm
from django.views.generic import ListView, DetailView
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


@login_required
def my_profile_view(request):
    profile = Profile.objects.get(user=request.user)
    # THESE IS FOR THE CHANGE PROFILE
    form = ProfileModelForm(request.POST or None,
                            request.FILES or None, instance=profile)
    # TO  CONFIRM
    confirm = False
    #  TO CHECK WEATHER THE PSOTS IS UPLADED FOR NOT
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            confirm = True
    context = {
        'profile': profile,
        'form': form,
        'confirm': confirm,
    }

    return render(request, 'profiles/myprofile.html', context)

# THESE IS THE CODE THAT I HAD WRITE FOR THE FIRST TIME


@login_required
def my_profile_view_edit(request):
    profile = Profile.objects.get(user=request.user)
    # THESE IS FOR THE CHANGE PROFILE
    form = ProfileModelForm(request.POST or None,
                            request.FILES or None, instance=profile)
    # TO  CONFIRM
    confirm = False
    #  TO CHECK WEATHER THE PSOTS IS UPLADED FOR NOT
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            confirm = True
            context = {
                'profile': profile,
                'form': form,
                'confirm': confirm,
            }
            return render(request, 'profiles/myprofile.html', context)
    else:
        context = {
            'profile': profile,
            'form': form,
            'confirm': confirm,
        }
        return render(request, 'profiles/pro_edite.html', context)


@login_required
def invites_received_view(request):
    profile = Profile.objects.get(user=request.user)
    qs = Relationship.objects.invatations_received(profile)
    results = list(map(lambda x: x.sender, qs))
    is_empty = False
    if len(results) == 0:
        is_empty = True

    context = {
        'qs': results,
        'is_empty': is_empty,
    }

    return render(request, 'profiles/my_invites.html', context)


@login_required
def accept_invatation(request):
    if request.method == "POST":
        pk = request.POST.get('profile_pk')
        sender = Profile.objects.get(pk=pk)
        receiver = Profile.objects.get(user=request.user)
        rel = get_object_or_404(Relationship, sender=sender, receiver=receiver)
        if rel.status == 'send':
            rel.status = 'accepted'
            rel.save()
    return redirect('profiles:my-invites-view')


@login_required
def reject_invatation(request):
    if request.method == "POST":
        pk = request.POST.get('profile_pk')
        receiver = Profile.objects.get(user=request.user)
        sender = Profile.objects.get(pk=pk)
        rel = get_object_or_404(Relationship, sender=sender, receiver=receiver)
        rel.delete()
    return redirect('profiles:my-invites-view')


@login_required
def invite_profiles_list_view(request):
    user = request.user
    qs = Profile.objects.get_all_profiles_to_invite(user)
    context = {'qs': qs}
    return render(request, 'profiles/to_invite_list.html', context)


@login_required
def profiles_list_view(request):
    user = request.user
    qs = Profile.objects.get_all_profiles(user)
    context = {'qs': qs}
    return render(request, 'profiles/profile_list.html', context)


# LoginRequiredMixin
class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'profiles/detail.html'

    # def get_object(self):
    #     slug = self.kwargs.get('slug')
    #     profile = Profile.objects.get(slug=slug)
    #     return profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(username__iexact=self.request.user)
        profile = Profile.objects.get(user=user)
        rel_r = Relationship.objects.filter(sender=profile)
        rel_s = Relationship.objects.filter(receiver=profile)
        rel_receiver = []
        rel_sender = []
        for item in rel_r:
            rel_receiver.append(item.receiver.user)
        for item in rel_s:
            rel_sender.append(item.sender.user)
        context["rel_receiver"] = rel_receiver
        context["rel_sender"] = rel_sender
        context['posts'] = self.get_object().get_all_authors_posts()
        context['len_posts'] = True if len(
            self.get_object().get_all_authors_posts()) > 0 else False
        return context


class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'profiles/detail.html'

    # def get_object(self):
    #     slug = self.kwargs.get('slug')
    #     profile = Profile.objects.get(slug=slug)
    #     return profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(username__iexact=self.request.user)
        profile = Profile.objects.get(user=user)
        rel_r = Relationship.objects.filter(sender=profile)
        rel_s = Relationship.objects.filter(receiver=profile)
        rel_receiver = []
        rel_sender = []
        for item in rel_r:
            rel_receiver.append(item.receiver.user)
        for item in rel_s:
            rel_sender.append(item.sender.user)
        context["rel_receiver"] = rel_receiver
        context["rel_sender"] = rel_sender
        context['posts'] = self.get_object().get_all_authors_posts()
        context['len_posts'] = True if len(
            self.get_object().get_all_authors_posts()) > 0 else False
        return context


class ProfileListView(LoginRequiredMixin, ListView):
    model = Profile
    template_name = 'profiles/profile_list.html'
    # context_object_name = 'qs'

    def get_queryset(self):
        qs = Profile.objects.get_all_profiles(self.request.user)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(username__iexact=self.request.user)
        profile = Profile.objects.get(user=user)
        rel_r = Relationship.objects.filter(sender=profile)
        rel_s = Relationship.objects.filter(receiver=profile)
        rel_receiver = []
        rel_sender = []
        for item in rel_r:
            rel_receiver.append(item.receiver.user)
        for item in rel_s:
            rel_sender.append(item.sender.user)
        context["rel_receiver"] = rel_receiver
        context["rel_sender"] = rel_sender
        context['is_empty'] = False
        if len(self.get_queryset()) == 0:
            context['is_empty'] = True

        return context


@login_required
def send_invatation(request):
    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        user = request.user
        sender = Profile.objects.get(user=user)
        receiver = Profile.objects.get(pk=pk)
        rel = Relationship.objects.create(
            sender=sender, receiver=receiver, status='send')
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('profiles:my-profile-view')


@login_required
def remove_from_friends(request):
    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        user = request.user
        sender = Profile.objects.get(user=user)
        receiver = Profile.objects.get(pk=pk)
        rel = Relationship.objects.get(
            (Q(sender=sender) & Q(receiver=receiver)) | (
                Q(sender=receiver) & Q(receiver=sender))
        )
        rel.delete()
        return redirect(request.META.get('HTTP_REFERER'))

    return redirect('profiles:my-profile-view')


# def search(request):
#     query = request.GET['query']
#     if len(query) > 78:
#         allPosts = Post.objects.none()
#     else:
#         allPostsTitle = Post.objects.filter(title__icontains=query)
#         allPostsAuthor = Post.objects.filter(author__icontains=query)
#         allPostsContent = Post.objects.filter(content__icontains=query)
#         allPosts = allPostsTitle.union(allPostsContent, allPostsAuthor)
#     if allPosts.count() == 0:
#         messages.warning(
#             request, "No search results found. Please refine your query.")
#     params = {'allPosts': allPosts, 'query': query}
#     return render(request, 'home/search.html', params)

# # these si the custion singup page


# def handleSignUp(request):
#     if request.method == "POST":
#         # Get the post parameters
#         username = request.POST['username']
#         email = request.POST['email']
#         fname = request.POST['fname']
#         lname = request.POST['lname']
#         pass1 = request.POST['pass1']
#         pass2 = request.POST['pass2']

#         # check for errorneous input
#         if len(username) >= 8:
#             messages.error(
#                 request, " Your user name must be under 10 characters")
#             return redirect('home')

#         if not username.isalnum():
#             messages.error(
#                 request, " User name should only contain letters and numbers")
#             return redirect('home')
#         if (pass1 != pass2):
#             messages.error(request, " Passwords do not match")
#             return redirect('home')

#         # Create the user
#         myuser = User.objects.create_user(username, email, pass1)
#         myuser.first_name = fname
#         myuser.last_name = lname
#         myuser.save()
#         messages.success(request, " Your iCoder has been successfully created")
#         return redirect('home')

#     else:
#         return HttpResponse("404 - Not found")


# def handeLogin(request):
#     if request.method == "POST":
#         # Get the post parameters
#         loginusername = request.POST['loginusername']
#         loginpassword = request.POST['loginpassword']

#         user = authenticate(username=loginusername, password=loginpassword)
#         if user is not None:
#             login(request, user)
#             messages.success(
#                 request, f"Successfully Logged In  {{request.user}}")
#             return redirect("home")
#         else:
#             messages.error(request, "Invalid credentials! Please try again")
#             return redirect("home")

#     return HttpResponse("404- Not found")
#     return HttpResponse("login")


# def handelLogout(request):
#     logout(request)
#     messages.success(request, "Successfully logged out")
#     return redirect('home')


# def about(request):
#     return render(request, "home/about.html")


# THESE IS FOR THE POST COMMENT AND FOR LIKE AND UNLIKE PURPOSE IN MYPROFILE

@login_required
def post_comment_create_and_list_view(request):
    qs = Post.objects.all()
    profile = Profile.objects.get(user=request.user)
    # initials / from ,comment and form
    p_form = PostModelForm()
    c_form = CommentModelForm()
    post_added = False

    profile = Profile.objects.get(user=request.user)

    if 'submit_p_form' in request.POST:
        print(request.POST)
        p_form = PostModelForm(request.POST, request.FILES)
        if p_form.is_valid():
            instance = p_form.save(commit=False)
            instance.author = profile
            instance.save()
            p_form = PostModelForm()
            post_added = True

    if 'submit_c_form' in request.POST:
        c_form = CommentModelForm(request.POST)
        if c_form.is_valid():
            instance = c_form.save(commit=False)
            instance.user = profile
            instance.post = Post.objects.get(id=request.POST.get('post_id'))
            instance.save()
            c_form = CommentModelForm()

    context = {
        'qs': qs,
        'profile': profile,
        'p_form': p_form,
        'c_form': c_form,
        'post_added': post_added,
    }
    return render(request, 'profiles/myprofile.html', context)


@login_required
def like_unlike_post(request):
    user = request.user
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post_obj = Post.objects.get(id=post_id)
        profile = Profile.objects.get(user=user)

        if profile in post_obj.liked.all():
            post_obj.liked.remove(profile)
        else:
            post_obj.liked.add(profile)

        like, created = Like.objects.get_or_create(
            user=profile, post_id=post_id)

        if not created:
            if like.value == 'Like':
                like.value = 'Unlike'
            else:
                like.value = 'Like'
        else:
            like.value = 'Like'

            post_obj.save()
            like.save()

        # return JsonResponse(data, safe=False)
    return redirect('profiles/myprofile.html')

# class PostDeleteView(LoginRequiredMixin, DeleteView):


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'posts/confirm_del.html'
    success_url = reverse_lazy('posts:main-post-view')
    success_url = '/posts/'

    def get_object(self, *args, **kwargs):
        pk = self.kwargs.get('pk')
        obj = Post.objects.get(pk=pk)
        if not obj.author.user == self.request.user:
            messages.warning(
                self.request, 'You need to be the author of the post in order to delete it')
        return obj

# class PostUpdateView(LoginRequiredMixin, UpdateView):


class PostUpdateView(LoginRequiredMixin, UpdateView):
    form_class = PostModelForm
    model = Post
    template_name = 'posts/update.html'
    success_url = reverse_lazy('posts:main-post-view')
    
    def form_valid(self, form):
        profile = Profile.objects.get(user=self.request.user)
        if form.instance.author == profile:
            return super().form_valid(form)
        else:
            form.add_error(
                None, "You need to be the author of the post in order to update it")
            return super().form_invalid(form)
