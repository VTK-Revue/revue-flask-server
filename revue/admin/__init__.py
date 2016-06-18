from flask_nav.elements import View, Subgroup

from revue import nav
from revue.utilities.ui.bootstrap import CustomNavbar

admin_navbar = CustomNavbar(
    'Revue',
    [
        View('Home', '.index'),
        View('Activations', '.registrations'),
        View('Users', '.all_users'),
        View('Groups', '.group_page'),
        Subgroup('Mail',
                 View('Lists', '.view_mailing_lists'),
                 View('Update files', '.generate_mail_lists'))
    ], [
        View('Intern', 'intern.index')
    ]
)
nav.register_element('admin_navbar', admin_navbar)
