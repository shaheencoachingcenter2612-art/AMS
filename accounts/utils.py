from functools import wraps

from django.contrib import messages
from django.shortcuts import redirect


# =========================================================
# GET USER ROLE
# =========================================================

def get_user_role(user):
    """
    Returns the application role of the logged-in user.

    Superusers are always treated as Super Admin.
    """

    if not user.is_authenticated:
        return None

    if user.is_superuser:
        return "Super Admin"

    try:
        return user.profile.role
    except Exception:
        return None


# =========================================================
# ROLE REQUIRED DECORATOR
# =========================================================

def role_required(*allowed_roles):
    """
    Restrict a view to specific application roles.

    Example:

        @role_required("Super Admin", "Vice Principal")
        def my_view(request):
            ...
    """

    def decorator(view_func):

        @wraps(view_func)
        def wrapper(request, *args, **kwargs):

            # -------------------------------------------------
            # LOGIN REQUIRED
            # -------------------------------------------------

            if not request.user.is_authenticated:

                return redirect(
                    "accounts:login"
                )

            # -------------------------------------------------
            # SUPER ADMIN HAS FULL ACCESS
            # -------------------------------------------------

            if request.user.is_superuser:

                return view_func(
                    request,
                    *args,
                    **kwargs
                )

            # -------------------------------------------------
            # GET ROLE
            # -------------------------------------------------

            role = get_user_role(
                request.user
            )

            # -------------------------------------------------
            # NO ROLE
            # -------------------------------------------------

            if not role:

                messages.error(
                    request,
                    "Your account does not have a role assigned. "
                    "Please contact the administrator."
                )

                return redirect(
                    "website:dashboard"
                )

            # -------------------------------------------------
            # CHECK PERMISSION
            # -------------------------------------------------

            if role not in allowed_roles:

                messages.error(
                    request,
                    "You do not have permission to access this page."
                )

                return redirect(
                    "website:dashboard"
                )

            return view_func(
                request,
                *args,
                **kwargs
            )

        return wrapper

    return decorator


# =========================================================
# PERMISSION MATRIX
# =========================================================

ROLE_PERMISSIONS = {

    "Super Admin": {

        "dashboard",
        "students",
        "teachers",
        "academics",
        "attendance",
        "teacher_diary",
        "results",
        "fees",
        "salary",
        "timetable",
        "accounts",
        "reports",
    },

    "Vice Principal": {

        "dashboard",
        "students",
        "teachers",
        "academics",
        "attendance",
        "teacher_diary",
        "results",
        "timetable",
        "reports",
    },

    "Teacher": {

        "dashboard",
        "attendance",
        "teacher_diary",
        "results",
        "timetable",
        "students",
    },

    "Accountant": {

        "dashboard",
        "fees",
        "salary",
        "students",
        "reports",
    },
}


# =========================================================
# MODULE PERMISSION CHECK
# =========================================================

def has_permission(user, permission):
    """
    Check whether a user has access to a particular module.

    Example:

        has_permission(request.user, "fees")
    """

    if not user.is_authenticated:
        return False

    if user.is_superuser:
        return True

    role = get_user_role(user)

    if not role:
        return False

    return permission in ROLE_PERMISSIONS.get(
        role,
        set()
    )


# =========================================================
# MODULE REQUIRED DECORATOR
# =========================================================

def permission_required(permission):
    """
    Restrict a view according to the central permission matrix.

    Example:

        @permission_required("fees")
        def fee_list(request):
            ...
    """

    def decorator(view_func):

        @wraps(view_func)
        def wrapper(request, *args, **kwargs):

            if not request.user.is_authenticated:

                return redirect(
                    "accounts:login"
                )

            if not has_permission(
                request.user,
                permission
            ):

                messages.error(
                    request,
                    "You do not have permission to access this module."
                )

                return redirect(
                    "website:dashboard"
                )

            return view_func(
                request,
                *args,
                **kwargs
            )

        return wrapper

    return decorator