from flask_nav.elements import View, Subgroup

from revue import nav
from revue.utilities.permissions import Permissions
from revue.utilities.ui.bootstrap import CustomNavbar, PermissionView

intern_navbar = CustomNavbar(
    'Revue',
    [
        View('Home', '.index'),
        View('Dit jaar', '.show_current_year'),
        View('Medewerkers', '.members'),
        View('Media', '.media')
    ], [

        View('Public', 'public.index'),
        PermissionView('Admin', 'admin.index', Permissions.ADMIN),
        Subgroup('Account',
                 View('Profiel', '.profile'),
                 View('Groups', '.view_own_groups'),
                 View('Logout', '.logout'),
                 ),
    ]
)
nav.register_element('intern_navbar', intern_navbar)
