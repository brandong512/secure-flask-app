class Validation:
    @staticmethod
    def isNumericString(string):
        if any(not letter.isdigit() for letter in string):
            return False

        return True

    @staticmethod
    def isBlank(myString):
        return not (myString and myString.strip())
