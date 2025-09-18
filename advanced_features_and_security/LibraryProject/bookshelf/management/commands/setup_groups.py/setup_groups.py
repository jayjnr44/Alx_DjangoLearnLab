from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from relationship_app.models import Book

class Command(BaseCommand):
    help = "Set up default groups and assign permissions"

    def handle(self, *args, **kwargs):
        # Clear existing groups
        Group.objects.all().delete()

        # Create groups
        editors, _ = Group.objects.get_or_create(name="Editors")
        viewers, _ = Group.objects.get_or_create(name="Viewers")
        admins, _ = Group.objects.get_or_create(name="Admins")

        # Get permissions
        can_view = Permission.objects.get(codename="can_view")
        can_create = Permission.objects.get(codename="can_create")
        can_edit = Permission.objects.get(codename="can_edit")
        can_delete = Permission.objects.get(codename="can_delete")

        # Assign permissions
        viewers.permissions.add(can_view)
        editors.permissions.add(can_view, can_create, can_edit)
        admins.permissions.add(can_view, can_create, can_edit, can_delete)

        self.stdout.write(self.style.SUCCESS("Groups and permissions have been set up."))
