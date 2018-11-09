import xml.dom.minidom


def main():
    dom = xml.dom.minidom.parse('log.xml')
    testcases = dom.getElementsByTagName('testcase')
    for testcase in testcases:
        print(testcase.childNodes)


if __name__ == '__main__':
    main()
