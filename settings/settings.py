basic_url = 'C:\\Users\\Lenovo\\Desktop\\sample_project'
commands = [
    {
        'file': 'sample_python_file.py',
        'commands': [
            {'func': 'add',
             'name': 'test_sample',
             'command_type': 'add',
             'position': {
                 'direction': 'after',
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
                       }
             },
            {'func': 'add',
             'name': 'test_sample_before',
             'command_type': 'add',
             'position': {
                 'direction': 'before',
                 'location': 'testing'
             },
             'paras': {'ceshi1': 'ceshi',
                       'ceshi2': 1,
                       }
             },
            {'func': 'add',
             'name': 'ceshi1',
             'command_type': 'add'
             },
            {'func': 'add',
             'name': 'ceshi3',
             'command_type': 'delete'
             },
            {'func': 'delete',
             'name': 'ceshi3',
             'command_type': 'add'
             }
        ]
    }
]
