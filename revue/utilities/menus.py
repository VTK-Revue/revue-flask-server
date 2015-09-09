from revue.models.menus import MenuEntryRelationship, MenuEntry


def get_menu_structure(menu_entry):
    if menu_entry is None:
        return None
    children = MenuEntryRelationship.query.filter_by(parent_id=menu_entry.id)
    return {
        'title': menu_entry.title,
        'page': menu_entry.page,
        'description': menu_entry.description,
        'children': [get_menu_structure(MenuEntry.query.get(x.child_id)) for x in children]
    }
