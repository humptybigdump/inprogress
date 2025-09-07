#include <iostream>

int main() {
    bool playing = true;
    int player = 1;
    int field = 0;
    char token = 'X';
    char first = '1';
    char second = '2';
    char third = '3';
    char fourth = '4';
    char fifth = '5';
    char sixth = '6';
    char seventh = '7';
    char eight = '8';
    char ninth = '9';
    while (playing)
    {
        // visualize game board
        std::cout << "    |    |    \n";
        std::cout << "  " << first <<" |  " << second <<" |  " << third <<"  \n";
        std::cout << "____|____|____\n";
        std::cout << "    |    |    \n";
        std::cout << "  " << fourth <<" |  " << fifth <<" |  " << sixth <<"  \n";
        std::cout << "____|____|____\n";
        std::cout << "    |    |    \n";
        std::cout << "  " << seventh <<" |  " << eight <<" |  " << ninth <<"  \n";
        std::cout << "    |    |    \n";

        // ask player for input and switch player
        std::cout << "Player " << player << " please choose a field: ";
        std::cin >> field;
        if (player == 1) {
            token = 'X';
            player = 2;
        } else {
            token = 'O';
            player = 1;
        }

        // modify game board according to input and win conditions
        switch (field)
        {
            case 1:
                first = token;
                // win condition with checks limited to include position 1
                if (second == token && third == token || fourth == token && seventh == token || fifth == token && ninth == token) {
                    playing = false;
                }
                break;
            case 2:
                if (first == token && third == token || fifth == token && eight == token) {
                    playing = false;
                }
                second = token;
                break;
            case 3:
                if (first == token && second == token || sixth == token && ninth == token || fifth == token && seventh == token) {
                    playing = false;
                }
                third = token;
                break;
            case 4:
                // TODO win condition
                fourth = token;
                break;
            case 5:
                // TODO win condition
                fifth = token;
                break;
            case 6:
                // TODO win condition
                sixth = token;
                break;
            case 7:
                // TODO win condition
                seventh = token;
                break;
            case 8:
                // TODO win condition
                eight = token;
                break;
            case 9:
                // TODO win condition
                ninth = token;
                break;
            default:
                if (player == 1) {
                    player = 2;
                } else {
                    player = 1;
                }
        }
    }
    return 0;
}