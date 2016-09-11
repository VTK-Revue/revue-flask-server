import os
import time

from revue.models.mail import MailingAlias, YearGroupMailingList, PersistentGroupMailingList, MailingList
from revue.models.general import RevueYear
from revue.utilities import groups


def generate_list_file(name, entries):
    filename = os.environ['EXIM_LISTS'] + '/' + name
    f = open(filename, 'w')
    for m in entries:
        print(m.get_address(), file=f)
    f.close()


def generate_list_files():
    # TODO: create files in new directory and replace target directory with this temporary directory
    # Currently existing files are never removed
    for l in PersistentGroupMailingList.query.all():
        generate_list_file(l.get_local_address(), l.entries())
    for l in MailingList.query.all():
        entries = list(l.entries)
        address = l.get_local_address()
        generate_list_file(address, entries)
    current_year = int(os.environ['CURRENT_YEAR'])
    for l in YearGroupMailingList.query.all():
        base_filename = l.get_local_address()
        entries_list = l.get_entries_per_year()
        for ml in entries_list:
            generate_list_file(l.get_local_address_year(ml['year']), ml['entries'])
            if ml['year'] == current_year:
                generate_list_file(base_filename, ml['entries'])
    for year in RevueYear.query.all():
        year_participations = groups.get_year_participations(year)
        entries = [participation.user().email() for participation in year_participations]
        generate_list_file("all_{}".format(year.year), entries)
        if year.year == current_year:
            generate_list_file("all", entries)


def generate_alias_file():
    f = open(os.environ['EXIM_ALIASES'], 'w')
    for a in MailingAlias.query.all():
        print("{}: {}".format(a.get_local_address(), a.other_address().get_address()))
    f.close()


def generate_all_mail_files():
    print("Generating all mail files. ({})".format(time.strftime("%A, %d. %B %Y %I:%M:%S %p")))
    generate_alias_file()
    generate_list_files()
