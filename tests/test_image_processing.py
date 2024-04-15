import unittest
from utils.image_processing import is_base64

class TestIsBase64(unittest.TestCase):

    def test_valid_base64(self):
        valid_base64 = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg=="
        self.assertTrue(is_base64(valid_base64))

    def test_invalid_base64(self):
        invalid_base64 = "This is not valid base64"
        self.assertFalse(is_base64(invalid_base64))

    def test_no_base64_encoding(self):
        no_encoding = "data:image/png,iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg=="
        self.assertFalse(is_base64(no_encoding))

    def test_invalid_format(self):
        invalid_format = "This is not an image;base64,iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg=="
        self.assertFalse(is_base64(invalid_format))

class TestIsBase64Additional(unittest.TestCase):

    def test_empty_string(self):
        empty = ""
        self.assertFalse(is_base64(empty))

    def test_whitespace_string(self):
        whitespace = "   "
        self.assertFalse(is_base64(whitespace))

    def test_partially_valid_base64(self):
        partially_valid = "data:image/png;base64,ThisIsNotValidBase64=="
        self.assertFalse(is_base64(partially_valid))

    def test_valid_base64_with_newlines(self):
        with_newlines = "data:image/png;base64,\niVBORw0KGgoAAA\nANSUhEUgAAAAUA\nAAAFCAYAAACN\nbyblAAAAHElE\nQVQI12P4//8/w38GIAXDI\nBKE0DHxgljNBAAO9TXL0Y4OHwAAA\nAAABJRU5ErkJggg=="
        self.assertTrue(is_base64(with_newlines))

    def test_valid_base64_with_whitespace(self):
        with_whitespace = "data:image/png;base64,   iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg==   "
        self.assertTrue(is_base64(with_whitespace))

class TestIsBase64Additional2(unittest.TestCase):

    def test_very_long_base64(self):
        very_long_base64 = "data:image/png;base64," + "a"*10000
        self.assertTrue(is_base64(very_long_base64))

    def test_max_base64_length(self):
        max_length_base64 = "data:image/png;base64," + "a"*65535
        self.assertTrue(is_base64(max_length_base64))

    def test_over_max_base64_length(self):
        over_max_length = "data:image/png;base64," + "a"*65536
        self.assertFalse(is_base64(over_max_length))

    def test_invalid_data_url_scheme(self):
        invalid_scheme = "http://example.com/image.png"
        self.assertFalse(is_base64(invalid_scheme))

    def test_jpeg_image_type(self):
        jpeg_image = "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAYEBQYFBAYGBQYHBwYIChAKCgkJChQODwwQFxQYGBcUFhYaHSUfGhsjHBYWICwgIyYnKSopGR8tMC0oMCUoKSj/2wBDAQcHBwoIChMKChMoGhYaKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCj/wAARCACgAKADASIAAhEBAxEB/8QAHAAAAQUBAQEAAAAAAAAAAAAABAADBQYHAgEI/8QARRAAAgEDAwIEAwUFBAQFBQEAAQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0Kx0fDxFjNDU2JygpLwF0NTVKLC8WKTo//EABoBAAIDAQEAAAAAAAAAAAAAAAIDAAEEBQb/xAApEQACAgEEAgMAAQQDAAAAAAAAAQIRAwQSITETQQUiUWEUMoFCkaH/2gAMAwEAAhEDEQA/ALxREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREB"
        self.assertTrue(is_base64(jpeg_image))

if __name__ == '__main__':
    unittest.main()