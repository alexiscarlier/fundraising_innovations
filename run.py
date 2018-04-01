# NOTES

# Should add a requirements file which install all the dependencies

import dokuwiki
import airtable as at
import os
from functools import reduce
import string
import re
import getpass

# muhkejwew31%
# keyklyto2SYSfTty6

# THE CLASSES I'M IMPORTING

import table_formatter
import airtable_fetcher

# THIS RUNS TO STORE PASSWORD AND USERKEY AS ENV VARIABLES

pss = getpass.getpass("Please enter your dokuwiki password: ")
os.environ['DOKUWIKI_PASS'] = pss
userkey = input("Please enter your airtable user key: ")
os.environ['AIRTABLE_API_KEY'] = userkey

# THIS IS ALL SET UP

# define a punctuation stripper for using later in pagename constructors
punctuation_translator = str.maketrans('', '', string.punctuation)

"""
Set up the APIs
"""

# for DokuWiki we need url, user name and password
usr = "alexiscarlier"  # this has to be added to the remoteuser in config:authentication

# the official DW
url = "http://localhost/~alexiscarlier/dokuwiki"
pss = os.environ['DOKUWIKI_PASS']

# for Airtable we need database key, user key and names of the requested tables
basekey_giving_researchers_shared = 'appBzOSifwBqSuVfH'
basekey_giving_impact = "apprleNrkR7dTtW60"

userkey = os.environ['AIRTABLE_API_KEY']

tools_sample = 'tools_public_sample'
theories = 'Theories'
papers = 'papers_mass'
ftse = "ftse100+givingpolicies"
experiments = "Charity experiments"


"""
Fetch the relevant tables from Airtable
"""

airtablefetcher = airtable_fetcher.AirtableFetcher(userkey)

tools_dict = airtablefetcher.fetch_table_and_records(basekey_giving_researchers_shared, tools_sample)
tools_records = tools_dict['records']

theories_dict = airtablefetcher.fetch_table_and_records(basekey_giving_researchers_shared, theories, ['Theory'])
theories_table = theories_dict['table']
theories_records = theories_dict['records']

"""
Initialize the wiki object
"""

wiki = dokuwiki.DokuWiki(url, usr, pss)


# STAND ALONE FUNCTION TO BE ENCAPSULATED LATER

def tool_row_constructor(record):
    """
    Construct a row for the tools table based on data delivered by Airtable.
    :param record: a single record from the Airtable
    :return: a formatted row for DW
    """
    tool_name = record['fields']['Toolname']
    page_name= tool_name.translate(punctuation_translator)
    tool_page_name = '[[iifwiki:tools:{}|{}]]'.format(page_name, tool_name)

    category = record['fields'].get('Category', [""])
    findings = record['fields'].get('Findings summarized', [""])

    if 'Theories' not in record['fields']:
        theory_names = ''
    else:
        theory_names = [theories_table.get(theory_id)['fields']['Theory'] for
                        theory_id in record['fields']['Theories']]
    row = "| " + tool_page_name + " | " + category[0] + " | " +\
        findings[0].rstrip() + " | " + ', '.join(theory_names) + " |\n"
    return row


# THIS IS THE CODE THAT RUNS AND DOES SOMETHING

tableformatter = table_formatter.TableFormatter()

tools_page_link = "start"
tools_page = wiki.pages.get(tools_page_link)
# define the header of the tools table
tools_header = "\n^ Tool name ^ Category ^ Description ^ Theories ^\n"
# create the new page content
tableformatter.format_table(tools_page, tools_header, tools_records, 'Toolname', tool_row_constructor)
new_tools_page = tableformatter.new_page
# publish it to DW
wiki.pages.set(tools_page_link, new_tools_page)


# Relies on the format_table, and tool_row_constructor
