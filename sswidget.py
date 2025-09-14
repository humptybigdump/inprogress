import os

from PyQt5 import QtCore
from PyQt5.Qt import Qt
from PyQt5.QtGui import QPainter, QPixmap, QCursor
from PyQt5.QtWidgets import QWidget, QMessageBox

from spidersolitaire import SpiderSolitaire, SpiderSolitaireError, DealError


class SSWidget(QWidget):
    statusUpdated = QtCore.pyqtSignal(str) # define signal for status update
    dealtCards = QtCore.pyqtSignal(str) # define signal for when cards where dealt

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        
        # Karten-Parameter (zum Zeichnen und Positionsberechnung)
        self._card_width = 90
        self._card_spacing = 8
        self._card_padding_v = 30

        # Setze feste Breite und minimale Höhe des Widgets
        self.setFixedWidth(self._card_spacing + 10 * (self._card_width + self._card_spacing))
        self.setMinimumHeight(700)

        # Bilder laden
        faceDownImage = QPixmap(os.path.join("res", "cards", "gray_back.png"))
        self._cardImageMap = { "face_down": faceDownImage.scaledToWidth(self._card_width, Qt.SmoothTransformation) }

        value_lookup = ["A"] + list(map(str, range(2, 11))) + ["J", "Q", "K"]
        for card in SpiderSolitaire.ALL_CARDS:
            fileName = value_lookup[card.get_value()-1] + ("S" if card.get_suit() == "spades" else "H")
            image = QPixmap(os.path.join("res", "cards", fileName))
            self._cardImageMap[card] = image.scaledToWidth(self._card_width, Qt.SmoothTransformation)

        # Weiterer Karten-Parameter (zum Zeichnen und Positionsberechnung)
        self._card_height = self._cardImageMap['face_down'].height()

        self._logic = SpiderSolitaire()
        
        # not needed, since we only want updates when the left mouse button is pressed anyways
        #self.setMouseTracking(True)

    def deal(self):
        """
        Slot für den Klick auf den "Deal"-Button.
        Falls zulässig und möglich wird auf jeden Stapel eine neue Karte ausgeteilt.
        """
        print("deal")
        # TODO: Hier kommt Ihr Code
    
    def reset(self):
        """
        Slot für den Klick auf den "New Game"-Button.
        Startet das Spiel neu und setzt die Labels zurück.
        """
        print("reset")
        # TODO: Hier kommt Ihr Code
    
    def posToIndices(self, pos):
        """
        Liefert den Stapel- und Kartenindex für die übergebene (Maus-)Position.
        Wenn 'pos' zu keiner Karte/keinem Stapel gehört oder diese nicht bewegt werden kann,
        ist der zugehörige Rückgabewert 'None'.
        """
        x_adjusted = pos.x() - self._card_spacing // 2
        stack_index = min(max(x_adjusted // (self._card_width + self._card_spacing), 0), 9)
        stack = self._logic.get_stack(stack_index)
        # y coordinates for face-down cards [10-value]
        ystart_last_seq = self._card_spacing + stack.num_facedown_cards * self._card_padding_v
        # visible cards up to the last sequence
        len_last_seq = 0
        # stack not empty -> there could be cards 'under' the last sequence
        if not stack.is_empty():
            len_last_seq = len(list(stack.last_sequence()))
            ystart_last_seq += (len(list(stack.iter_faceup_cards())) - len_last_seq) * self._card_padding_v

        height_last_seq = (len_last_seq - 1) * self._card_padding_v + self._card_height
        # mouse was clicked too high or low
        if not (ystart_last_seq <= pos.y() <= ystart_last_seq + height_last_seq):
            return None, None

        if len_last_seq == 0:
            return stack_index, None
        else:
            return stack_index, min((pos.y() - ystart_last_seq) // self._card_padding_v, len_last_seq-1)
    
    def mousePressEvent(self, event):
        """
        Event zum verarbeiten eines Maus-Presses. Hier wird das Aufheben einer (Teil-)Sequenz realisiert.
        """
        print("Mouse Press") # Das können Sie entfernen

        # uns interessieren nur Linksklicks
        if event.button() == Qt.LeftButton:
            # Maus global "fangen", damit alle mouseEvents in diesem Widget ankommen
            self.grabMouse()
            
            # TODO: Hier kommt Ihr Code

    def mouseMoveEvent(self, event):
        """
        Event zum verarbeiten einer Mausbewegung.
        """
        print("mouse move") # Das können Sie entfernen

        # TODO: Hier kommt Ihr Code
    
    def mouseReleaseEvent(self, event):
        """
        Event zum verarbeiten eines Maus-Releases. Hier wird das Ablegen der 'moving_sequenz' realisiert.
        """
        print("Mouse Release") # Das können Sie entfernen

        # uns interessieren nur Linksklicks
        if event.button() == Qt.LeftButton:
            # Maus wieder freigeben
            self.releaseMouse()
            
            # keine moving sequence -> nichts zu tun
            if self._logic.moving_sequence is not None:
                print("moving sequence") # Das können Sie entfernen (nur zum debuggen)
                
                # TODO: hier kommt Ihr Code

    def paintEvent(self, event):
        """
        Event zum Zeichnen des Widgets. Hier werden das Spielfeld und die Karten gezeichnet.
        """
        painter = QPainter(self)
        
        # draw background
        painter.setPen(Qt.NoPen)
        painter.setBrush(Qt.darkGreen)
        painter.drawRect(event.rect())
        
        # draw the cards on each stack
        x = self._card_spacing
        for stack in self._logic.iter_stacks():
            y = self._card_spacing
            # face-down cards
            for _ in range(stack.num_facedown_cards):
                painter.drawPixmap(x, y, self._cardImageMap["face_down"])
                y += self._card_padding_v

            # visible cards
            for card in stack.iter_faceup_cards():
                painter.drawPixmap(x, y, self._cardImageMap[card])
                y += self._card_padding_v
            
            x += self._card_width + self._card_spacing
        
        # draw moving sequence under the mouse
        if self._logic.moving_sequence is not None:
            mousePos = self.mapFromGlobal(QCursor.pos())
            y = 0
            for card in self._logic.moving_sequence:
                painter.drawPixmap(mousePos.x() - self._card_width // 2, mousePos.y() - 15 + y, self._cardImageMap[card])
                y += self._card_padding_v
