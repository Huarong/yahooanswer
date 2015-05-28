#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import requests


"""

output:

26
set([u'396545367', u'396545301', u'396545327', u'396546046', u'396545443', u'396545444', u'396545394', u'396545018', u'396545019', u'396545014', u'396545015', u'396545016', u'396545469', u'396545401', u'396545013', u'396545213', u'396545311', u'396545454', u'396545144', u'396545451', u'396545439', u'396545012', u'396545660', u'396545433', u'396546089', u'396545122'])

"""

def main():
    r = requests.get('https://answers.yahoo.com/dir/index')
    sid_reg = re.compile(r'href=/dir/index\?sid=(\d+)')
    found = sid_reg.findall(r.text)
    found = set(found)
    print len(found)
    print found


if __name__ == '__main__':
    main()
