from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('',views.IndexView.as_view(),name='home'),

    path('profile/<int:pk>/',views.ProfileView.as_view(),name='profile'),
    path('profile/edit/<slug:slug>/<int:pk>',views.EditProfileView.as_view(),name='edit_profile'),
    path('notifications',views.NotificationView.as_view(),name='notification'),
    path('post/<int:pk>',views.notification_view,name="view_notification"),
    path('<int:pk>/',views.view_notification,name="is_viewed"),
    path('process_notification/',views.change_notification,name="is_read"),
    
    path('posts/edit/<int:pk>/',views.EditPostView.as_view(),name='edit_post'),
    # path('posts/delete/<int:pk>/',views.DeletePost.as_view(),name='delete_post'),
    path('posts/delete/<int:pk>/',views.delete_post,name='delete_post'),
    path('logout/',views.logout_user,name='logout'),
    path('messages/',views.message_view,name='all_messages'),
    path('messages/<str:username>/',views.read_message,name='read_message'),
    # path('notifications/unread/all/',views.get_counts,name='get_counts'),

    path('notification/subscribe/<int:id>/',views.subscribe_notification,name='subscribe_notification'),
    path('notification/disable/<int:id>/',views.disable_notification,name='disable_notification'),

    path('chat_user/',views.chat_user,name='chat_user'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
