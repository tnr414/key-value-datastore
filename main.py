'''

import DataStore

if __name__ == '__main__':

    # this line will create new file with given name as argument
    store1 = DataStore.datastore('abc')
    # this line will create new / use file of default name
    store2 = DataStore.datastore()
    # this line will use already existing file of given name
    store2 = DataStore.datastore('abc', False)
    store1.create('01', {'name' : 'abhay', 'age' : 18})
    store1.create('02', {'name' : 'adarsh', 'age' : 20})
    print(store1.read('01'), type(store1.read('01')))
    print(store1.read('02'), type(store1.read('02')))
    store1.delete('02')
    print(store1.read('01'), type(store1.read('01')))
    #following line will throw an error,
    print(store1.read('02'), type(store1.read('02')))

'''
    
