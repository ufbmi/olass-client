"""
Goal: store utility function
"""
import logging
import pandas as pd
import sqlalchemy as db
from datetime import datetime
from urllib import parse
from olass.models.patient import Patient

log = logging.getLogger(__package__)
LINES_PER_CHUNK = 20000


def get_file_reader(file_path, columns, sep=','):
    """
    Get csv data in chunks with size defined by LINES_PER_CHUNK

    :param columns: dictionary mapping the destination <=> source columns
    """
    log.info("columns: {}".format(columns))
    reader = None
    source_columns = [col for col in columns.values()]

    try:
        reader = pd.read_csv(file_path,
                             sep=sep,
                             dtype=object,
                             skipinitialspace=True,
                             skip_blank_lines=True,
                             usecols=source_columns,
                             chunksize=LINES_PER_CHUNK,
                             iterator=True)
        return reader
    except ValueError as exc:
        log.error("Please check if the column names match: {}"
                  "\nError: {}".format(source_columns, exc))
    return reader


def get_db_url_sqlserver(db_host, db_port, db_name, db_user, db_pass):
    """
    Helper function for creating the "pyodbc" connection string.

    @see http://docs.sqlalchemy.org/en/latest/dialects/mssql.html
    @see https://code.google.com/p/pyodbc/wiki/ConnectionStrings
    """
    params = parse.quote(
        "Driver={{FreeTDS}};Server={};Port={};"
        "Database={};UID={};PWD={};"
        .format(db_host, db_port, db_name, db_user, db_pass))
    return 'mssql+pyodbc:///?odbc_connect={}'.format(params)


def get_db_url_mysql(config):
    return 'mysql+mysqlconnector://{}:{}@{}/{}' \
        .format(config['DB_USER'],
                config['DB_PASS'],
                config['DB_HOST'],
                config['DB_NAME'])

def get_db_engine(config):
    """
    @see http://docs.sqlalchemy.org/en/latest/core/connections.html
    """
    db_name = config['DB_NAME']
    url = get_db_url_mysql(config)
    engine = db.create_engine(url,
                              pool_size=10,
                              max_overflow=5,
                              pool_recycle=3600,
                              echo=False)
    try:
        engine.execute("USE {}".format(db_name))
    except db.exc.OperationalError:
        print('Database {} does not exist.'.format(db_name))
    return engine


def serialize_data_frame(config, df, entity):
    """
    Write the frame to the specific entity table
    """
    engine = get_db_engine(config)
    records = df.to_dict(orient='records')
    result = engine.execute(entity.__table__.insert(), records)
    return result


def _format_date(val, fmt):
    """
    :param val: the input string for date
    :param fmt: the input format for the date
    """
    if not val:
        return None

    fmt_out = '%Y-%m-%d'

    try:
        d = datetime.strptime(val, fmt)
    except Exception:
        log.warning("Problem formatting date: {} {}".format(val, fmt))
        return None

    return d.strftime(fmt_out)


def process_frame(df_source, columns, config):
    """
    Apply column-specific logic (data transformation/filtering)
    """
    df_source.fillna('', inplace=True)
    df_size = min(LINES_PER_CHUNK, df_source.index.max() + 1)
    df = create_data_frame(columns.keys(), df_size)

    for col, source_col in columns.items():
        # log.info("Parsing df[{}] = .. from {}".format(col, source_col))
        if 'pat_birth_date' == col:
            df[col] = df_source[source_col].map(
                lambda x: _format_date(x, fmt='%m/%d/%Y'))
        else:
            df[col] = df_source[source_col]

    if config['SEND_TO_DB']:
        # write the records to the database
        serialize_data_frame(config, df, Patient)

    return df


def process_reader_data(reader, columns, config):
    """
    TODO: Make it process in paralel
    """
    frames = []

    for index, df_source in enumerate(reader):
        log.info("Process frame: {}".format(index))
        df = process_frame(df_source, columns, config)
        frames.append(df)

    return pd.concat(frames, ignore_index=True)


def create_data_frame(columns, index_size=0, do_fill=True):
    """"
    :param columns: the names of the columns
    :param index_size: how many rows
    :param do_fill: flag for filling the data frame with empty strings
    """
    index = range(index_size)
    df = pd.DataFrame(index=index, columns=columns)

    if do_fill:
        df.fillna('', inplace=True)
    return df


def write_data_frame(df, file_path, sep=','):
    """
    Store the dataframe to a file
    """
    try:
        df.to_csv(file_path, sep=sep, index=False, encoding='utf-8')
    except Exception as exc:
        print("Problem writing file {} due: \n{}".format(file_path, exc))
        raise exc
    return True


def import_voter_data(file_path, columns, out_file, config):
    """
    Extract `columns` from the csv file specified by `file_path`
    and store them to to a file, and optionally to the database.
    """
    reader = get_file_reader(file_path, columns)
    df = process_reader_data(reader, columns, config)
    log.info("Done with processing... Writing the output file: {}"
             .format(out_file))
    success = write_data_frame(df, out_file)

    if success:
        log.info('Wrote result file: {}'.format(out_file))
    else:
        log.error("Failed to write file: {}".format(out_file))
