tools_page_link = "start"
tools_page = wiki.pages.get(tools_page_link)
# define the header of the tools table
tools_header = "\n^ Tool name ^ Category ^ Description ^ Theories ^\n"
# create the new page content
new_tools_page = format_table(tools_page, tools_header, tools_records, 'Toolname', tool_row_constructor)
# publish it to DW
wiki.pages.set(tools_page_link, new_tools_page)


# Relies on the format_table, and tool_row_constructor




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
