#! /usr/bin/env python
# -*- coding : utf-8 -*-

import uuid
import dateutil.parser

class JsonSerializer(object):
    """A serializer that provides methods to serialize and deserialize JSON
    dictionaries.

    Note, one of the assumptions this serializer makes is that all objects that
    it is used to deserialize have a constructor that can take all of the
    attribute arguments. I.e. If you have an object with 3 attributes, the
    constructor needs to take those three attributes as keyword arguments.
    """

    __attributes__ = None
    """The attributes to be serialized by the seralizer.
    The implementor needs to provide these."""

    __required__ = None
    """The attributes that are required when deserializing.
    The implementor needs to provide these."""

    __attribute_serializer__ = None
    """The serializer to use for a specified attribute. If an attribute is not
    included here, no special serializer will be user.
    The implementor needs to provide these."""

    __object_class__ = None
    """The class that the deserializer should generate.
    The implementor needs to provide these."""

    serializers = dict(
                        id=dict(
                            serialize=lambda x: uuid.UUID(bytes=x).hex,
                            deserialize=lambda x: uuid.UUID(hex=x).bytes
                        ),
                        date=dict(
                            serialize=lambda x: x.isoformat(),
                            deserialize=lambda x: dateutil.parser.parse(x)
                        )
                    )

    def deserialize(self, json, **kwargs):
        """Deserialize a JSON dictionary and return a populated object.

        This takes the JSON data, and deserializes it appropriately and then calls
        the constructor of the object to be created with all of the attributes.

        Args:
            json: The JSON dict with all of the data
            **kwargs: Optional values that can be used as defaults if they are not
                present in the JSON data
        Returns:
            The deserialized object.
        Raises:
            ValueError: If any of the required attributes are not present
        """
        d = dict()
        for attr in self.__attributes__:
            if attr in json:
                val = json[attr]
            elif attr in self.__required__:
                try:
                    val = kwargs[attr]
                except KeyError:
                    raise ValueError("{} must be set".format(attr))

            serializer = self.__attribute_serializer__.get(attr)
            if serializer:
                d[attr] = self.serializers[serializer]['deserialize'](val)
            else:
                d[attr] = val

        return self.__object_class__(**d)

    def serialize(self, obj):
        """Serialize an object to a dictionary.

        Take all of the attributes defined in self.__attributes__ and create
        a dictionary containing those values.

        Args:
            obj: The object to serialize
        Returns:
            A dictionary containing all of the serialized data from the object.
        """
        d = dict()
        for attr in self.__attributes__:
            val = getattr(obj, attr)
            if val is None:
                continue
            serializer = self.__attribute_serializer__.get(attr)
            if serializer:
                d[attr] = self.serializers[serializer]['serialize'](val)
            else:
                d[attr] = val

        return d
