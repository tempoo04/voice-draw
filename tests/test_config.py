import unittest

import config


class ConfigTests(unittest.TestCase):
    def test_paths_are_project_relative(self):
        self.assertEqual(config.ICON_DIR.parent, config.ROOT_DIR)
        self.assertEqual(config.IMAGE_OUTPUT_DIR.parent, config.ROOT_DIR)


if __name__ == "__main__":
    unittest.main()
