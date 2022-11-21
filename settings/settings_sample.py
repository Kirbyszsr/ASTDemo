basic_url = '[BASIC_URL_FOR_YOUR_PROJECT]'
commands = [
    {
        'file': 'YOUR_FILE_NAME.py',
        'commands': [
            # {'name' : 'ceshi',
            #  'command_type': 'add',
            #  'paras': {}
            #  },
            {'func': 'add',  # add or delete
             'name': 'test_sample',
             'command_type': 'add',
             'position': {
                                'direction': 'before',
                                'location': 'testing'
                          },
             'paras': {'ceshi1': 'ceshi',
                       'ceshi2': 1,
                       'ceshi3': True,
                       'ceshi4': {'ceshi': "ceshi",
                                  "ceshi2": 1,
                                  1: "ceshi3"
                                  },
                       'ceshi5': [1, 2, 'ceshi'],
                       'ceshi6': (1, 2),
                       'ceshi7': 5.6,
                       'ceshi8': 9j
                       # '[paraname] : [paras]'
                       }
             },
            {'func': 'add',
             'name': 'ceshi2',
             'command_type': 'add'
             },
            {'func': 'add',
             'name': 'ceshi3',
             'command_type': 'delete'
             }
        ]
    }
]
