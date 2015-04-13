# -*- coding: UTF-8 -*-
import types


class ChoiceType(types.TypeDecorator):
    '''
    ChoiceType is used seperated the actual MAGIC NUMBER and representation,
    the user could only use the representation to read and write the field
    '''

    impl = types.Integer

    def __init__(self, choices, *args, **kw):
        '''
        :type choices: dict
        :param choices: key是实际存储值, value是展示值
        '''
        self.choices = dict(choices)
        super(ChoiceType, self).__init__(*args, **kw)

    def process_bind_param(self, value, dialect):
        if value is None:
            return None
        for k, v in self.choices.items():
            if v == value:
                return k
        raise ValueError(u'value must be of ' +
                         ', '.join(self.choices.values()))

    def process_result_value(self, value, dialect):
        return None if value is None else self.choices[value]


class ListType(types.TypeDecorator):

    impl = types.String

    def process_bind_param(self, value, dialect):
        return '|'.join(value)

    def process_result_value(self, value, dialect):
        return value.split('|')
