from django.http import Http404
from django.apps import apps
from rest_framework.permissions import BasePermission
from apps.users import models


class IsWorker(BasePermission):
    """
        Allows access only to admin users or Worker.
    """

    def has_permission(self, request, view):
        user = request.user
        if user.is_staff:
            has_permission = True
        else:
            try:
                worker = models.Worker.objects.get(id=user.id)
                if worker:
                    has_permission = True
            except:
                has_permission = False
        if has_permission:
            return request.user and (worker or request.user.is_staff)
        else:
            raise Http404


def is_owner(app, model_name):
    """
    User View Restriction Decorator. It provides permissions if the logged
    in user is administrator, or if it is the owner of the object
    """

    def _is_owner(f):

        def inner(*args, **kwargs):

            model = apps.get_model(app, model_name)
            model_id = kwargs.get('pk')

            try:
                user = args[0].request.user
            except:
                user = args[0].user

            has_permission = False

            if user.is_staff:
                has_permission = True
            else:
                try:
                    model_obj = model.objects.get(id=model_id)
                    if model_obj.worker.id == user.id:
                        has_permission = True
                    else:
                        has_permission = False
                except:
                    has_permission = False

            if has_permission:
                r = f(*args, **kwargs)
            else:
                raise Http404
            return r
        return inner
    return _is_owner
