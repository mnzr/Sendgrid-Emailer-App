import rethinkdb as r
from rethinkdb.errors import RqlRuntimeError
from config import *

def setup_db():
    """to setup a DB"""
    connection = r.connect(host=HOST,
                           port=PORT)
    try:
        r.db_create(DB).run(connection)
        r.db(DB).table_create(TABLE).run(connection)
        print('Using newly created database.')
    except RqlRuntimeError:
        print('Using existing database.')
    finally:
        connection.close()


def delete_db():
    connection = r.connect(host=HOST,
                           port=PORT)
    try:
        r.db(DB).table(TABLE).delete().run(connection)
        print('Deleted table "{}" database.'.format(TABLE))
    except RqlRuntimeError:
        print('Could not delete table {}.'.format(TABLE))
    finally:
        connection.close()


def main():
    setup_db()

if __name__ == '__main__':
    main()
