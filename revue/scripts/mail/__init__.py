import os

from revue.models.mail import MailingAlias, YearGroupMailingList, PersistentGroupMailingList


def generate_list_file(name, members):
    filename = os.environ['EXIM_LISTS'] + '/' + name
    print('Writing to file {}'.format(name))
    f = open(filename, 'w')
    for m in members:
        print(m.get_address(), file=f)
    f.close()


def generate_list_files():
    # TODO: create files in new directory and replace target directory with this temporary directory
    for l in PersistentGroupMailingList.query.all():
        generate_list_file(l.get_local_address(), l.members())
    for l in YearGroupMailingList.query.all():
        base_filename = l.get_local_address()
        members_lists = l.get_members_per_year()
        for ml in members_lists:
            generate_list_file(l.get_local_address_year(ml['year']), ml['members'])
            # TODO: write symlink


def generate_alias_file():
    f = open(os.environ['EXIM_ALIASES'], 'w')
    for a in MailingAlias.query.all():
        print("{}: {}".format(a.get_local_address(), a.other_address().get_address()))
    f.close()


def generate_all_mail_files():
    generate_alias_file()
    generate_list_files()
