import unittest
import string
import types
import os

import verschluesselung_vererbung


def skip_not_impl(obj, *attr):
    c_obj = obj
    # recursively check if 'attr' exists in 'obj'
    for name in attr:
        if not hasattr(c_obj, name):
            break
        c_obj = getattr(c_obj, name)
    else:
        if type(c_obj) == types.FunctionType:
            return lambda f: f
    
    return unittest.skip("{!r} is not yet implemented.".format(".".join(attr)))


def counter(func):
    count = 0

    def f(*args, **kwargs):
        nonlocal count
        count += 1
        return func(*args, *kwargs)

    def get_count():
        return count

    return f, get_count
    

class EncryptionTests(unittest.TestCase):
    @skip_not_impl(verschluesselung_vererbung, "Encryptor", "decrypt_character")
    @skip_not_impl(verschluesselung_vererbung, "Encryptor", "decrypt_string")
    def test_b(self):
        "b)\t'decrypt_string' - Test"
        encryptor = verschluesselung_vererbung.Encryptor("Encryptor")
        encryptor.decrypt_character, get_decrypt_character_count = counter(encryptor.decrypt_character)

        # check result
        self.assertEqual(encryptor.decrypt_string(string.ascii_letters), string.ascii_letters)
        # check if encryptor.decrypt_character was called
        self.assertEqual(get_decrypt_character_count(), len(string.ascii_letters), msg="Fuer 'Encryptor.decrypt_string' soll 'Encryptor.decrypt_character' verwendet werden.")

    @skip_not_impl(verschluesselung_vererbung, "CaseInsensitiveEncryptor", "encrypt_upper_character")
    @skip_not_impl(verschluesselung_vererbung, "CaseInsensitiveEncryptor", "encrypt_character")
    def test_c_i(self):
        "c)\t'encrypt_character' - Test"
        encryptor = verschluesselung_vererbung.CaseInsensitiveEncryptor("CaseInsensitive")
        encrypt_upper_character, get_encrypt_upper_count = counter(encryptor.encrypt_upper_character)

        def encrypt_upper_character_checker(c):
            self.assertTrue(c.isalpha(), msg="'Encryptor.encrypt_upper_character' wird mit einem nicht-Buchstaben aufgerufen.")
            self.assertTrue(c.isupper(), msg="'Encryptor.encrypt_upper_character' wird mit einem Kleinbuchstaben aufgerufen.")
            res = encrypt_upper_character(c)
            self.assertTrue(res.isalpha(), msg="Der Returnwert von 'Encryptor.encrypt_upper_character' ist ein kein Buchstabe.")
            self.assertTrue(res.isupper(), msg="Der Returnwert von 'Encryptor.encrypt_upper_character' ist ein kein GroßBuchstabe.")

            return res

        encryptor.encrypt_upper_character = encrypt_upper_character_checker
        

        ref_count = 0
        for c in string.printable:
            # check output
            self.assertEqual(encryptor.encrypt_character(c), c)
            # check call to Enrcryptor.encrypt_upper_character
            if c.isalpha():
                ref_count += 1
 
            self.assertEqual(get_encrypt_upper_count(), ref_count, msg="Fuer Buchstaben soll 'Encryptor.encrypt_upper_character' verwendet werden.\n"
                "Nicht-Buchstaben sollen so wie sie sind zurueckgegeben werden.")

    @skip_not_impl(verschluesselung_vererbung, "CaseInsensitiveEncryptor", "decrypt_upper_character")
    @skip_not_impl(verschluesselung_vererbung, "CaseInsensitiveEncryptor", "decrypt_character")
    def test_c_ii(self):
        "c)\t'decrypt_character' - Test"
        encryptor = verschluesselung_vererbung.CaseInsensitiveEncryptor("CaseInsensitive")
        decrypt_upper_character, get_decrypt_upper_count = counter(encryptor.decrypt_upper_character)

        def decrypt_upper_character_checker(c):
            self.assertTrue(c.isalpha(), msg="'Encryptor.decrypt_upper_character' wird mit einem nicht-Buchstaben aufgerufen.")
            self.assertTrue(c.isupper(), msg="'Encryptor.decrypt_upper_character' wird mit einem Kleinbuchstaben aufgerufen.")
            res = decrypt_upper_character(c)
            self.assertTrue(res.isalpha(), msg="Der Returnwert von 'Encryptor.decrypt_upper_character' ist kein Buchstabe.")
            self.assertTrue(res.isupper(), msg="Der Returnwert von 'Encryptor.decrypt_upper_character' ist kein GroßBuchstabe.")

            return res
        
        encryptor.decrypt_upper_character = decrypt_upper_character_checker
        
        ref_count = 0
        for c in string.printable:
            # check output
            self.assertEqual(encryptor.decrypt_character(c), c)
            # check call to Enrcryptor.encrypt_upper_character
            if c.isalpha():
                ref_count += 1
 
            self.assertEqual(get_decrypt_upper_count(), ref_count, msg="Fuer Buchstaben soll 'Encryptor.decrypt_upper_character' verwendet werden.\n"
                "Nicht-Buchstaben sollen so wie sie sind zurueckgegeben werden.")


class CaesarTests(unittest.TestCase):
    @skip_not_impl(verschluesselung_vererbung, "CaesarEncryptor", "__init__")
    def test_e_i(self):
        "e)\t'Konstruktor' - Test"
        encryptor = verschluesselung_vererbung.CaesarEncryptor(5)
        self.assertEqual(encryptor.name, "Caesar", msg="Wurde der Konstruktor der Basisklasse aufgerufen?")

    @skip_not_impl(verschluesselung_vererbung, "CaesarEncryptor", "encrypt_upper_character")
    def test_e_ii(self):
        "e)\t'encrypt_upper_character' - Test"
        encryptor = verschluesselung_vererbung.CaesarEncryptor(5)
        comp = "FGHIJKLMNOPQRSTUVWXYZABCDE"

        for i, c in enumerate(string.ascii_uppercase):
            self.assertEqual(encryptor.encrypt_upper_character(c), comp[i])
    
    @skip_not_impl(verschluesselung_vererbung, "CaesarEncryptor", "decrypt_upper_character")
    def test_e_iii(self):
        "e)\t'decrypt_upper_character' - Test"
        encryptor = verschluesselung_vererbung.CaesarEncryptor(5)
        comp = "FGHIJKLMNOPQRSTUVWXYZABCDE"

        for i, c in enumerate(comp):
            self.assertEqual(encryptor.decrypt_upper_character(c), string.ascii_uppercase[i])

    @skip_not_impl(verschluesselung_vererbung, "CaesarEncryptor", "encrypt_file")
    def test_f_i(self):
        "f)\t'encrypt_file' - Test"
        encryptor = verschluesselung_vererbung.CaesarEncryptor(13)
        encryptor.encrypt_string, get_encrypt_string_count = counter(encryptor.encrypt_string)
        encryptor.decrypt_string, get_decrypt_string_count = counter(encryptor.decrypt_string)

        with open("test_case_f_i.tmp", "w") as f:
            f.write("bC.")

        encryptor.encrypt_file("test_case_f_i.tmp", "test_case_f_i2.tmp")
        os.remove("test_case_f_i.tmp")
        
        self.assertTrue(os.path.isfile("test_case_f_i2.tmp"), msg="Zieldatei wurde nicht erstellt.")

        self.assertTrue(get_encrypt_string_count() > 0, msg="encrypt_string wurde nie aufgerufen.")
        self.assertTrue(get_decrypt_string_count() == 0, msg="decrypt_string sollte hier nich aufgerufen werden.")

        with open("test_case_f_i2.tmp") as f:
            res = f.read()
        os.remove("test_case_f_i2.tmp")

        self.assertEqual(res, "Encryptor: Caesar\noP.")

    @skip_not_impl(verschluesselung_vererbung, "CaesarEncryptor", "decrypt_file")
    def test_f_ii(self):
        "f)\t'decrypt_file' - Test"
        encryptor = verschluesselung_vererbung.CaesarEncryptor(13)
        encryptor.encrypt_string, get_encrypt_string_count = counter(encryptor.encrypt_string)
        encryptor.decrypt_string, get_decrypt_string_count = counter(encryptor.decrypt_string)

        with open("test_case_f_ii.tmp", "w") as f:
            f.write("Encryptor: Caesar\noP.")

        encryptor.decrypt_file("test_case_f_ii.tmp", "test_case_f_ii2.tmp")
        os.remove("test_case_f_ii.tmp")

        self.assertTrue(os.path.isfile("test_case_f_ii2.tmp"), msg="target-Datei wurde nicht erstellt.")
        
        self.assertTrue(get_decrypt_string_count() > 0, msg="decrypt_string wurde nie aufgerufen.")
        self.assertTrue(get_encrypt_string_count() == 0, msg="encrypt_string sollte hier nich aufgerufen werden.")

        with open("test_case_f_ii2.tmp") as f:
            res = f.read()
        os.remove("test_case_f_ii2.tmp")

        self.assertEqual(res, "bC.")


class VigenereTests(unittest.TestCase):
    @skip_not_impl(verschluesselung_vererbung, "VigenereEncryptor", "__init__")
    def test_g_i(self):
        "g)\t'Konstruktor' - Test"
        encryptor = verschluesselung_vererbung.VigenereEncryptor("PYTHON")
        self.assertEqual(encryptor.name, "Vigenere", msg="Wurde der Konstruktor der Basisklasse aufgerufen?")

    @skip_not_impl(verschluesselung_vererbung, "VigenereEncryptor", "encrypt_upper_character")
    def test_g_ii(self):
        "g)\t'encrypt_upper_character' - Test"
        encryptor = verschluesselung_vererbung.VigenereEncryptor("TEST")
        comp = "TFUWXJYABNCEFRGIJVKMNZOQRD"

        for i, c in enumerate(string.ascii_uppercase):
            self.assertEqual(encryptor.encrypt_upper_character(c), comp[i])

    
    @skip_not_impl(verschluesselung_vererbung, "VigenereEncryptor", "decrypt_upper_character")
    def test_g_iii(self):
        "g)\t'decrypt_upper_character' - Test"
        encryptor = verschluesselung_vererbung.VigenereEncryptor("TEST")
        comp = "TFUWXJYABNCEFRGIJVKMNZOQRD"

        for i, c in enumerate(comp):
            self.assertEqual(encryptor.decrypt_upper_character(c), string.ascii_uppercase[i])
    
    @skip_not_impl(verschluesselung_vererbung, "VigenereEncryptor", "encrypt_file")
    def test_g_iv(self):
        "g)\t'encrypt_file' - Test"
        encryptor = verschluesselung_vererbung.VigenereEncryptor("BFGC")

        with open("test_case_h_i.tmp", "w") as f:
            f.write("4bC.")

        encryptor.encrypt_file("test_case_h_i.tmp", "test_case_h_i2.tmp")
        os.remove("test_case_h_i.tmp")
        
        self.assertTrue(os.path.isfile("test_case_h_i2.tmp"), msg="Zieldatei wurde nicht erstellt.")

        with open("test_case_h_i2.tmp") as f:
            res = f.read()
        os.remove("test_case_h_i2.tmp")

        self.assertEqual(res, "Encryptor: Vigenere\n4cH.")

    @skip_not_impl(verschluesselung_vererbung, "VigenereEncryptor", "decrypt_file")
    def test_g_v(self):
        "g)\t'decrypt_file' - Test"
        encryptor = verschluesselung_vererbung.VigenereEncryptor("BFGC")

        with open("test_case_h_ii.tmp", "w") as f:
            f.write("Encryptor: Vigenere\n4cH.")

        encryptor.decrypt_file("test_case_h_ii.tmp", "test_case_h_ii2.tmp")
        os.remove("test_case_h_ii.tmp")

        self.assertTrue(os.path.isfile("test_case_h_ii2.tmp"), msg="Zieldatei wurde nicht erstellt.")

        with open("test_case_h_ii2.tmp") as f:
            res = f.read()
        os.remove("test_case_h_ii2.tmp")

        self.assertEqual(res, "4bC.")


class Result(unittest.TextTestResult):
    def getDescription(self, test):
        doc_first_line = test.shortDescription()
        if self.descriptions and doc_first_line:
            return doc_first_line
        else:
            return str(test)

    def addSkip(self, test, reason):
        unittest.TestResult.addSkip(self, test, reason)
        if self.showAll:
            self.stream.writeln("skipped ({})".format(reason))
        elif self.dots:
            self.stream.write("s")
            self.stream.flush()
    
    def wasSuccessful(self):
        return len(self.failures) == len(self.errors) == len(self.skipped) == 0


_failed = False
def run_test(test, msg):
    global _failed
    if _failed:
        return

    suite = unittest.defaultTestLoader.loadTestsFromTestCase(test)
    l = len(msg) + 8
    line = "+" + "-" * l + "+"
    print(line + "\n|    " + msg + "    |\n" + line)
    res = unittest.TextTestRunner(verbosity=2, failfast=True, resultclass=Result).run(suite)
    if not res.wasSuccessful():
        _failed = True


if __name__ == "__main__":
    run_test(EncryptionTests, "Testing Encryption")
    
    print()
    run_test(CaesarTests, "Testing 'CaesarEncryptor'")
    
    print()
    run_test(VigenereTests, "Testing 'VigenereEncryptor'")
