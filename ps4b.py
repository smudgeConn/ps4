# Problem Set 4B
# Name: <your name here>
# Collaborators:
# Time Spent: x:xx

import string

### HELPER CODE ###


def load_words(file_name):  # output is a list of words
    '''
    file_name (string): the name of the file containing
    the list of words to load

    Returns: a list of valid words. Words are strings of lowercase letters.

    Depending on the size of the word list, this function may
    take a while to finish.
    '''
    # print("Loading word list from file...")
    # inFile: file
    inFile = open(file_name, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.extend([word.lower() for word in line.split(' ')])
    # print("  ", len(wordlist), "words loaded.")
    return wordlist


def is_word(word_list, word):  # output is a boolean
    '''
    Determines if word is a valid word, ignoring
    capitalization and punctuation

    word_list (list): list of words in the dictionary.
    word (string): a possible word.

    Returns: True if word is in word_list, False otherwise

    Example:
    >>> is_word(word_list, 'bat') returns
    True
    >>> is_word(word_list, 'asdf') returns
    False
    '''
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
    return word in word_list


def get_story_string():      # output is a string
    """
    Returns: a story in encrypted text.
    """
    f = open("story.txt", "r")
    story = str(f.read())
    f.close()
    return story

### END HELPER CODE ###


WORDLIST_FILENAME = 'words.txt'


class Message(object):                      # takes in a string
    def __init__(self, text):               # a function to initialize the Message class
        '''
        Initializes a Message object

        text (string): the message's text

        a Message object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        self.message_text = text
        self.valid_words = load_words(WORDLIST_FILENAME)

    def get_message_text(self):             # returns the input
        '''
        Used to safely access self.message_text outside of the class

        Returns: self.message_text
        '''
        return self.message_text

    def get_valid_words(self):              # returns a list of words
        '''
        Used to safely access a copy of self.valid_words outside of the class.
        This helps you avoid accidentally mutating class attributes.

        Returns: a COPY of self.valid_words
        '''
        return self.valid_words.copy()

    def build_shift_dict(self, shift):      # returns a dictionary of shifted letters
        '''
        Creates a dictionary that can be used to apply a cipher to a letter.
        The dictionary maps every uppercase and lowercase letter to a
        character shifted down the alphabet by the input shift. The dictionary
        should have 52 keys of all the uppercase letters and all the lowercase
        letters only.

        shift (integer): the amount by which to shift every letter of the
        alphabet. 0 <= shift < 26

        Returns: a dictionary mapping a letter (string) to
                 another letter (string).
        '''
        self.shift = shift
        dictionary = {string.ascii_lowercase[i]: string.ascii_lowercase[(
            i + shift) % 26] for i in range(26)}

        return dictionary

    def apply_shift(self, shift):           # returns a string of shifted letters
        '''
        Applies the Caesar Cipher to self.message_text with the input shift.
        Creates a new string that is self.message_text shifted down the
        alphabet by some number of characters determined by the input shift

        shift (integer): the shift with which to encrypt the message.
        0 <= shift < 26

        Returns: the message text (string) in which every character is shifted
             down the alphabet by the input shift
        '''
        self.shift = shift
        dictionary = self.build_shift_dict(shift)
        shifted_message = ''
        for char in self.message_text:
            if char.lower() in dictionary:
                if char.isupper():
                    shifted_message += dictionary[char.lower()].upper()
                else:
                    shifted_message += dictionary[char]
            else:
                shifted_message += char
        return shifted_message

    def __str__(self):                      # returns the input
        return self.message_text    # returns the input


class PlaintextMessage(Message):            # takes in a string and a shift
    def __init__(self, text, shift):        # a function to initialize the PlaintextMessage class
        '''
        Initializes a PlaintextMessage object

        text (string): the message's text
        shift (integer): the shift associated with this message

        A PlaintextMessage object inherits from Message and has five attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
            self.shift (integer, determined by input shift)
            self.encryption_dict (dictionary, built using shift)
            self.message_text_encrypted (string, created using shift)

        '''
        self.message_text = text
        self.valid_words = load_words(WORDLIST_FILENAME)
        self.shift = shift
        self.encryption_dict = self.build_shift_dict(shift)
        self.message_text_encrypted = self.apply_shift(shift)

    def get_shift(self):                    # returns the shift input
        '''
        Used to safely access self.shift outside of the class

        Returns: self.shift
        '''
        return self.shift

    def get_encryption_dict(self):          # returns a copy of encryption_dict
        '''
        Used to safely access a copy self.encryption_dict outside of the class

        Returns: a COPY of self.encryption_dict
        '''
        return self.encryption_dict.copy()

    def get_message_text_encrypted(self):   # returns message_text_encrypted
        '''
        Used to safely access self.message_text_encrypted outside of the class

        Returns: self.message_text_encrypted
        '''
        return self.message_text_encrypted

    def change_shift(self, shift):          # changes the shift input
        '''
        Changes self.shift of the PlaintextMessage and updates other
        attributes determined by shift.

        shift (integer): the new shift that should be associated with this message.
        0 <= shift < 26

        Returns: nothing
        '''
        self.shift = shift
        self.encryption_dict = self.build_shift_dict(shift)
        self.message_text_encrypted = self.apply_shift(shift)
        pass


class CiphertextMessage(Message):           # takes in a string
    def __init__(self, text):               # a function to initialize the CiphertextMessage class
        '''
        Initializes a CiphertextMessage object

        text (string): the message's text

        a CiphertextMessage object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        self.message_text = text
        self.valid_words = load_words(WORDLIST_FILENAME)

    # returns a tuple of the best shift value and the decrypted message
    def decrypt_message(self):
        '''
        Decrypt self.message_text by trying every possible shift value
        and find the "best" one. We will define "best" as the shift that
        creates the maximum number of real words when we use apply_shift(shift)
        on the message text. If s is the original shift value used to encrypt
        the message, then we would expect 26 - s to be the best shift value
        for decrypting it.

        Note: if multiple shifts are equally good such that they all create
        the maximum number of valid words, you may choose any of those shifts
        (and their corresponding decrypted messages) to return

        Returns: a tuple of the best shift value used to decrypt the message
        and the decrypted message text using that shift value
        '''
        message_text = self.message_text
        message = self.message_text.split(' ')
        shift = 0
        decrypted_message = ''
        for i in range(26):
            for word in message:
                if is_word(self.valid_words, Message(word).apply_shift(i)):
                    shift = i
                    decrypted_message += Message(word).apply_shift(i) + ' '

        for i, letter in enumerate(message_text):
            if letter.isupper():
                decrypted_message[i].upper()
        return (shift, decrypted_message.strip())


if __name__ == '__main__':

    #    Example test case (PlaintextMessage)
    #    plaintext = PlaintextMessage('hello', 2)
    #    print('Expected Output: jgnnq')
    #    print('Actual Output:', plaintext.get_message_text_encrypted())
    #
    #    #Example test case (CiphertextMessage)
    #    ciphertext = CiphertextMessage('jgnnq')
    #    print('Expected Output:', (24, 'hello'))
    #    print('Actual Output:', ciphertext.decrypt_message())

    # TODO: WRITE YOUR TEST CASES HERE

    # TODO: best shift value and unencrypted story

    # TEST CASE 1 for PlaintextMessage: test number 1-25 for lowercase
    # plaintext = PlaintextMessage('hello world', 3)
    # expected_output = 'khoor zruog'
    # print('Expected Output: khoor zruog')
    # print('Actual Output:', plaintext.get_message_text_encrypted())
    # print(expected_output == plaintext.get_message_text_encrypted())
    # # TEST CASE 2 for PlaintextMessage: test number > 25 for lowercase
    # plaintext = PlaintextMessage('z', 26)
    # expected_output = 'z'
    # print('Expected Output: z')
    # print('Actual Output:', plaintext.get_message_text_encrypted())
    # print(expected_output == plaintext.get_message_text_encrypted())
    # # TEST CASE 3 for PlaintextMessage: test number < 0 for lowercase
    # plaintext = PlaintextMessage('a', -1)
    # expected_output = 'z'
    # print('Expected Output: z')
    # print('Actual Output:', plaintext.get_message_text_encrypted())
    # print(expected_output == plaintext.get_message_text_encrypted())
    # # TEST CASE 4 for PlaintextMessage: test number 1-25 for uppercase
    # plaintext = PlaintextMessage('A', 25)
    # expected_output = 'Z'
    # print('Expected Output: Z')
    # print('Actual Output:', plaintext.get_message_text_encrypted())
    # print(expected_output == plaintext.get_message_text_encrypted())
    # # TEST CASE 5 for PlaintextMessage: test number > 25 for uppercase
    # plaintext = PlaintextMessage('Z', 26)
    # expected_output = 'Z'
    # print('Expected Output: Z')
    # print('Actual Output:', plaintext.get_message_text_encrypted())
    # print(expected_output == plaintext.get_message_text_encrypted())
    # # TEST CASE 6 for PlaintextMessage: test number < 0 for uppercase
    # plaintext = PlaintextMessage('A', -1)
    # expected_output = 'Z'
    # print('Expected Output: Z')
    # print('Actual Output:', plaintext.get_message_text_encrypted())
    # print(expected_output == plaintext.get_message_text_encrypted())
    # # TEST CASE 7 for PlaintextMessage: test if input has a number
    # plaintext = PlaintextMessage('A1', 1)
    # expected_output = 'B1'
    # print('Expected Output: B1')
    # print('Actual Output:', plaintext.get_message_text_encrypted())
    # print(expected_output == plaintext.get_message_text_encrypted())

    # TEST CASE 1 for CipherText: test for lowercase
    # ciphertext = CiphertextMessage('khoor zruog')
    # print('Expected Output:', (23, 'hello world'))
    # print('Actual Output:', ciphertext.decrypt_message())

    # TEST CASE 2 for CipherText: test for uppercase
    # ciphertext = CiphertextMessage('KHOOR ZRUOG')
    # print('Expected Output:', (23, 'HELLO WORLD'))
    # print('Actual Output:', ciphertext.decrypt_message())

    # TEST CASE 7 for CipherText: test if input has a number
    # doesn't work because the function doesn't recognize the number as a word
    # ciphertext = CiphertextMessage('khoor1 zruog')
    # print('Expected Output:', (23, 'hello1 world'))
    # print('Actual Output:', ciphertext.decrypt_message())

    # DECODE STORY
    story = get_story_string()
    print(story)
    # ciphertext = CiphertextMessage(story)
    # print('Decoded Story:', ciphertext.decrypt_message())
