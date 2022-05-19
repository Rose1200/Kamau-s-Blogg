import unittest
from model import Blogs

class Blogs(unittest.TestCase):
    '''
    Test Class to test the behavior of the News class
    '''

    def setUp(self):
        '''
        Set up method that will run before every Test 
        '''
        self.apple_news = Blogs()

if __name__ == '__main__':
    unittest.main()       