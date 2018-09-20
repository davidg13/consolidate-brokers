# Python 3 compatible
import csv
import itertools
import random

MIN_SIMILARITY = 0.75

def load_file(filename):
    """Read a csv file into a dict representing the records.
    params:
        filename - relative path of the csv to read
    returns: (dict) - a dictionary with headers, records, and count
    """
    records = []
    line_count = 0
    with open(filename, encoding='utf-8') as brokers_csv:
        csv_reader = csv.reader(brokers_csv, delimiter=',')
        for row in csv_reader:
            # read the first row as the headers
            if line_count == 0:
                headers = tuple(row)
            else:
                records.append(tuple(row))
            line_count += 1
    return {
        'headers': headers,
        'records': records,
        'count': line_count - 1
    }

def write_file(filename, records):
    with open(filename, 'w') as output_file:
        writer = csv.writer(output_file)
        for record in records:
            writer.writerow(record)

def create_hash_vector(record, hash_mod):
    """Create a list of hash numbers for the record
    params:
        record - a tuple of primitices representing a record
        hash_mod - (int) a number to modulo the hash value 
    returns (tuple) - a tuple of hash codes - one per column
    """
    # internal helper fn to return a truncated md5 hash of a string
    def hash_it(col_string):
        return hash(col_string) % hash_mod
    # Make sure everything is a string before hashing
    return tuple([hash_it(col) for col in record])

def compare_vectors_on_cols(first, second, cols=None):
    """Comapre similarity of two vectors based on specific columns
    params:
        first - a list or tuple of values
        second - a list or tuple of values of equal length
        cols - indices to compare on
    returns (float) - portion of columns that match
    """
    assert len(first) == len(second)
    if cols is None:
        cols = range(len(first))
    matches = [ci for ci in cols if first[ci] == second[ci]]
    return len(matches)/len(cols)

def group_similar_records(records, cols_to_compare, min_similarity):
    """Splits a set of records into groups based on similar hash vectors.
    params:
        records - a list of tuples
        cols_to_compare - a list of columns to compare
        min_similarity - 
    """
    # 
    grouped_records = []
    for record in records:
        # if it's similar to a group, add it and move on
        for group in grouped_records:
            if compare_vectors_on_cols(group[0], record, cols_to_compare) > min_similarity:
                group.append(record)
                continue
        # otherwise, create a new group
        grouped_records.append([record])
    

def group_records_exact(records, key_columns):
    """Collect exact mathes based on a set of key columns
    params:
        records - a list of tuples to consolidate
        key_columns - the columns to collate by (exact matching only)
    returns (list) - a list of record tuples with a group id prepended to each record
    """
    # helper fn to make a sub-tuple for grouping
    def make_key_for_cols(record):
        return tuple([record[i] for i in key_columns])

    # use itertools to group by key columns
    # itertools expects sorted data
    sorted_records = sorted(records, key=make_key_for_cols)
    grouped_records = [
        list(group) for _, group in itertools.groupby(sorted_records, key=make_key_for_cols)
    ]
    
    # make list of tuples with group id appended
    # TODO: there is probably a more elegant way to do this with iterators
    records_with_group_ids = []
    ids = range(len(grouped_records))
    for id, record_group in zip(ids, grouped_records):
        for record in record_group:
            records_with_group_ids.append(tuple([id] + list(record)))

    # return records_with_group_ids
    return records_with_group_ids

def consolidate_brokers(input_filename, key_cols, output_filename, exact=False):
    brokers = load_file(input_filename)
    if exact:
        grouped_records = group_records_exact(brokers['records'], key_cols)
    else:
        raise RuntimeError("fuzzy match not implemented")
    headers = ['GROUP_ID'] + list(brokers['headers'])
    output = [headers] + grouped_records
    write_file(output_filename, output)
