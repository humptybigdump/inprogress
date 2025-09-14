import random

# Dieses dictionary dient lediglich zur Ausgabe in der Console.
# Es wird in der Klasse Card und Stack für die magische Methode '__str__' verwendet
n = [i for i in range(14) if i != 11]
uni_cards = {
    'hearts': {v+1: chr(127153 + n[v]) for v in range(13)},
    'spades': {v+1: chr(127137 + n[v]) for v in range(13)},
    'facedown': chr(127136)
}
# Falls die Kartensymbole schlecht lesbar sind:
#uni_cards = {
#    'hearts': {v+1: "H{:02}".format(v+1) for v in range(13)},
#    'spades': {v+1: "S{:02}".format(v+1) for v in range(13)},
#    'facedown': "|X|"
#}


class Card:
    """
    Eine einzelne Spielkarte, die Informationen bzgl Kartenwert und -Farbe speichert.
    """
    def __init__(self, value, suit):
        self._value = value
        self._suit = suit
    
    def get_value(self):
        "Liefert den Wert der Karte"
        return self._value

    def get_suit(self):
        "Liefert die Farbe der Karte"
        return self._suit

    def fits_to(self, card, matching_suit=True):
        "Prueft, ob diese Karte an eine andere angehaengt werden kann"
        if matching_suit:
            return self._value + 1 == card.get_value() and self._suit == card.get_suit()
        else:
            return self._value + 1 == card.get_value() and self._suit != card.get_suit()

    def __str__(self):
        return uni_cards[self._suit][self._value]


class Sequence:
    """
    Diese Klasse modelliert eine absteigende Sequenz von Karten
    """
    def __init__(self, list_of_cards):
        if not list_of_cards:
            # TODO: Durch das Werfen einer Exception ersetzen
            print("Inconsistent sequence - empty!")
            return

        card = list_of_cards[0]
        for current_card in list_of_cards[1:]:
            if not current_card.fits_to(card):
                # TODO: Durch das Werfen einer Exception ersetzen
                print("Inconsistent sequence {}!".format("-".join(map(str, list_of_cards))))
                return
            card = current_card

        self._cards = list_of_cards

    def first_card(self):
        "Liefert die erste Karte dieser Sequenz"
        return self._cards[0]

    def last_card(self):
        "Liefert die letzte Karte dieser Sequenz"
        return self._cards[-1]

    def is_full(self):
        "Prueft, ob die Sequenz vollstaendig ist, also alle 13 Karten beinhaltet."
        return len(self._cards) == 13

    def fits_to(self, other, matching_suit=True):
        "Prueft, ob diese Sequenz an eine andere angehaengt werden kann"
        return self.first_card().fits_to(other.last_card(), matching_suit=matching_suit)

    def merge(self, other):
        "Kombiniert diese Sequenz mit einer anderen, indem die andere Sequenz angehaengt wird."
        if not other.fits_to(self):
            # TODO: Durch das Werfen einer Exception ersetzen
            print(f"Can't merge sequences {self} and {other}!")
            return

        self._cards += other._cards
    
    def split(self, index):
        "Teilt diese Sequenz am gegebenen Index und liefert eine neue Sequenz mit den abgetrennten Karten."
        # wuerde eine leere Sequenz hinterlassen oder absplitten
        if not (0 < index < len(self._cards)):
            # TODO: Durch das Werfen einer Exception ersetzen
            print(f"Unsupported Split at index {index}")
            return
        
        splitted = Sequence(self._cards[index:])
        self._cards[:] = self._cards[:index]
        return splitted

    # TODO: Hier kommt Ihr Code

    def __str__(self):
        return "-".join(map(str, self._cards))


class Stack:
    """
    Ein Stapel von Sequenzen. Diese Klasse modelliert die einzelnen Stapel des Spiels.
    Neben den Sequenzen, welche den aufgedeckten Karten entsprechen, merkt sich ein Stapel noch die umgedrehten/verdeckten Karten.
    """
    def __init__(self, card, facedown_cards):
        self._sequences = [Sequence([card])]
        self._facedown_cards = facedown_cards

    def is_empty(self):
        "Prueft, ob dieser Stapel leer ist, es also keine offenen Karten mehr gibt."
        return not self._sequences

    def last_sequence(self):
        "Liefert die letzte Sequenz in diesem Stapel"
        # Stapel darf nicht leer sein
        if self.is_empty():
            # TODO: Durch das Werfen einer Exception ersetzen
            print("Stack is empty!")
            return

        return self._sequences[-1]
    
    def append_sequence(self, seq):
        "Fuegt dem Stapel eine Sequenz hinzu"
        self._sequences.append(seq)
    
    def remove_last_sequence(self):
        "Entfernt die letzte Sequenz dieses Stapels"
        # Stapel darf nicht leer sein
        if self.is_empty():
            # TODO: Durch das Werfen einer Exception ersetzen
            print("Stack is empty!")
            return

        self._sequences.pop()
        # alternativ
        # del self._sequences[-1]

    def test_revealcard(self):
        """
        Deckt, wenn moeglich, eine neue Karte von den zugedeckten Karten auf.
        Dafuer muss der Stapel leer sein und es muss noch zugedeckte geben.
        """
        if self.is_empty() and self._facedown_cards:
            self.append_sequence(Sequence([self._facedown_cards.pop()]))

    def test_fullsequence(self):
        "Prueft, ob die letzte Sequenz vollstaendig ist und deckt in diesem Fall eine neue Karte auf."
        if self.last_sequence().is_full():
            self._sequences.pop()
            self.test_revealcard()
    
    def deal_card(self, card):
        """
        Realisiert das Austeilen einer Karte auf den Stapel.
        Die Karte wird entweder an die untersten Sequenz angehaengt oder es wird eine neue erzeugt.
        Im ersten Fall kann eine vollstaendige Sequenz entstehen und muss deshalb durch 'test_fullsequence()' ueberprueft werden.
        """
        seq = Sequence([card])

        # TODO: Dieser Code soll durch ein geeignetes try-except-Konstrukt ersetzt werden
        if seq.fits_to(self.last_sequence()):
            self.last_sequence().merge(seq)
            self.test_fullsequence()
        else:
            self.append_sequence(seq)
    
    @property
    def num_facedown_cards(self):
        """
        Liefert die Anzahl an verdeckten Karten dieses Stapels
        """
        return len(self._facedown_cards)
    
    # TODO: Hier kommt Ihr Code

    def __str__(self):
        return " ".join(self.num_facedown_cards *  [uni_cards['facedown']] + list(map(str, self._sequences)))


class SpiderSolitaire:
    ALL_CARDS = [Card(value, suit) for value in range(1, 14) for suit in ["hearts", "spades"]]
    """
    Klasse, die das ganze Spielfeld an sich verwaltet.
    """
    def __init__(self):
        # wir starten mit allen Karten (4 ganze Kartendecks mit jeweils 13 Herz und 13 Pik)
        self._stack2deal = 4 * SpiderSolitaire.ALL_CARDS
        # Durchmischen aller Karten
        random.shuffle(self._stack2deal)

        # Anzahl verdeckter Karten pro Stapel
        cards2deal_perstack = [5, 5, 5, 5, 4, 4, 4, 4, 4, 4]

        # Es werden 10 Stapel erzeugt und in self._stacks gespeichert. 
        # Jeder Stapel bekommt hierbei die entsprechende Anzahl verdeckter Karten und die eine aufgedeckte Karte uebergeben.
        self._stacks = []
        for k in range(10):
            facedown_cards = [self._stack2deal.pop() for _ in range(cards2deal_perstack[k])]
            self._stacks.append(Stack(self._stack2deal.pop(), facedown_cards))
        
        # Sequenz unter dem Mauszeiger/bewegende Sequenz
        self.moving_sequence = None
        # Woher kam die bewegte Sequenz
        self.origin_stack_index = None
    
    # TODO: Hier kommt Ihr Code

    @property
    def num_cards2deal(self):
        """
        Liefert die Anzahl an noch auszuteilenden Karten
        """
        return len(self._stack2deal)

    def deal(self):
        """
        Teilt an jeden der 10 Stapel eine Karte aus.
        Vorher muss geprueft werden, ob es noch Karten zum austeilen gibt und auf jedem Stapel mindestens eine aufgedeckte Karte liegt.
        """
        if self.num_cards2deal == 0:
            # TODO: Durch das Werfen einer Exception ersetzen
            print("All cards have already been dealt")
            return

        empty_stacks = [i for i, stack in enumerate(self._stacks) if stack.is_empty()]
        if empty_stacks:
            # TODO: Durch das Werfen einer Exception ersetzen
            print("There must be at least one card at every stack!")
            return

        for stack in self._stacks:
            stack.deal_card(self._stack2deal.pop())

    def pick_up(self, stack_index, card_index):
        """
        'Aufheben' einer Sequenz
        """
        if self.moving_sequence is not None:
            # TODO: Durch das Werfen einer Exception ersetzen
            print("Already moving!")
            return
        
        if not (0 <= stack_index < 10):
            # TODO: Durch das Werfen einer Exception ersetzen
            print("Wrong index for stack!")
            return
        
        stack = self._stacks[stack_index]
        
        # -------------------------------------------------------------------------------------#
        # TODO: Dieser Code soll durch ein geeignetes try-except-Konstrukt ersetzt werden
        # kann nicht von leerem Stapel aufheben
        if stack.is_empty():
            print("Stack is empty!")
            return
        
        if card_index == 0:
            self.moving_sequence = stack.last_sequence()
            stack.remove_last_sequence()
        else:
            splitted = stack.last_sequence().split(card_index)
            # card_index war nicht zulaessig
            if splitted is None:
                return
            else:
                self.moving_sequence = splitted
        # -------------------------------------------------------------------------------------#
        
        self.origin_stack_index = stack_index
    
    def abort_move(self):
        "'Abbruch' des Bewegvorgangs"
        if self.moving_sequence is not None:
            source_stack = self._stacks[self.origin_stack_index]

            # -------------------------------------------------------------------------------------#
            # TODO: Dieser Code soll durch ein geeignetes try-except-Konstrukt ersetzt werden
            # Ursprungsstapel leer oder bewegende Sequenz passt nicht zum Ursprungsstapel -> append
            if source_stack.is_empty() or not self.moving_sequence.fits_to(source_stack.last_sequence()):
                source_stack.append_sequence(self.moving_sequence)
            # Sequenz passt zum Urspringsstapel -> merge
            else:
                source_stack.last_sequence().merge(self.moving_sequence)
            # -------------------------------------------------------------------------------------#
            
            # reset containers
            self.moving_sequence = None
            self.origin_stack_index = None
    
    def move(self, stack_index):
        "'Bewegen' einer (Teil-) Sequenz"
        if self.moving_sequence is None:
            # TODO: Durch das Werfen einer Exception ersetzen
            print("There is nothing to move. Call 'pick_up' first.")
            return
        
        if stack_index is None or stack_index == self.origin_stack_index:
            self.abort_move()
            return
        
        if not (0 <= stack_index < 10):
            self.abort_move()
            # TODO: Durch das Werfen einer Exception ersetzen
            print("Wrong index for stack")
            return

        target_stack = self._stacks[stack_index]
        source_stack = self._stacks[self.origin_stack_index]
                
        # Stapel ist leer oder Sequenz passt nur im Wert (Farben verschieden) -> Haenge Sequenz an Stapel an
        if target_stack.is_empty() or self.moving_sequence.fits_to(target_stack.last_sequence(), matching_suit=False):
            target_stack.append_sequence(self.moving_sequence)
            source_stack.test_revealcard()
        # Sequenz kann an bestehende Sequenz angehaengt werden
        elif self.moving_sequence.fits_to(target_stack.last_sequence(), matching_suit=True):
            target_stack.last_sequence().merge(self.moving_sequence) 
            target_stack.test_fullsequence()
            source_stack.test_revealcard()
        # Sequenz passt nicht -> Lege Sequenz zurueck auf den urspruenglichen Stapel
        else:
            self.abort_move()
            # TODO: Durch das Werfen einer Exception ersetzen
            print("Move not possible!")
            return
        
        # reset containers
        self.moving_sequence = None
        self.origin_stack_index = None

    def is_won(self):
        "Gibt True zurück, wenn das Spiel gewonnen wurde."
        return all(stack.is_empty() for stack in self._stacks)

    def play(self):
        "Die Spielschleife. Gibt True zurück, wenn das Spiel gewonnen wurde."
        # Wir sind gerade dabei eine Sequenz zu bewegen
        if self.moving_sequence is not None:
            print("picked up: " + str(self.moving_sequence))
            print("Options:")
            print("k    move sequence to stack k")
            print('"b"  move sequence back to original stack {}'.format(self.origin_stack_index))
            
            user_in = input("Input: ").strip().lower()
            
            # Zuruecklegen auf den ursprungsstapel (Abbruch)
            if user_in == "b":
                self.abort_move()
                return
            
            try:
                stack_index = int(user_in)
            except ValueError:
                print("Wrong input!")
                return
                
            self.move(stack_index)
            
            # Gewinnabfrage
            if self.is_won():
                print("Congratulations, you won!")
                return True
        else:
            print("Options:")
            # es gibt noch Karten zum Austeilen
            if self.num_cards2deal > 0:
                print('"d"   deal (there are still {} cards to deal)'.format(self.num_cards2deal))                
            print("k, n  pick up the last subsequence (part [n:]) of stack k")
            print("k     pick up the last sequence of stack k")
            user_in = input("Input: ").strip().lower()
        
            # Austeilen
            if user_in == "d":
                self.deal()
                return

            try:
                splitted = user_in.split(",")
                # nur Stacknummer eingegeben
                if len(splitted) == 1:
                    stack_index, card_index = int(splitted[0]), 0
                # beides eingegeben
                else:
                    stack_index, card_index = map(int, splitted)
            except ValueError:
                print("Wrong input!")
                return
            
            self.pick_up(stack_index, card_index)

    def __str__(self):
        res = [f"{i} {stack}" for i, stack in enumerate(self._stacks)]
        return "\n".join(res)


# TODO: Hier kommt Ihr Code


if __name__ == "__main__":
    ss = SpiderSolitaire()

    print("Teste 'SpiderSolitaire.iter_stacks()' and 'Stack.iter_faceup_cards()':")
    for stack in ss.iter_stacks():
        for card in stack.iter_faceup_cards():
            print(card, end=" ")
        print()

    # zum Testen des 'DealError' koennen folgende Zeilen einkommentiert werden
    #ss._stacks[0]._sequences = []
    #ss._stacks[1]._sequences = []


    is_won = False
    while not is_won:
        print()
        print(ss)
        
        # TODO: Hier kommt Ihr Code
        is_won = ss.play()
