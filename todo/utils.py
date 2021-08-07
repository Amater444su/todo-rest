from todo.models import (
    Groups, Profile
)


def UserInGroupOr403(user, group):
    if user not in group.users.all():
        raise PermissionDenied
