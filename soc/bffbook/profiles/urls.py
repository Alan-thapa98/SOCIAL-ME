from django.urls import path
from .views import (
    my_profile_view,
    invites_received_view,
    profiles_list_view,
    invite_profiles_list_view,
    ProfileDetailView,
    ProfileListView,
    send_invatation,
    remove_from_friends,
    accept_invatation,
    reject_invatation,
    # handleSignUp,
    # handeLogin,
    # handelLogout,
    # THESE IS FOR THE PSOT
    post_comment_create_and_list_view,
    like_unlike_post, PostDeleteView,
    PostUpdateView,

)
from .views import my_profile_view_edit
app_name = 'profiles'


app_name = 'posts'

urlpatterns = [

]

urlpatterns = [
    path('', ProfileListView.as_view(), name='all-profiles-view'),
    path('myprofile/', my_profile_view, name='my-profile-view'),
    path('my-invites/', invites_received_view, name='my-invites-view'),
    path('to-invite/', invite_profiles_list_view, name='invite-profiles-view'),
    path('send-invite/', send_invatation, name='send-invite'),
    path('remove-friend/', remove_from_friends, name='remove-friend'),
    path('<slug>/', ProfileDetailView.as_view(), name='profile-detail-view'),
    path('my-invites/acctept/', accept_invatation, name='accept-invite'),
    path('my-invites/reject/', reject_invatation, name='reject-invite'),
    # THESE IS CREATED BY ME FOR THE DEMO AND TEST AND BATTER FUNCTIONS
    path('myprofile/profile_edite', my_profile_view_edit,
         name='my-profile-view-edit'),
    # sing up in loge in
    # path('/signup', handleSignUp, name="handleSignUp"),
    # path('/login', handeLogin, name="handleLogin"),
    # path('/logout', handelLogout, name="handleLogout"),




    # THESE IS FOR THE POSTS

]


# urlpatterns = [
#     path('myprofile/', my_profile_view, name='my-profile-view'),
#     path('my-invites/', invites_received_view, name='my-invites-view'),
#     path('to-invite/', invite_profiles_list_view, name='invite-profiles-view'),
#     path('send-invite/', send_invatation, name='send-invite'),
#     path('remove-friend/', remove_from_friends, name='remove-friend'),

#     path('my-invites/acctept/', accept_invatation, name='accept-invite'),
#     path('my-invites/reject/', reject_invatation, name='reject-invite'),

#     path('all-profiles/', ProfileListView.as_view(), name='all-profiles-view'),

#     # excptions
#     # path('all-profiles/', profiles_list_view, name='all-profiles-view'),
#     # end of excptions

#     # path('', ProfileListView.as_view(), name='all-profiles-view'),
#     # path('<slug>/', ProfileDetailView.as_view(), name='profile-detail-view'),


# ]
