from flask_nav.elements import View

from revue.utilities.ui.bootstrap import CustomNavbar
from revue import nav

public_navbar = CustomNavbar(
    'Revue',
    [
        View('Home', '.index')
    ], [
        View('Intern', 'intern.index')
    ]
)
nav.register_element('public_navbar', public_navbar)
