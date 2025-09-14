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
            raise Exception("Inconsistent sequence - empty!")

        card = list_of_cards[0]
        for current_card in list_of_cards[1:]:
            if not current_card.fits_to(card):
                raise Exception("Inconsistent sequence {}!".format("-".join(map(str, list_of_cards))))
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
            raise UnsupportedMerge(f"Can't merge sequences {self} and {other}!")

        self._cards += other._cards
    
    def split(self, index):
        "Teilt diese Sequenz am gegebenen Index und liefert eine neue Sequenz mit den abgetrennten Karten."
        # wuerde eine leere Sequenz hinterlassen oder absplitten
        if not (0 < index < len(self._cards)):
            raise UnsupportedSplit(index == 0)

        splitted = Sequence(self._cards[index:])
        self._cards[:] = self._cards[:index]
        return splitted
    
    def __iter__(self):
        """
        Macht die Klasse Sequence iterierbar.
        """
        return iter(self._cards)
        # alternativ:
        #for card in self._cards:
        #    yield card
        # oder auch:
        # yield from self._cards
    
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
            raise NoLastSequence("Stack is empty!")

        return self._sequences[-1]
    
    def append_sequence(self, seq):
        "Fuegt dem Stapel eine Sequenz hinzu"
        self._sequences.append(seq)
    
    def remove_last_sequence(self):
        "Entfernt die letzte Sequenz dieses Stapels"
        # Stapel darf nicht leer sein
        if self.is_empty():
            raise NoLastSequence("Stack is empty!")

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

        try: 
            self.last_sequence().merge(seq)
            self.test_fullsequence()
        except UnsupportedMerge:
            self.append_sequence(seq)
    
    @property
    def num_facedown_cards(self):
        """
        Liefert die Anzahl an verdeckten Karten dieses Stapels
        """
        return len(self._facedown_cards)
    
    def iter_faceup_cards(self):
        """
        Liefert einen Iterator ueber alle Karten dieses Stapels
        """
        for seq in self._sequences:
            for card in seq:
                yield card

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

    def iter_stacks(self):
        """
        Liefert einen Iterator ueber alle Stapel
        """
        return iter(self._stacks)

    def get_stack(self, stack_index):
        return self._stacks[stack_index]

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
            raise SpiderSolitaireError("All cards have already been dealt.")

        empty_stacks = [i for i, stack in enumerate(self._stacks) if stack.is_empty()]
        if empty_stacks:
            raise DealError(empty_stacks)

        for stack in self._stacks:
            stack.deal_card(self._stack2deal.pop())
    
    def pick_up(self, stack_index, card_index):
        """
        'Aufheben' einer Sequenz
        """
        if self.moving_sequence is not None:
            raise SpiderSolitaireError("Already moving!")
        
        if not (0 <= stack_index < 10):
            raise SpiderSolitaireError("Wrong index for stack!")
        
        stack = self._stacks[stack_index]

        try:
            self.moving_sequence = stack.last_sequence().split(card_index)
        # kann nicht von leerem Stapel aufheben
        except NoLastSequence:
            raise SpiderSolitaireError(f"Stack {stack_index} is empty!")
        except UnsupportedSplit as e:
            # wir heben die komplette Sequenz auf -> entferne Sequenz aus dem Stapel
            if e.full_split:
                self.moving_sequence = stack.last_sequence()
                stack.remove_last_sequence()
            # wir wuerden eine leere Sequenz aufheben
            else:
                raise SpiderSolitaireError("Wrong index for sequence!")
        
        self.origin_stack_index = stack_index
    
    def abort_move(self):
        "'Abbruch' des Bewegvorgangs"
        if self.moving_sequence is not None:
            source_stack = self._stacks[self.origin_stack_index]

            try:
                source_stack.last_sequence().merge(self.moving_sequence)
            # Ursprungsstapel leer oder bewegende Sequenz passt nicht zum Ursprungsstapel -> append
            except (NoLastSequence, UnsupportedMerge):  
                source_stack.append_sequence(self.moving_sequence)

            # reset containers
            self.moving_sequence = None
            self.origin_stack_index = None
    
    def move(self, stack_index):
        "'Bewegen' einer (Teil-) Sequenz"
        if self.moving_sequence is None:
            raise SpiderSolitaireError("There is nothing to move. Call 'pick_up' first.")
        
        if stack_index is None or stack_index == self.origin_stack_index:
            self.abort_move()
            return
        
        if not (0 <= stack_index < 10):
            self.abort_move()
            raise SpiderSolitaireError("Wrong index for stack")

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
            raise SpiderSolitaireError("Move not possible!")
        
        # reset containers
        self.moving_sequence = None
        self.origin_stack_index = None
    
    def is_won(self):
        return all(stack.is_empty() for stack in self._stacks)

    def __str__(self):
        res = [f"{i} {stack}" for i, stack in enumerate(self._stacks)]
        return "\n".join(res)


class UnsupportedMerge(Exception):
    """
    Exception, falls Sequenzen beim Mergen nicht zusammenpassen  
    """
    pass


class NoLastSequence(Exception):
    """
    Exception, falls keine Sequenz am Stack vorhanden
    """
    pass


class UnsupportedSplit(Exception):
    def __init__(self, full_split):
        # full_split steht fuer einen split an index 0
        self.full_split = full_split


class SpiderSolitaireError(Exception):
    """
    Die Basisklasse fuer unsere (Status-) Exceptions
    """
    pass


class DealError(SpiderSolitaireError):
    def __init__(self, empty_stacks):
        self.empty_stacks = empty_stacks
