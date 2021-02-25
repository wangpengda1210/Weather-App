# write your code here
import shelve

with shelve.open('my_library', flag='c', writeback=True) as lib:
    lib['Anna Karenina'] = 'Happy families are all alike; every unhappy family is unhappy in its own way...'

print('A new book has been added to the library!')
