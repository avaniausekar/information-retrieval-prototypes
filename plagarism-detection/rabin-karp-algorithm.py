# string-searching algorithm that uses hashing to find an exact match of a pattern string in a text
# Uses Rolling hash to quickly filter out text that canot match the pattern
# used for pattern searching


class RollingHash:
    # Select a prime number ‘p‘ as the modulus. This choice helps avoid overflow issues and ensures a good distribution of hash values.
    # Choose a base ‘b‘ (usually a prime number as well), which is often the size of the character set (e.g., 256 for ASCII characters).
    def __init__(self, base=256, modulo=(10**9 + 7)):
        self.base = base
        self.modulo = modulo
        self.hash = 0
        self.window = []
        self.power = 1

    def add_char(self, c):
        char_code = ord(c)
        self.hash = (self.hash * self.base + char_code) % self.modulo
        self.window.append(c)

        # Update highest power if this is not the first character
        if len(self.window) > 1:
            self.power = (self.power * self.base) % self.modulo

    def remove_char(self):
        if not self.window:
            self.power = 1
            return None

        char = self.window.pop(0)
        char_code = ord(char)
        self.hash = (self.hash - char_code * self.power) % self.modulo
        self.power = (self.power // self.base) % self.modulo
        return char

    def calculate_hash(self, text):
        res = 0
        for char in text:
            res = (res * self.base + ord(char)) % self.modulo
        return res

    def get_hash(self):
        return self.hash


def rabin_karp(text, substring):
    if not substring or not text or len(substring) > len(text):
        return []

    matches = []

    pattern_length = len(substring)
    rolling_hash = RollingHash()
    pattern_hash = rolling_hash.calculate_hash(substring)

    text_hash = RollingHash()
    for i in range(pattern_length):
        text_hash.add_char(text[i])

    if text_hash.get_hash() == pattern_hash and text[:pattern_length] == substring:
        matches.append(0)

    # Slide the window through the text
    for i in range(pattern_length, len(text)):
        # Remove the first character and add the next character
        text_hash.remove_char()
        text_hash.add_char(text[i])

        window_start = i - pattern_length + 1

        # If hash values match, verify with direct string comparison ???
        if text_hash.get_hash() == pattern_hash:
            window_text = text[window_start:window_start + pattern_length]
            if window_text == substring:
                matches.append(window_start)

    return matches


def main():
    text = "A good person"
    pattern = "d per"
    # TODO white spacessssssssssssssss

    matches = rabin_karp(text, pattern)

    if matches:
        print(f"Pattern '{pattern}' found at positions: {matches}")
    else:
        print(f"Pattern '{pattern}' not found in the text.")


main()

# prefix = suffix = 0
# base  = 256
# last_index = 0
# power = 1

# for i,c in enumerate(s):
#     char = (ord(c) - ord('a') + 1)
#     prefix = prefix * base
#     prefix = prefix + char
#     suffix = suffix + char * power
#     power = power * base
#     if prefix == suffix:
#         last_index = i
