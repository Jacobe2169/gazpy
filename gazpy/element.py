# coding = utf-8


from functools import wraps


def objectify(func):
    """Mimic an object given a dictionary.

    Given a dictionary, create an object and make sure that each of its
    keys are accessible via attributes.
    If func is a function act as decorator, otherwise just change the dictionary
    and return it.
    :param func: A function or another kind of object.
    :returns: Either the wrapper for the decorator, or the changed value.

    Example::

    >>> obj = {'old_key': 'old_value'}
    >>> oobj = objectify(obj)
    >>> oobj['new_key'] = 'new_value'
    >>> print oobj['old_key'], oobj['new_key'], oobj.old_key, oobj.new_key

    >>> @objectify
    ... def func():
    ...     return {'old_key': 'old_value'}
    >>> obj = func()
    >>> obj['new_key'] = 'new_value'
    >>> print obj['old_key'], obj['new_key'], obj.old_key, obj.new_key

    """

    def create_object(value):
        """Create the object.

        Given a dictionary, create an object and make sure that each of its
        keys are accessible via attributes.
        Ignore everything if the given value is not a dictionary.
        :param value: A dictionary or another kind of object.
        :returns: Either the created object or the given value.

        """
        if isinstance(value, dict):
            # Build a simple generic object.
            class Object(dict):
                def __setitem__(self, key, val):
                    setattr(self, key, val)
                    return super(Object, self).__setitem__(key, val)

            # Create that simple generic object.
            ret_obj = Object()
            # Assign the attributes given the dictionary keys.
            for key, val in value.items():
                if isinstance(val, dict):
                    ret_obj[key] = objectify(val)
                else:
                    ret_obj[key] = val
                setattr(ret_obj, key, val)
            return ret_obj
        else:
            return value

    # If func is a function, wrap around and act like a decorator.
    if hasattr(func, '__call__'):
        @wraps(func)
        def wrapper(*args, **kwargs):
            """Wrapper function for the decorator.

            :returns: The return value of the decorated function.

            """
            value = func(*args, **kwargs)
            return create_object(value)

        return wrapper

    # Else just try to objectify the value given.
    else:
        return create_object(func)


class Element():

    """
    Da Bomb Code ! Made by me <3
    """
    def __init__(self, series, gazetteer):
        self.data = series
        self.p_holder = gazetteer

    @property
    def id(self):
        return self.data[self.p_holder.id_field]

    @property
    def label(self):
        if not isinstance(self.p_holder.label_fields, tuple) and not isinstance(self.p_holder.label_fields, list):
            return self.data[self.p_holder.label_fields]
        else:
            return objectify({lang: self.data[lang] for lang in self.p_holder.label_fields})

    @property
    def alias(self):
        if not isinstance(self.p_holder.alias_fields, tuple) and not isinstance(self.p_holder.label_fields, list):
            return self.data[self.p_holder.alias_fields]
        else:
            return objectify({lang: self.data[field][lang] for field, lang in self.p_holder.alias_fields})

    @property
    def coord(self):
        return objectify(self.data[self.p_holder.coordinates_field])

    @property
    def class_(self):
        return self.data[self.p_holder.class_field]

    @property
    def score(self):
        return self.data[self.p_holder.score_field]

    @property
    def other(self):
        return self.data
