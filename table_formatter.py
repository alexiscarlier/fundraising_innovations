class TableFormatter(object):

    def __init__(self):
        self.new_page = None


    def format_table(self, page_content, header, records, main_column, constructor):
        # define the relevant portion of the page, whatever is between the datatables tags
        # we're assuming for now there's one table per page
        start_tag = '<datatables>'
        end_tag = '</datatables>'
        start_index = page_content.find(start_tag) + len(start_tag)
        end_index = page_content.find(end_tag)

        # initialize table content with the header
        table_content = header
        # construct the rows for all available records using the corresponding constructor function
        for record in records:
            # we only consider records in which the main column is not empty
            if main_column not in record['fields']:
                pass
            else:
                table_content += constructor(record)

        # combine the table with the rest of the page
        new_page = page_content[:start_index] + table_content + page_content[end_index:]
        self.new_page = new_page
