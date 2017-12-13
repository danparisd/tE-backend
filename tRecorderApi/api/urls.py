from django.conf.urls import url
from rest_framework import routers

from api.views.zip import ZipViewSet
from api.views.tr import TrViewSet
from . import views
from .views import (
    book, language,
    version, anthology, index,
    resumable_upload, all_projects,
    ProjectViewSet)

router = routers.DefaultRouter()
router.register(r'projects', ProjectViewSet)
# router.register(r'chapters', views.ChapterViewSet)
# router.register(r'chunks', views.ChunkViewSet)
# router.register(r'languages', views.LanguageViewSet)
router.register(r'books', book.BookViewSet)
# router.register(r'languages', language.LanguageViewSet)
# router.register(r'books', views.BookViewSet)
# router.register(r'users', views.UserViewSet)
router.register(r'takes', views.TakeViewSet)
router.register(r'comments', views.CommentViewSet)
router.register(r'anthologies', views.AnthologyViewSet)
router.register(r'zip', ZipViewSet)
router.register(r'tr', TrViewSet)

urlpatterns = [
    url(r'^$', index.index, name='index'),
    url(r'^upload/(?P<filename>[^/]+)$',
        views.file_upload.FileUploadView.as_view()),
    url(r'^resumable_upload/(?P<filename>[^/]+)/$',
        views.resumable_upload.ResumableFileUploadView.as_view()),
    # url(r'^source/(?P<filename>[^/]+)$',
    # views.UploadSourceFileView.as_view()),
    # url(r'^get_project_takes/$', views.GetProjectTakesView.as_view()),
    # url(r'^update_project_takes/$', views.UpdateProjectTakesView.as_view()),
    # url(r'^exclude_files/$', views.ExcludeFilesView.as_view()),
    # url(r'^all_projects/$', all_projects.AllProjectsView.as_view()),
    url(r'^get_chapters/$', views.ProjectChapterInfoView.as_view()),
    url(r'^get_langs/$', views.language.GetLanguages.as_view()),
    url(r'^get_versions/$', views.version.GetVersions.as_view()),
    url(r'^get_anthologies/$', views.anthology.GetAnthologies.as_view()),
    # url(r'^get_books/$', views.getBooksView.as_view()),
    # url(r'^push_takes/$', views.PushTakesView.as_view()),
    # url(r'^stitch_takes/$', views.SourceStitchView.as_view()),
    url(r'^get_chunks/$', views.GetChunks.as_view()),
    url(r'^get_takes/$', views.GetTakes.as_view()),
    url(r'^get_comments/$', views.GetComments.as_view()),
    url(r'^get_books/$', views.book.GetBooksView.as_view()),
    # url(r'^languages/$',languageView.languages),
    url(r'^get_projects/$', all_projects.GetProjectsView.as_view()),
]

urlpatterns += router.urls
