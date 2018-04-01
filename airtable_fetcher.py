import airtable as at

class AirtableFetcher(object):

    def __init__(self, api_key):
        self.api_key = api_key

    def fetch_table_and_records(self, basekey, table_identifier, fields=None):
        table = at.Airtable(basekey, table_identifier, self.api_key)
        if fields == None:
            records = table.get_all()
        else:
            records = table.get_all(fields = fields)
        return {'table': table, 'records': records}


# refactor using ternary below later
# a if condition else b
