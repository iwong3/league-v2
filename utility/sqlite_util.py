# sqlite-util.py stores helper functions for sqlite3

# get column names given sqlite cursor
def get_column_names(cursor):
    column_names = []
    for d in cursor.description:
        column_names.append(d[0])
    return column_names
