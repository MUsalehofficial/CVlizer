import unicodedata


def allowed_file(filename):
    return filename.lower().endswith(('.pdf', '.doc', '.docx'))


def array_to_lowercase(array):
    return list(map(lambda item: item.lower(), array))


def decode_unicode_chars(str):
    return unicodedata.normalize('NFD', str).encode('ascii', 'ignore')


