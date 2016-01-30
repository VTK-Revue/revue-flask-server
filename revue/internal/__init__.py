from flask_nav.elements import View, Subgroup

from revue import nav
from revue.utilities.permissions import Permissions
from revue.utilities.ui.bootstrap import CustomNavbar, PermissionView

intern_navbar = CustomNavbar(
    'Revue',
    [
        View('Home', '.index'),
        View('Activiteiten', '.activities'),
        View('Script', '.script'),
        View('Medewerkers', '.members'),
        View('Media', '.media')
    ], [
        Subgroup('Account',
                 View('Profiel', '.profile'),
                 View('Groups', '.view_own_groups')
        ),
        PermissionView('Admin', 'admin.index', Permissions.ADMIN),
        View('Logout', '.logout'),
        View('Public', 'public.index')
    ]
)
nav.register_element('intern_navbar', intern_navbar)
