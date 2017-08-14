#Schema for the csv files
doc_schema = {
    'nodes': {
        'type': 'dict',
        'schema': {
            'id'  : {'required': True, 'type': 'integer', 'coerce': int},
            'lat' : {'type': 'float', 'coerce': float},
            'lon' : {'type': 'float', 'coerce': float},
            'user': {'type': 'string'},
            'uid' : {'type': 'integer', 'coerce': int},
            'version'  : {'type': 'integer', 'coerce': int},
            'changeset': {'type': 'integer', 'coerce': int},
            'timestamp': {'type': 'string'}
            }
        },
    'node_tags': {
        'type': 'list',
        'schema': {
            'type': 'dict',
            'schema': {
                'id' : {'required': True, 'type': 'integer', 'coerce': int},
                'key': {'type': 'string'},
                'value': {'type': 'string'},
                'type' : {'type': 'string'}
            }
        }
    },
    'ways': {
        'type': 'dict',
        'schema': {
            'id': {'required': True, 'type': 'integer', 'coerce': int},
            'user': {'type': 'string'},
            'uid' : {'type': 'integer', 'coerce': int},
            'version' : {'type': 'string'},
            'changeset': {'type': 'integer', 'coerce': int},
            'timestamp': {'type': 'string'}
            }
        },
    'ways_tags':{
        'type': 'list',
        'schema': {
            'type': 'dict',
            'schema': {
                'id' : {'required': True, 'type': 'integer', 'coerce': int},
                'key': {'required': True, 'type': 'string'},
                'value': {'required': True, 'type': 'string'},
                'type' : {'type': 'string'}
                }
            }
        },
    'ways_nodes':{
        'type': 'list',
        'schema': {
            'type': 'dict',
            'schema': {
                'id' : {'required': True, 'type': 'integer', 'coerce': int},
                'node_id': {'required': True, 'type': 'integer', 'coerce': int},
                'position': {'required': True, 'type': 'integer', 'coerce': int}
                }
            }
        }
    }
