from functools import wraps

from django.contrib import messages
from django.shortcuts import redirect


def role_required(*allowed_roles):

    def decorator(view_func):

        @wraps(view_func)
        def wrapper(request, *args, **kwargs):

            if not request.user.is_authenticated:
                return redirect("accounts:login")

            # Superuser always has full access
            if request.user.is_superuser:
                return view_func(
                    request,
                    *args,
                    **kwargs
                )

            try:
                role = request.user.profile.role
            except Exception:
                messages.error(
                    request,
                    "Your account does not have a role assigned."
                )
                return redirect("dashboard")

            if role not in allowed_roles:

                messages.error(
                    request,
                    "You do not have permission to access this page."
                )

                return redirect("dashboard")

            return view_func(
                request,
                *args,
                **kwargs
            )

        return wrapper

    return decorator