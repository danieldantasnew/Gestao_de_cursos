from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

app_name = 'catalogo'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login', views.login, name='login'),
    path('login', views.logout, name='logout'),

    path('perfis', views.perfis, name='perfis'),
    path('perfis/<uuid:id>/', views.perfil_detalhe, name='perfis-detalhe'),
    path('perfis/novo', views.criar_perfil, name='perfis-novo'),
    path('perfis/<uuid:id>/editar', views.editar_perfil, name='perfis-editar'),
    path('perfis/<uuid:id>/inativar/', views.inativar_perfil, name='perfis-inativar'),
    path('perfis/<uuid:id>/ativar/', views.ativar_perfil, name='perfis-ativar'),


    path('cursos', views.cursos, name='cursos'),
    path('cursos/novo', views.criar_curso, name='cursos-novo'),
    path('cursos/<uuid:id>/editar', views.editar_curso, name='cursos-editar'),
    path('cursos/<uuid:id>/', views.curso_detalhe, name='cursos-detalhe'),
    path('cursos/<uuid:id>/resumo/', views.cursos_resumo, name='cursos-resumo'),
    path('cursos/<uuid:id>/inativar/', views.inativar_curso, name='cursos-inativar'),
    path('cursos/<uuid:id>/ativar/', views.ativar_curso, name='cursos-ativar'),


    path('disciplinas', views.disciplinas, name='disciplinas'),
    path('disciplinas/novo', views.criar_disciplina, name='disciplinas-novo'),
    path('disciplinas/<uuid:id>/editar', views.editar_disciplina, name='disciplinas-editar'),
    path('disciplinas/<uuid:id>/inativar/', views.inativar_disciplina, name='disciplinas-inativar'),
    path('disciplinas/<uuid:id>/ativar/', views.ativar_disciplina, name='disciplinas-ativar'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)