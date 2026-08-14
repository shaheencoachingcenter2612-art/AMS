from django.urls import path

from . import views


app_name = "academics"


urlpatterns = [

    # =====================================================
    # ACADEMICS DASHBOARD
    # =====================================================

    path(
        "",
        views.academics_dashboard,
        name="dashboard",
    ),


    # =====================================================
    # SESSIONS
    # =====================================================

    path(
        "sessions/",
        views.session_list,
        name="session_list",
    ),

    path(
        "sessions/add/",
        views.add_session,
        name="add_session",
    ),

    path(
        "sessions/<int:pk>/edit/",
        views.edit_session,
        name="edit_session",
    ),

    path(
        "sessions/<int:pk>/delete/",
        views.delete_session,
        name="delete_session",
    ),


    # =====================================================
    # CLASSROOMS
    # =====================================================

    path(
        "classes/",
        views.classroom_list,
        name="classroom_list",
    ),

    path(
        "classes/add/",
        views.add_classroom,
        name="add_classroom",
    ),

    path(
        "classes/<int:pk>/edit/",
        views.edit_classroom,
        name="edit_classroom",
    ),

    path(
        "classes/<int:pk>/delete/",
        views.delete_classroom,
        name="delete_classroom",
    ),


    # =====================================================
    # SECTIONS
    # =====================================================

    path(
        "sections/",
        views.section_list,
        name="section_list",
    ),

    path(
        "sections/add/",
        views.add_section,
        name="add_section",
    ),

    path(
        "sections/<int:pk>/edit/",
        views.edit_section,
        name="edit_section",
    ),

    path(
        "sections/<int:pk>/delete/",
        views.delete_section,
        name="delete_section",
    ),


    # =====================================================
    # SUBJECTS
    # =====================================================

    path(
        "subjects/",
        views.subject_list,
        name="subject_list",
    ),

    path(
        "subjects/add/",
        views.add_subject,
        name="add_subject",
    ),

    path(
        "subjects/<int:pk>/edit/",
        views.edit_subject,
        name="edit_subject",
    ),

    path(
        "subjects/<int:pk>/delete/",
        views.delete_subject,
        name="delete_subject",
    ),

]