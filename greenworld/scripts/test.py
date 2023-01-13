import unittest

def main():
    suite = unittest.defaultTestLoader.discover('greenworld/tests', pattern = '*.py')
    unittest.TextTestRunner().run(suite)

if __name__ == '__main__':
    main()
