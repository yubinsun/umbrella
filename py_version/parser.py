import threading
import queue

# parst tcp packages which contains xml docs
# XML docs are continuous
import time
import xml.etree.ElementTree
import re


class tcp_parser(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.inputCache = queue.Queue()
        self.outputCache = queue.Queue()
        # self.xml_structure
        self.active = False
        # compiled RE
        self.re_cpkg = re.compile(b'cpkg')

        self.cpkg_pointer = 0  # which char the start of a head
        self.span_pointer = (0, 0)  # which ele in Q current checked

        # for test new parse_xml (brutal)
        self.inputStreamCache = bytearray(b'')

    def __parse_xml(self):
        # old parser. Some problems
        if not self.inputCache.empty():
            if self.span_pointer[0] == 0:
                # in the first element
                s = re.search(b'<cpkg>', self.inputCache.queue[0][self.cpkg_pointer:])
                if s:
                    self.cpkg_pointer = s.span()[0] + self.cpkg_pointer
                else:
                    print("Head not in the first element, pop it ")
                    print("span_p", self.span_pointer)
                    self.inputCache.get()
                    self.cpkg_pointer = 0
                    if self.span_pointer[0] != 0:
                        raise Exception("self.span_pointer[0] != 0:")
                    self.span_pointer = (0, 0)
                    return

            s = re.search(b'</cpkg>', self.inputCache.queue[self.span_pointer[0]][self.span_pointer[1]:])
            if s:
                self.span_pointer = (self.span_pointer[0], s.span()[1] + self.span_pointer[1])
            else:
                self.span_pointer = (self.span_pointer[0] + 1, 0)

            # output stage
            if self.span_pointer[1] != 0:
                if self.span_pointer[0] == 0:
                    # output at the first ele, (cannot pop the first element then?)
                    # then simply output it
                    print(self.inputCache.queue[0][self.cpkg_pointer: self.span_pointer[1]])
                    # then need to set 2 pointers
                    self.cpkg_pointer = self.span_pointer[1]
                if self.span_pointer[0] > 0:
                    l = []
                    l.append(self.inputCache.get()[self.cpkg_pointer:])
                    for i in range(1, self.span_pointer[0]):
                        l.append(self.inputCache.get())
                    l.append(self.inputCache.queue[0][0:self.span_pointer[1]])
                    self.cpkg_pointer = 0
                    self.span_pointer = (0, self.span_pointer[1])
                    print(l)

    def _parse_xml(self):

        if not self.inputCache.empty():
            r = bytearray(self.inputCache.get())
            self.inputStreamCache += (r)
            # print(self.inputStreamCache)
        s = re.search(b'<cpkg>.+?</cpkg>', self.inputStreamCache)
        if s:
            # print(s.span()[0], s.span()[1])

            # self.outputCache.put(self.inputStreamCache[s.span()[0]: s.span()[1]])
            self.outputCache.put(self.inputStreamCache[s.span()[0]+6: s.span()[1]-7])
            # print(self.inputStreamCache[s.span()[0]+6: s.span()[1]-7])
            self.inputStreamCache = self.inputStreamCache[s.span()[1]:]

    def feed(self, xml_str):
        # fed in str can be incomplete, in bytes
        self.inputCache.put(xml_str)

    def run(self) -> None:
        self.active = True
        while self.active:
            self._parse_xml()
            time.sleep(0.000001)

    def stop(self):
        self.active = False

    def __del__(self):
        pass
def test_tcp_parser_old():
    t = tcp_parser(None)
    t.feed(b"rasfae<cpkg>\x89\x94\xc1")
    t.feed(b'123123123123')
    t.feed(b"\x89\x94\xc1</cpkg><cpkg>22222222</cpkg>")
    t.feed(b"<cpkg>33333</cpkg><cpkg>44444</cpkg>")
    t._parse_xml()
    t._parse_xml()
    t._parse_xml()
    t._parse_xml()
    t._parse_xml()
    t._parse_xml()
    t._parse_xml()


def test_tcp_parser():
    t = tcp_parser(None)
    t.feed(b"rasfae<cpkg>\x89\x94\xc1")
    t.feed(b'123123123123')
    t.feed(b"\x89\x94\xc1</cpkg><cpkg>22222222</cpkg>")
    t.feed(b"<cpkg>33333</cpkg><cpkg>44444</cpkg>")
    t._parse_xml()
    t._parse_xml()
    t._parse_xml()
    t._parse_xml()
    t._parse_xml()
    t._parse_xml()
    t._parse_xml()


if __name__ == '__main__':
    test_tcp_parser()
