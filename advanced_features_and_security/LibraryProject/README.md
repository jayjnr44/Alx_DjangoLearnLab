# LibraryProject

This is a Django project called LibraryProject.

## Setup

1. Install Django: `pip install django`
2. Start the development server: `python manage.py runserver`
3. Visit [http://127.0.0.1:8000/](http://127.0.0.1:8000/) to view the default Django welcome page.

# Permissions & Groups Setup

- **Custom permissions** are defined in `Book.Meta.permissions`.
- Groups:
  - **Viewers** → can_view
  - **Editors** → can_view, can_create, can_edit
  - **Admins** → can_view, can_create, can_edit, can_delete
- Run `python manage.py setup_groups` to auto-create groups.
- Views are protected with `@permission_required`.
- Assign users to groups via the Django Admin.
