from django.contrib.auth.mixins import UserPassesTestMixin


class IsAdminUserMixin(UserPassesTestMixin):
    """
        Mixin that restricts access to views based on the user's admin status.
    """

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_admin
