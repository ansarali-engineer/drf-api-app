from rest_framework.permissions import BasePermission


class HasRolePermission(BasePermission):

    message = "You do not have permission to perform this action."

    action_map = {
        "list": "can_view",
        "retrieve": "can_view",
        "create": "can_create",
        "update": "can_update",
        "partial_update": "can_update",
        "destroy": "can_delete",
    }

    def has_permission(self, request, view):

        if not request.user or not request.user.is_authenticated:
            return False
        print(request.user)
        screen_name = getattr(view, "permission_screen", None)

        if not screen_name:
            return False

        permission_field = self.action_map.get(view.action)

        if not permission_field:
            return False
        print(request.user.role.permissions)
        permission = request.user.role.permissions.filter(
            screen_name=screen_name
        ).first()
        if not permission:
            return False

        return getattr(permission, permission_field, False)