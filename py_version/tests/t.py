xml = b"""
<!--multi-package divider-->
<cpkg>
    <stats>
        <time>0</time>
        <checksum>0000000</checksum>
    </stats>
    <data>
        \x89\x94\xc1\xac\xc9[\xfa\xfe\xfaR\xd8W40,u\x15\xd2A\xd2\x85\x06\x7f\xa57\t\x82\rLL\xcb\x9d\x1eyKO\xc9\xdb\x8a\x81\x15Zr\x92\x0f\xd6\xe1S\x1008\xf05_)\x1d\xf1\xa9CK\x88\x046
    </data>
</cpkg>
<!--multi-package divider-->
<cpkg>
    <stats>
        <time>0</time>
        <checksum>0000000</checksum>
    </stats>

"""
# xml = b'\x89\x94\xc1\xac\xc9[\xfa\xfe\xfaR\xd8W40,u\x15\xd2A\xd2\x85\x06\x7f\xa57\t\x82\rLL\xcb\x9d\x1eyKO\xc9\xdb\x8a\x81\x15Zr\x92\x0f\xd6\xe1S\x1008\xf05_)\x1d\xf1\xa9CK\x88\x046'
# x = xml.replace('\n', '').replace(' ', '').split('<!--multi-package-divider-->')
# print(x[1])
#
# import xml.etree.ElementTree as ET
#
# root = ET.fromstring(x[1])
# child = root[1]
# print(child.tag, child.attrib, child.text)

import re
v = memoryview(xml)

print(data)