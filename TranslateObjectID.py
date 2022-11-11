import weakref

_id_to_obj_dict = weakref.WeakValueDictionary()


def create_callback_data_id(obj):
    """
    Uses the weakref module to create and store a reference to obj

    output value: reference to the object

    It is not possible to directly uses python object through a Callback function because
    with ctypes there is no pointer to python object.
    This function store in a dictionary a reference to an object
    This object can be retrieved using the get_callback_data_from_id function

    For python object that cannot be weakreferenced, one can creat a dummy class to wrap
    the python object :
        def MyList(list)
            pass

        data = MyList()
        id = create_callback_data_id(data)

    """
    obj_id = id(obj)
    _id_to_obj_dict[obj_id] = obj
    return obj_id


def get_callback_data_from_id(obj_id):
    """
    Retrieve an object stored using create_call_backdata_id
    """
    return _id_to_obj_dict[obj_id]


class MyList(list):
    pass
