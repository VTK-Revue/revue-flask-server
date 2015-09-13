from revue import nav
from flask_nav.elements import View
from revue.utilities.ui.bootstrap import CustomNavbar

intern_navbar = CustomNavbar(
    'Revue',
    [
        View('Home', '.index'),
        View('Activiteiten', '.activities'),
        View('Script', '.script'),
        View('Medewerkers', '.members'),
        View('Media', '.media')
    ],[
        View('Logout', '.logout'),
        View('Public', 'public.index')
    ]
)
nav.register_element('intern_navbar', intern_navbar)


