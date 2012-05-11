# -*- coding: utf-8 -*-

import selenium
from selenium.webdriver.support.ui import WebDriverWait

def _is_wrappable(obj):
    if (isinstance(obj, selenium.webdriver.remote.webdriver.WebDriver) or
        isinstance(obj, selenium.webdriver.remote.webelement.WebElement)):
        return True
    else:
        return False

def _chainreact(__getattr__):
    def containment(*methodname):
        self, methodobj = __getattr__(*methodname)
        def reaction(*realargs):
            result = methodobj(*realargs)
            result = result if result else self
            if _is_wrappable(result):
                return SeleniumWrapper(result)
            else:
                return result
        return reaction
    return containment

class SeleniumWrapper(object):

    def __init__(self, driver):
        if _is_wrappable(driver):
            self._driver = driver
        else:
            msg = "2nd argument should be an instance of WebDriver or WebElement. given %s.".format(type(driver))
            raise TypeError(msg)

    @property
    def unwrap(self):
        return self._driver

    @classmethod
    def create(cls, drivername):
        drivers = {'ie': selenium.webdriver.Ie,
                   'opera': selenium.webdriver.Opera,
                   'chrome': selenium.webdriver.Chrome,
                   'firefox': selenium.webdriver.Firefox}
        if not isinstance(drivername, str):
            msg = "drivername should be an instance of string. given %s".format(type(drivername))
            raise TypeError(msg)
        dname = drivername.lower()
        if dname in drivers:
            try:
                return SeleniumWrapper(drivers[dname]())
            except Exception, e:
                raise e
        else:
            msg = "drivername should be one of [IE, Opera, Chrome, Firefox](case-insentive). given %s".format(drivername)
            raise ValueError(msg)

    def __getattribute__(self, name):
        return object.__getattribute__(self, name)

    @_chainreact
    def __getattr__(self, name):
        return self._driver, getattr(self._driver, name)

    def waitfor(self, type, target, eager=False, timeout=10):
        if eager:
            types = {"id":lambda d: d.find_elements_by_id(target),
                     "name":lambda d: d.find_elements_by_name(target),
                     "xpath":lambda d: d.find_elements_by_xpath(target),
                     "link_text":lambda d: d.find_elements_by_link_text(target),
                     "partial_link_text":lambda d: d.find_elements_by_partial_link_text(target),
                     "tag":lambda d: d.find_elements_by_tag_name(target),
                     "class":lambda d: d.find_elements_by_class_name(target),
                     "css":lambda d: d.find_elements_by_css_selector(target), }
        else:
            types = {"id":lambda d: d.find_element_by_id(target),
                     "name":lambda d: d.find_element_by_name(target),
                     "xpath":lambda d: d.find_element_by_xpath(target),
                     "link_text":lambda d: d.find_element_by_link_text(target),
                     "partial_link_text":lambda d: d.find_element_by_partial_link_text(target),
                     "tag":lambda d: d.find_element_by_tag_name(target),
                     "class":lambda d: d.find_element_by_class_name(target),
                     "css":lambda d: d.find_element_by_css_selector(target), }
        finder = types[type]
        result = WebDriverWait(self._driver, timeout).until(finder)
        if eager and len(result):
            return SeleniumContainerWrapper(result)
        elif _is_wrappable(result):
            return SeleniumWrapper(result)
        else:
            return result

    def xpath(self, target, eager=False, timeout=10):
        return self.waitfor("xpath", timeout, eager, timeout)

    def css(self, target, eager=False, timeout=10):
        return self.waitfor("css", target, eager, timeout)

    def tag(self, target, eager=False, timeout=10):
        return self.waitfor("tag", target, eager, timeout)

    def by_class(self, target, eager=False, timeout=10):
        return self.waitfor("class", target, eager, timeout)

    def by_id(self, target, eager=False, timeout=10):
        return self.waitfor("id", target, eager, timeout)

    def by_name(self, target, eager=False, timeout=10):
        return self.waitfor("name", target, eager, timeout)

    def by_linktxt(self, target, eager=False, timeout=10):
        return self.waitfor("link_text", target, eager, timeout)

    def by_partial_linktxt(self, target, eager=False, timeout=10):
        return self.waitfor("partial_link_text", target, eager, timeout=10)

    def href(self, url, eager=False, timeout=10):
        return self.xpath("//a[@href='%s']".format(url), eager, timeout)

    def img(self, eager=True, ext=None, timeout=10):
        if ext:
            return self.xpath("//img[@contains(@src, '%s']".format(ext), eager, timeout)
        return self.xpath("//img", eager, timeout)