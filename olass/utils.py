"""
Goal: store utility functions
"""
import sys
import unicodedata
import logging
import pandas as pd
import sqlalchemy as db
from hashlib import sha256
from datetime import datetime
from datetime import date
from olass.models.patient import Patient

log = logging.getLogger(__package__)
# FORMAT_US_DATE = "%x"
# FORMAT_US_DATE_TIME = '%x %X'
FORMAT_DATABASE_DATE = "%Y-%m-%d"
FORMAT_DATABASE_DATE_TIME = "%Y-%m-%d %H:%M:%S"

LINES_PER_CHUNK = 20000

# table of punctuation characters + space
tbl = dict.fromkeys(i for i in range(sys.maxunicode)
                    if unicodedata.category(chr(i)).startswith('P') or
                    chr(i) in [' '])


def prepare_for_hashing(text):
    if not text:
        return ''
    return text.translate(tbl).lower()


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

    # def get_db_url_sqlserver(db_host, db_port, db_name, db_user, db_pass):
    #     """
    #     Helper function for creating the "pyodbc" connection string.
    #
    #     @see http://docs.sqlalchemy.org/en/latest/dialects/mssql.html
    #     @see https://code.google.com/p/pyodbc/wiki/ConnectionStrings
    #     """
    #     from urllib import parse
    #     params = parse.quote(
    #         "Driver={{FreeTDS}};Server={};Port={};"
    #         "Database={};UID={};PWD={};"
    #         .format(db_host, db_port, db_name, db_user, db_pass))
    #     return 'mssql+pyodbc:///?odbc_connect={}'.format(params)


def get_db_url_mysql(config):
    if 'DB_URL_TESTING' in config:
        return config['DB_URL_TESTING']

    return 'mysql+mysqlconnector://{}:{}@{}/{}' \
        .format(config['DB_USER'],
                config['DB_PASS'],
                config['DB_HOST'],
                config['DB_NAME'])


def get_db_engine(config):
    """
    @see http://docs.sqlalchemy.org/en/latest/core/connections.html
    """
    # TODO: add support for connecting to sqlserver
    db_name = config.get('DB_NAME')
    url = get_db_url_mysql(config)

    try:
        engine = db.create_engine(url,
                                  pool_size=10,
                                  max_overflow=5,
                                  pool_recycle=3600,
                                  echo=False)
    except TypeError as exc:
        log.warn("Got exc from db.create_engine(): {}".format(exc))
        engine = db.create_engine(url, echo=False)

    try:
        engine.execute("USE {}".format(db_name))
    except db.exc.OperationalError:
        log.warn('Cannot select [{}] database.'.format(db_name))
    return engine


def serialize_data_frame(config, df, entity):
    """
    Write the frame to the specific entity table
    """
    engine = get_db_engine(config)
    records = df.to_dict(orient='records')
    result = engine.execute(entity.__table__.insert(), records)
    return result


def format_date_as_string(val, fmt='%m-%d-%Y'):
    """
    :rtype str:
    :return the input value formatted as '%Y-%m-%d'

    :param val: datetime or string
    :param fmt: the input format for the date
    """
    if isinstance(val, date):
        return val.strftime(fmt)

    da = format_date(val, fmt)

    if not da:
        return ''

    return da.strftime(FORMAT_DATABASE_DATE)


def format_date(val, fmt='%m-%d-%Y'):
    """
    Transform the input string to a datetime object

    :param val: the input string for date
    :param fmt: the input format for the date
    """
    date = None

    try:
        date = datetime.strptime(val, fmt)
    except Exception as exc:
        log.warning("Problem formatting date: {} - {} due: {}"
                    .format(val, fmt, exc))

    return date


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
                lambda x: format_date(x, fmt='%m/%d/%Y'))
        else:
            df[col] = df_source[source_col]

    if config['SEND_TO_DB']:
        # write the records to the database
        serialize_data_frame(config, df, Patient)

    return df


def process_reader_data(reader, columns, config):
    """
    For each chunk of the original file call `meth`:process_frame
    """
    # TODO: Use paralel processing
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


def apply_sha256(val):
    """ Compute sha256 sum
    :param val: the input string
    :rtype string: the sha256 hexdigest
    """
    m = sha256()
    m.update(val.encode('utf-8'))
    return m.hexdigest()
