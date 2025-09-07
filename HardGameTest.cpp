//
// Created by Marcel Auer on 04.03.2025.
//

#include <catch2/catch_all.hpp>
#include <stdexcept>
#include "Checker.h"
#include "HardGame.h"
#include "Wordle.h"
#include <algorithm>

/**
 * @brief Fixture for setting up the HardGame test environment.
 *
 * This struct initializes the necessary components for testing the HardGame
 * class, including a Wordle instance, a Checker instance, and the HardGame
 * instance itself.
 */
struct HardGameFixture {
  /**
   * @brief Constructor for HardGameFixture.
   *
   * Initializes the Wordle and Checker instances and creates a HardGame
   * instance with a fixed seed for reproducibility.
   */
  HardGameFixture() {
    wordle =
        std::make_unique<Wordle>(12345);  ///< Fixed seed for reproducibility.
    solution = wordle->solution;  ///< Store the solution for testing.
    valid_guesses = wordle->wordle_valid_guesses;  ///< Store valid guesses.
    checker = std::make_unique<Checker>();
    game = std::make_unique<HardGame>(6, std::move(checker), std::move(wordle));
  }

  std::unique_ptr<Wordle> wordle;    ///< Pointer to the Wordle instance.
  std::unique_ptr<Checker> checker;  ///< Pointer to the Checker instance.
  std::unique_ptr<HardGame> game;    ///< Pointer to the EasyGame instance.
  std::string solution;              ///< The solution word for the game.
  std::unordered_set<std::string> valid_guesses;
};

/**
 * @brief Test case for entering a valid word in HardGame.
 *
 * Ensures that no exception is thrown when a valid word is entered.
 */
TEST_CASE_METHOD(HardGameFixture, "HardGame_EnterValidWord") {
  const std::string validWord = "apply";
  REQUIRE_NOTHROW(game->enterWord(validWord));
}

/**
 * @brief Test case for entering a word with invalid length in HardGame.
 *
 * Ensures that a NotAFiveLetterWordException is thrown when a word with
 * fewer or more than 5 letters is entered.
 */
TEST_CASE_METHOD(HardGameFixture, "HardGame_EnterWordWithInvalidLength") {
  const std::string invalidWord = "app";
  REQUIRE_THROWS_AS(game->enterWord(invalidWord), NotAFiveLetterWordException);
}

/**
 * @brief Test case for exceeding the guess limit in HardGame.
 *
 * Ensures that a GuessLimitReachedException is thrown when the player
 * attempts to enter a word after reaching the maximum number of guesses.
 */
TEST_CASE_METHOD(HardGameFixture, "HardGame_EnterWordExceedingGuessLimit") {
  for (int i = 0; i < 6; ++i) {
    game->enterWord("apple");
  }
  REQUIRE_THROWS_AS(game->enterWord("apple"), GuessLimitReachedException);
}

/**
 * @brief Test case for entering a word not in the valid guesses list in
 * HardGame.
 *
 * Ensures that a NotAValidWordException is thrown when a word not in the
 * valid guesses list is entered.
 */
TEST_CASE_METHOD(HardGameFixture, "HardGame_EnterWordNotInValidGuesses") {
  const std::string invalidWord = "zzzzz";
  REQUIRE_THROWS_AS(game->enterWord(invalidWord), NotAValidWordException);
}

/**
 * @brief Test case for entering the correct word in HardGame.
 *
 * Ensures that the result array indicates all letters are correct and
 * that the game is marked as won.
 */
TEST_CASE_METHOD(HardGameFixture, "HardGame_EnterWordWithCorrectGuess") {
  const std::string correctWord = solution;
  const std::array<int, 5> result = game->enterWord(correctWord);
  for (int i = 0; i < 5; ++i) {
    REQUIRE(result[i] == 2);
  }
  REQUIRE(game->won());
}

/**
 * @brief Test case for entering a word without reusing a correct letter in
 * HardGame.
 *
 * Ensures that a GreenLetterNotReusedException is thrown when a word is
 * entered that does not reuse a letter marked as correct in a previous guess.
 */
TEST_CASE_METHOD(HardGameFixture,
                 "HardGame_EnterWordWithoutReusingGreenLetter") {
  // Find a word that has exactly one letter in the correct position
  std::string firstWord;
  int greenIndex = -1;
  for (const auto& word : valid_guesses) {
    int greenCount = 0;
    int idx = -1;
    for (int i = 0; i < 5; ++i) {
      if (word[i] == solution[i]) {
        ++greenCount;
        idx = i;
      }
    }
    if (greenCount == 1) {
      firstWord = word;
      greenIndex = idx;
      break;
    }
  }
  REQUIRE_FALSE(firstWord.empty());

  game->enterWord(firstWord);

  // Find a second word that does not reuse the green letter
  std::string secondWord;
  char greenChar = firstWord[greenIndex];
  for (const auto& word : valid_guesses) {
    if (word.find(greenChar) == std::string::npos) {
      secondWord = word;
      break;
    }
  }
  REQUIRE_FALSE(secondWord.empty());

  REQUIRE_THROWS_AS(game->enterWord(secondWord), GreenLetterNotReusedException);
}

/**
 * @brief Test case for entering a word without reusing a yellow letter in
 * HardGame.
 *
 * Ensures that a YellowLetterNotReusedException is thrown when a word is
 * entered that does not reuse a letter marked as present but in the wrong
 * position in a previous guess.
 */
TEST_CASE_METHOD(HardGameFixture,
                 "HardGame_EnterWordWithoutReusingYellowLetter") {
        // Find a word that has exactly one letter in the wrong position
  std::string firstWord;
  int yellowIndex = -1;
  char yellowChar = '\0';
  for (const auto& word : valid_guesses) {
    int yellowCount = 0;
    int idx = -1;
    for (int i = 0; i < 5; ++i) {
      if (word[i] != solution[i] && solution.find(word[i]) != std::string::npos) {
        ++yellowCount;
        idx = i;
        yellowChar = word[i];
      }
    }
    if (yellowCount == 1) {
      firstWord = word;
      yellowIndex = idx;
      break;
    }
  }
  REQUIRE_FALSE(firstWord.empty());

  game->enterWord(firstWord);

  // Find a second word that does not reuse the yellow letter
  std::string secondWord;
  for (const auto& word : valid_guesses) {
    if (word.find(yellowChar) == std::string::npos) {
      secondWord = word;
      break;
    }
  }
  REQUIRE_FALSE(secondWord.empty());

  REQUIRE_THROWS_AS(game->enterWord(secondWord), YellowLetterNotReusedException);
}

/**
 * @brief Tests that entering a word with non-letter characters throws a WordContainsNonLetterException.
 */
TEST_CASE_METHOD(HardGameFixture, "HardGame_EnterWordWithNonLetterCharacters") {
  REQUIRE_THROWS_AS(game->enterWord("appl3"), WordContainsNonLetterException);
  REQUIRE_THROWS_AS(game->enterWord("appl!"), WordContainsNonLetterException);
  REQUIRE_THROWS_AS(game->enterWord("appl "), WordContainsNonLetterException);
}

/**
 * @brief Tests case-insensitivity in HardGame.
 *
 * Ensures that uppercase and lowercase letters are treated equally.
 */
TEST_CASE_METHOD(HardGameFixture, "HardGame_EnterWordCaseInsensitive") {
  std::string upperCaseWord = solution;
  std::transform(upperCaseWord.begin(), upperCaseWord.end(), upperCaseWord.begin(), ::toupper);
  const std::array<int, 5> result = game->enterWord(upperCaseWord);
  for (int i = 0; i < 5; ++i) {
    REQUIRE(result[i] == 2);
  }
  REQUIRE(game->won());
}

/**
 * @brief Tests that after using all guesses without the correct word, the game is not won.
 */
TEST_CASE_METHOD(HardGameFixture, "HardGame_UseAllGuessesWithoutWinning") {
  for (int i = 0; i < 6; ++i) {
    game->enterWord("apple");
  }
  REQUIRE_FALSE(game->won());
  REQUIRE_THROWS_AS(game->enterWord("apple"), GuessLimitReachedException);
}
