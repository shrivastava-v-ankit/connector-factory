#!/usr/bin/env python

"""
File to common methods exposed as static under Common class.
"""

import logging


logger = logging.getLogger(__name__)


class Common(object):
    """
    Class handle the common utility methods.

    ********
    Methods:
    --------

        normaize_connection_dict:   Method to convert the key of dictonary
                                    in upper case to ensure uniform access.
    """

    @staticmethod
    def normaize_connection_dict(connection_dict: dict,
                                 is_to_upper: bool = False):
        """
        Method helps to normalize the key name of dictonary to upper case.
        This helps even mixed case keys are provided will help further
        execution to handle the keys as reuired by application.

        ***********
        Attributes:
        -----------

            connection_dict:    (Required) => Dictonary object to normalize the
                                keys.
            is_to_upper:        (Optional) => If True keys will be normalized
                                to upper case else to lower case.
                                Default: False
        *******
        Return:
        -------

            conn_dict:          Dictonary to set keys to upper case for uniform
                                access.
        """
        if is_to_upper:
            conn_dict = {key.upper(): value for key,
                         value in connection_dict.items()}
        else:
            conn_dict = {key.lower(): value for key,
                         value in connection_dict.items()}
        return conn_dict
