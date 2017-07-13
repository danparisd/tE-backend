from django.conf.urls import url, include
#from . import views_sets
from rest_framework import routers
from .views_sets import *

router = routers.DefaultRouter()
router.register(r'languages', LanguageViewSet)
router.register(r'books', BookViewSet)
router.register(r'users', UserViewSet)
router.register(r'takes', TakeViewSet)
router.register(r'comments', CommentViewSet)
 
urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^upload/(?P<filename>[^/]+)$', FileUploadView.as_view()),
    url(r'^stream/(?P<filepath>.*)$', FileStreamView.as_view()),
    url(r'^get_project/$', ProjectView.as_view()),
    url(r'^get_source/$', SourceFileView.as_view()),
    url(r'^source/(?P<filename>[^/]+)$', SourceFileView.as_view()),
    url(r'^zipFiles/$', ProjectZipFilesView.as_view()),
    url(r'^exclude_files/$', ExcludeFilesView.as_view()),
    url(r'^all_project/$', AllProjectsView.as_view()),
    url(r'^get_chapters/$', ProjectChapterInfoView.as_view())
]

urlpatterns += router.urls
