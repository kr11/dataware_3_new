# coding:'utf-8'
__author__ = 'kangrong'

test_data = [
    {
        'age':'youth','income':'high','student':False,'credit_rating':'fair','class':'no'
    },
    {
        'age':'youth','income':'high','student':False,'credit_rating':'excellent','class':'no'
    },
    {
        'age':'middle_aged','income':'high','student':False,'credit_rating':'fair','class':'yes'
    },
    {
        'age':'senior','income':'medium','student':False,'credit_rating':'fair','class':'yes'
    },
    {
        'age':'senior','income':'low','student':True,'credit_rating':'fair','class':'yes'
    },
    {
        'age':'senior','income':'low','student':True,'credit_rating':'excellent','class':'no'
    },
    {
        'age':'middle_aged','income':'low','student':True,'credit_rating':'excellent','class':'yes'
    },
    {
        'age':'youth','income':'medium','student':False,'credit_rating':'fair','class':'no'
    },
    {
        'age':'youth','income':'low','student':True,'credit_rating':'fair','class':'yes'
    },
    {
        'age':'senior','income':'medium','student':True,'credit_rating':'fair','class':'yes'
    },
    {
        'age':'youth','income':'medium','student':True,'credit_rating':'excellent','class':'yes'
    },
    {
        'age':'middle_aged','income':'medium','student':False,'credit_rating':'excellent','class':'yes'
    },
    {
        'age':'middle_aged','income':'high','student':True,'credit_rating':'fair','class':'yes'
    },
       {
        'age':'senior','income':'medium','student':False,'credit_rating':'excellent','class':'no'
    }
]
labels = {'age':True,'income':True,'student':True,'credit_rating':True}

# a = labels.keys()
# print a
# test_data = [
#     {'no surfacing':1,'flippers':1,'class':'yes'},
#     {'no surfacing':1,'flippers':1,'class':'yes'},
#     {'no surfacing':1,'flippers':0,'class':'no'},
#     {'no surfacing':0,'flippers':1,'class':'no'},
#     {'no surfacing':0,'flippers':1,'class':'no'},
# ]
# labels = {'no surfacing':True,'flippers':True}