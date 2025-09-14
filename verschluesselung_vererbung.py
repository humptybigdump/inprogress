class Encryptor:
    def __init__(self, name):
        self.name = name

    def encrypt_character(self, c):
        return c

    def decrypt_character(self, c):
        return c

    def encrypt_string(self, s):
        return "".join(map(self.encrypt_character, s))

    def decrypt_string(self, s):
        pass  # Hier kommt Ihr Code (Aufgabenteil b))

    def encrypt_file(self, source_fn, target_fn):
        pass  # Hier kommt Ihr Code (Aufgabenteil f))

    def decrypt_file(self, source_fn, target_fn):
        pass  # Hier kommt Ihr Code (Aufgabenteil f))


class CaseInsensitiveEncryptor(Encryptor):
    def encrypt_upper_character(self, c):
        return c

    def decrypt_upper_character(self, c):
        return c

    def encrypt_character(self, c):
        pass  # Hier kommt Ihr Code (Aufgabenteil c))

    def decrypt_character(self, c):
        pass  # Hier kommt Ihr Code (Aufgabenteil c))



class CaesarEncryptor(CaseInsensitiveEncryptor):
    pass # Hier kommt Ihr Code (Aufgabenteil e))


class VigenereEncryptor(CaseInsensitiveEncryptor):
    pass # Hier kommt Ihr Code (Aufgabenteil g))


if __name__ == "__main__":
    C = CaesarEncryptor(13)
    print(C.decrypt_string("Bo zna qnf jvexyvpu Irefpuyhrffryhat araara fbyygr..."), end="\n\n")

    decrypted = C.decrypt_file("rot13.txt", "clear.txt")
    print(decrypted, end="\n\n")
    
    text = "DIESER TEXT IST GEHEIM"
    print("Klartext:", text)    
    G = VigenereEncryptor("PYTHON")
    encrypted = G.encrypt_string(text)
    print("Verschlüsselter Text:", encrypted)
    G = VigenereEncryptor("PYTHON")
    print("Entschlüsselter Text:", G.decrypt_string(encrypted), end="\n\n")
    
    V = VigenereEncryptor("PYTHONISTTOLL")
    decrypted = V.decrypt_string('''Upxbrr, auahsypg Ehlhgmjynbvpc,
Rhjvgmj tng Pwnqbba,
Jqj uxhcpicg mshmjmkiyvtl,
Apaztalvvp, otgg Osvtazmix!
Otggl Nnctxk ptyscg dwrlwk
Pod oxc Fvrr alkxbr rtrxpzg;
Idex Apyhaalb jmjwxb Mcjcwlf,
Jw vxbb dlcdmlf Stmxzsw htgea.''')    
    print(decrypted)
