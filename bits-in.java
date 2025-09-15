int leftShifted = someVariable << bits; // verschiebt Bits in "someVariable" um "bits" nach links und füllt rechts mit Null-Bits auf
int rightShifted = someVariable >>> bits; // verschiebt Bits in "someVariable" um "bits" nach rechts und füllt links mit Null-Bits auf
int bitmask = 1 << (bit); // Bitmaske mit genau einem gesetzten Bit an Position "bit", entspricht binär 2^bit
int invBitmask = ~bitmask; // invertierte Bitmaske, alle Bits außer "bit" sind gesetzt
int singleBit = someVariable & bitmask; // Einzelnes Bit aus "someVariable" extrahieren. Wenn das Bit gesetzt ist, gilt singleBit==bitmask; sonst singleBit==0
int clearedBit = someVariable & invBitmask; // Setzt einzelnes Bit "bit" in "someVariable" auf 0
int setBit = someVariable | bitmask; // Setzt einzelnes Bit "bit" in "someVariable" auf 1
int toggledBit = someVariable ^ bitmask; // Invertiert einzelnes Bit "bit" in "someVariable"
