import os

from revue.models.mail import MailingAlias, YearGroupMailingList, PersistentGroupMailingList, MailingList


def generate_list_file(name, entries):
    filename = os.environ['EXIM_LISTS'] + '/' + name
    f = open(filename, 'w')
    for m in entries:
        print(m.get_address(), file=f)
    f.close()


def generate_list_files():
    # TODO: create files in new directory and replace target directory with this temporary directory
    for l in PersistentGroupMailingList.query.all():
        generate_list_file(l.get_local_address(), l.entries())
    for l in MailingList.query.all():
        generate_list_file(l.get_local_address(), l.entries)
    for l in YearGroupMailingList.query.all():
        base_filename = l.get_local_address()
        entries_list = l.get_entries_per_year()
        for ml in entries_list:
            generate_list_file(l.get_local_address_year(ml['year']), ml['entries'])
            # TODO: write symlink


def generate_alias_file():
    f = open(os.environ['EXIM_ALIASES'], 'w')
    for a in MailingAlias.query.all():
        print("{}: {}".format(a.get_local_address(), a.other_address().get_address()))
    f.close()


def generate_all_mail_files():
    generate_alias_file()
    generate_list_files()
