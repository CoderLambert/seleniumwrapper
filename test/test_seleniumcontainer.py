import sys

sys.path.append("./../src")

import unittest
import collections
import mock
import selenium
from seleniumpytest.container import SeleniumContainerWrapper
from seleniumpytest.wrapper import SeleniumWrapper

class TestSeleniumContainerWrapper(unittest.TestCase):

    def test_container_raise_if_given_argument_is_not_an_instance_of_Sequence(self):
        containment = 1
        self.assertNotIsInstance(containment, collections.Sequence)
        self.assertRaises(TypeError, SeleniumContainerWrapper, containment)
        self.assertRaises(TypeError, SeleniumContainerWrapper.wrap, containment)

    def test_container_holds_given_argument_if_it_is_an_instance_of_Sequence(self):
        containment = []
        self.assertIsInstance(containment, collections.Sequence)
        SeleniumContainerWrapper(containment)
        SeleniumContainerWrapper.wrap(containment)

    def test_container_should_delegate_unknown_attribute_access_to_wrapped_container(self):
        container = SeleniumContainerWrapper([])
        container.append(1)
        container.append(1)
        self.assertEquals(container.count(1), 2)
        self.assertEquals(container.pop(), 1)
        self.assertEquals(container.count(1), 1)

    def test_container_should_return_wrapped_object_if_possible(self):
        mock1 = mock.Mock(selenium.webdriver.remote.webdriver.WebDriver)
        mock2 = mock.Mock(selenium.webdriver.remote.webdriver.WebElement)
        iterable = [mock1, mock2]
        container = SeleniumContainerWrapper(iterable)
        wrapped1 = container.pop()
        self.assertTrue(isinstance(wrapped1, SeleniumWrapper))
        self.assertTrue(hasattr(wrapped1, 'waitfor'))
        wrapped2 = container.pop()
        self.assertTrue(isinstance(wrapped2, SeleniumWrapper))
        self.assertTrue(hasattr(wrapped2, 'waitfor'))

    def test_container_should_support_indexing_and_also_wrap_if_possible(self):
        mock1 = mock.Mock(selenium.webdriver.remote.webdriver.WebDriver)
        mock2 = mock.Mock(selenium.webdriver.remote.webdriver.WebElement)
        iterable = [mock1, mock2, 1]
        container = SeleniumContainerWrapper(iterable)
        self.assertIsInstance(container[0], SeleniumWrapper)
        self.assertIsInstance(container[1], SeleniumWrapper)
        self.assertIsInstance(container[2], int)

    def test_container_support_for_statement(self):
        mock1 = mock.Mock(selenium.webdriver.remote.webdriver.WebDriver)
        mock2 = mock.Mock(selenium.webdriver.remote.webdriver.WebElement)
        iterable = [mock1, mock2]
        container = SeleniumContainerWrapper(iterable)
        for m in container:
            self.assertIsInstance(m, SeleniumWrapper)

    def test_container_has_length(self):
        mock1 = mock.Mock(selenium.webdriver.remote.webdriver.WebDriver)
        mock2 = mock.Mock(selenium.webdriver.remote.webdriver.WebElement)
        iterable = [mock1, mock2]
        container = SeleniumContainerWrapper(iterable)
        self.assertEquals(len(container), 2)

    def test_container_support__contains__protocol(self):
        mock1 = mock.Mock(selenium.webdriver.remote.webdriver.WebDriver)
        mock2 = mock.Mock(selenium.webdriver.remote.webdriver.WebElement)
        iterable = [mock1, mock2]
        container = SeleniumContainerWrapper(iterable)
        self.assertTrue(mock1 in container)
        self.assertTrue(mock2 in container)

def suite():
    suite = unittest.TestSuite()
    suite.addTests(unittest.makeSuite(TestSeleniumContainerWrapper))
    return suite

if __name__ == "__main__":
    suite()