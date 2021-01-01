import os
from sys import getsizeof
import json
from functools import wraps
from threading import Lock  



'''
Below function 'synchronized' and class 'Synchronized' is used to
provide multithreading property. An user can access it using multiple
threads. It will make sure that a function of datastore class will be
completely executed at a time.
'''

def synchronized(lock):
    def wrapper(f):
        @wraps(f)
        def inner_wrapper(*args, **kwargs):
            with lock:
                return f(*args, **kwargs)
            return inner_wrapper
        return wrapper


class Synchronized:

    def __int_subclass__(cls, **kwargs):
        synchronizer = synchronized(Lock())
        for name in cls.__dict__:
            attr = getattr(cls, name)
            if callable(attr):
                setattr(cls, name, synchronizer(attr))


'''  
datastore is class that can be used as key value datastore using local
file system. This class takes to default parameters to intialize an
instance of the class. The first parameter is the name of file where
you want to store key value pairs. This paramter must be a string.
Second parameter takes a boolean value, indicating that whether user
want to create a new file or use an existing one. Default value of this
argument is True, indicating to create a new file.

Class basically provides three functionality:
    1. create - This function is used to insert a key value arguments in
       datastore.
    2. read - This function is used to read to stored data by providing
       a key.
    3. delete - This function is used to delete already existing key value
       pair from the datastore

** Details to use functions is written just before the code of respective functions **
'''
class datastore(Synchronized):
    
    def __init__(self, filename = 'mystorage', newfile = True):

        # filename must be a string
        if(type(filename) != str):
            raise TypeError("'filename' must be a string")
        self.filename = filename+'.json'

        self.storage = {}
        #maximum allowed length of key is 32
        self.KEY_LENGTH_LIMIT = 32
        #maximum allowed size of value is 16KB
        self.VALUE_SIZE_LIMIT = 16*1024
        # maximum allowed size of datastore is 1GB
        self.FILE_SIZE_LIMIT = 1024*1024*1024 

        # if filename is not passed it will use default name
        if os.path.isfile(self.filename) == True and filename == 'mystorage':
            pass

        # already existing file can't be used as newfile.
        elif os.path.isfile(self.filename) == True and newfile == True:
            raise Exception("File with given filename already exist")

        # given filename doest not already exist
        elif os.path.isfile(self.filename) == False and newfile == False:
            raise Exception("File with given filename does not exist")

        # creating file for new datastore
        elif newfile == True:
            with open(self.filename, 'w') as fp:
                json.dump(self.storage, fp)

        
    '''
    Below function is used to insert data in datastore. It takes two
    arguments, key and value. These two arguments must fulfill the
    following properties.
        1. key must be a string
        2. key should be unique i.e. should not be already existed
           in datastore
        3. datastore size should not exceed 1GB
        4. Length of the key should not exceed 32 characters.
        5. Size of value is capped at 16KB

    '''
    def create(self, key, value):

        # opening datastore file and storing it in a varaible
        with open(self.filename, 'r') as fp:
            data = json.load(fp)
            
        # key should be unique i.e. should not be already existed in datastore     
        if key in data:
            raise Exception("Value associated with gievn key already exist")

        # key must be a string
        if(type(key) != str):
            raise TypeError("Key must be a string")

        # datastore size should not exceed 1GB
        if os.stat(self.filename).st_size > self.FILE_SIZE_LIMIT:
            raise Exception("Memory size exceeded")

        # Length of the key should not exceed 32 characters.
        if len(key) > self.KEY_LENGTH_LIMIT :
            raise Exception("Length is ley cannot be grater than 32")

        # Size of value is capped at 16KB
        if getsizeof(value) > self.VALUE_SIZE_LIMIT :
            raise Exception("Value size limit exceeded")

        # converting value into a json object and storing it
        value = json.dumps(value)
    
        self.storage[key] = value
        data.update(self.storage)

        # writing key and value in datastore
        with open(self.filename, 'w') as fp:
            json.dump(data, fp)


    '''
    Delete function is used to delete the data from datastore.
    It takes key as an argument whose corrosponding value needs
    to be deleted from the datastore. If any value corrosponding
    to given value does not exist, then it will throw an error.
    '''
    
    def delete(self, key):
        # opening datastore file and storing it in a varaible
        with open(self.filename, 'r') as fp:
            data = json.load(fp)
        # value corrosponding to key must be present in datastore
        if key not in data:
            raise Exception("Value associated with gievn key deos not exist")

        # if key exist in temporary storage it must be deleted too.
        if key in self.storage:
            self.storage.pop(key)

        # deleting key-value from permanent storage
        data.pop(key)
        # writing the updated storage in datastore file
        with open(self.filename, 'w') as fp:
            json.dump(data, fp)


    '''
    Read function is used to read value from datastore. It
    takes key as an arguments and return value. Value will
    always be a json object. If any value corrosponding to
    given key does not exist, then it will give an error.
    '''    
    def read(self, key):
        # opening datastore file and storing it in a varaible
        with open(self.filename, 'r') as fp:
            data = json.load(fp)

        #  given key and corrosponding value must be in datastore    
        if key not in data:
            raise Exception("Value associated with gievn key deos not exist")

        # returning the value
        return data[key]



             
