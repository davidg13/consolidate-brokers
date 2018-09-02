# Python 3 compatible
from .brokers import (
    load_file, create_hash_vector, compare_vectors_on_cols, 
    group_records_exact
)

def test_load_file():
    result = load_file('test_data/test_file.csv')
    assert result['headers'] == ('COL_A', 'COL_B', 'COL_C')
    assert result['count'] == 3
    assert result['records'] == [
        ('Alpha','1','First'),
        ('Beta','2','Second'),
        ('Gamma','3','Third'),
    ]

def test_create_hash_vector():
    record = ('Alpha',1,'First')
    hash_mod = 5
    hash_vector = create_hash_vector(record, hash_mod)
    assert hash_vector == (
        hash('Alpha') % 5,
        hash(1) % 5,
        hash('First') % 5)

def test_compare_vectors_on_cols():
    vector_a = ('a', 'b', 'c', 'd', 'e')
    vector_b = ('a', 'b', 'c', 'y', 'z')
    similarity_all = compare_vectors_on_cols(vector_a, vector_b, cols=list(range(5)))
    similarity_start = compare_vectors_on_cols(vector_a, vector_b, [0,1,2])
    similarity_end = compare_vectors_on_cols(vector_a, vector_b, [1, 2,3,4])
    assert similarity_all == 0.6
    assert similarity_start == 1.0
    assert similarity_end == 0.5

def test_group_records_exact():
    records = [
        ('A', '1', 'x', 'y'),
        ('B', '1', 'x', 'y'),
        ('A', '1', 'x', 'z'),
        ('A', '2', 'u', 'v'),
        ('B', '1', 's', 't'),
        ('B', '2', 'p', 'r')
    ]

    records_with_ids = group_records_exact(records, [0,1])
    print(records_with_ids)
    assert records_with_ids == [
        (0, 'A', '1', 'x', 'y'),
        (0, 'A', '1', 'x', 'z'),
        (1, 'A', '2', 'u', 'v'),
        (2, 'B', '1', 'x', 'y'),
        (2, 'B', '1', 's', 't'),
        (3, 'B', '2', 'p', 'r')
    ]