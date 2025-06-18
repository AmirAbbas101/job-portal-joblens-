from functools import wraps

from django.shortcuts import render


def recruiter(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Check if the user is authenticated and has the recruiter role
        if request.user.is_authenticated and hasattr(request.user, "role"):
            if request.user.role == "RE":
                return view_func(request, *args, **kwargs)

        # If user is not authorized, return forbidden response
        return render(request, "permission-denied.html")

    return _wrapped_view
