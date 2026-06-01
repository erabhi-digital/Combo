from functools import wraps
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required


def membership_required(view_func):

    @wraps(view_func)
    @login_required
    def wrapper(request, *args, **kwargs):

        membership = getattr(request.user, "membership", None)

        # If membership does not exist
        if membership is None:
            return redirect("members:create_order")

        # Check expiry
        membership.check_status()

        if membership.is_active:
            return view_func(request, *args, **kwargs)

        return redirect("members:create_order")
    
    return wrapper