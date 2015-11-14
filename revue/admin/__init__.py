from flask_nav.elements import View

from revue import nav
from revue.utilities.ui.bootstrap import CustomNavbar

admin_navbar = CustomNavbar(
    'Revue',
    [
        View('Home', '.index'),
        View('Activations', '.registrations'),
        View('Users', '.all_users'),
        View('Groups', '.group_page')
    ], [
        View('Intern', 'intern.index')
    ]
)
nav.register_element('admin_navbar', admin_navbar)
