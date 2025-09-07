//
// Created by Marcel Auer on 04.03.2025.
//

#include <catch2/catch_all.hpp>
#include <stdexcept>
#include <algorithm>
#include "Checker.h"
#include "EasyGame.h"
#include "Wordle.h"

/**
 * @brief Fixture for setting up the EasyGame test environment.
 *
 * This struct initializes the necessary components for testing the EasyGame
 * class, including a Wordle instance, a Checker instance, and the EasyGame
 * instance itself.
 */
struct EasyGameFixture {
  /**
   * @brief Constructor for EasyGameFixture.
   *
   * Initializes the Wordle and Checker instances and creates an EasyGame
   * instance with a fixed seed for reproducibility.
   */
  EasyGameFixture() {
    wordle =
        std::make_unique<Wordle>(12345);  ///< Fixed seed for reproducibility.
    solution = wordle->solution;  ///< Store the solution for testing.
    valid_guesses = wordle->wordle_valid_guesses;  ///< Store valid guesses.
    checker = std::make_unique<Checker>();
    game = std::make_unique<EasyGame>(6, std::move(checker), std::move(wordle));
  }

  std::unique_ptr<Wordle> wordle;    ///< Pointer to the Wordle instance.
  std::unique_ptr<Checker> checker;  ///< Pointer to the Checker instance.
  std::unique_ptr<EasyGame> game;    ///< Pointer to the EasyGame instance.
  std::string solution;              ///< The solution word for the game.
  std::unordered_set<std::string> valid_guesses;
};

/**
 * @brief Test case for entering a valid word in EasyGame.
 *
 * Ensures that no exception is thrown when a valid word is entered.
 */
TEST_CASE_METHOD(EasyGameFixture, "EasyGame_EnterValidWord") {
  const std::string validWord = "apple";
  REQUIRE_NOTHROW(game->enterWord(validWord));
}

/**
 * @brief Test case for entering a word with invalid length in EasyGame.
 *
 * Ensures that a NotAFiveLetterWordException is thrown when a word with
 * fewer or more than 5 letters is entered.
 */
TEST_CASE_METHOD(EasyGameFixture, "EasyGame_EnterWordWithInvalidLength") {
  const std::string invalidWord = "app";
  REQUIRE_THROWS_AS(game->enterWord(invalidWord), NotAFiveLetterWordException);
}

/**
 * @brief Test case for exceeding the guess limit in EasyGame.
 *
 * Ensures that a GuessLimitReachedException is thrown when the player
 * attempts to enter a word after reaching the maximum number of guesses.
 */
TEST_CASE_METHOD(EasyGameFixture, "EasyGame_EnterWordExceedingGuessLimit") {
  for (int i = 0; i < 6; ++i) {
    game->enterWord("apple");
  }
  REQUIRE_THROWS_AS(game->enterWord("apple"), GuessLimitReachedException);
}

/**
 * @brief Test case for entering a word not in the valid guesses list in
 * EasyGame.
 *
 * Ensures that no exception is thrown when a word not in the valid guesses list
 * is entered, as EasyGame allows such guesses.
 */
TEST_CASE_METHOD(EasyGameFixture, "EasyGame_EnterWordNotInValidGuesses") {
  const std::string invalidWord = "zzzzz";
  REQUIRE_NOTHROW(game->enterWord(invalidWord));
}

/**
 * @brief Test case for entering the correct word in EasyGame.
 *
 * Ensures that the result array indicates all letters are correct and
 * that the game is marked as won.
 */
TEST_CASE_METHOD(EasyGameFixture, "EasyGame_EnterWordWithCorrectGuess") {
  const std::string correctWord = solution;
  const std::array<int, 5> result = game->enterWord(correctWord);
  for (int i = 0; i < 5; ++i) {
    REQUIRE(result[i] == 2);
  }
  REQUIRE(game->won());
}

/**
 * @brief Test case for entering a word with all wrong letters in EasyGame.
 *
 * Ensures that the result array indicates all letters are incorrect and
 * that the game is not marked as won.
 */
TEST_CASE_METHOD(EasyGameFixture, "EasyGame_EnterWordWithWrongLetters") {
  // ensure that no letter from the solution is in the wrong word
  std::string wrongWord;
  for (const auto& word : valid_guesses) {
    bool hasCommonLetter = false;
    for (char c : word) {
      if (solution.find(c) != std::string::npos) {
        hasCommonLetter = true;
        break;
      }
    }
    if (!hasCommonLetter) {
      wrongWord = word;
      break;
    }
  }
  const std::array<int, 5> result = game->enterWord(wrongWord);
  for (int i = 0; i < 5; ++i) {
    REQUIRE(result[i] == 0);
  }
  REQUIRE_FALSE(game->won());
}

/**
 * @brief Test case for entering a word with non-letter characters in EasyGame.
 *
 * Ensures that a WordContainsNonLetterException is thrown when the word contains non-letter characters.
 */
TEST_CASE_METHOD(EasyGameFixture, "EasyGame_EnterWordWithNonLetterCharacters") {
  REQUIRE_THROWS_AS(game->enterWord("appl3"), WordContainsNonLetterException);
  REQUIRE_THROWS_AS(game->enterWord("appl!"), WordContainsNonLetterException);
  REQUIRE_THROWS_AS(game->enterWord("appl "), WordContainsNonLetterException);
}

/**
 * @brief Test case for case-insensitivity in EasyGame.
 *
 * Ensures that uppercase and lowercase letters are treated equally.
 */
TEST_CASE_METHOD(EasyGameFixture, "EasyGame_EnterWordCaseInsensitive") {
  std::string upperCaseWord = solution;
  std::transform(upperCaseWord.begin(), upperCaseWord.end(), upperCaseWord.begin(), ::toupper);
  const std::array<int, 5> result = game->enterWord(upperCaseWord);
  for (int i = 0; i < 5; ++i) {
    REQUIRE(result[i] == 2);
  }
  REQUIRE(game->won());
}

/**
 * @brief Test case for not winning after using all guesses without correct word.
 *
 * Ensures that after using all guesses without the correct word, the game is not won.
 */
TEST_CASE_METHOD(EasyGameFixture, "EasyGame_UseAllGuessesWithoutWinning") {
  for (int i = 0; i < 6; ++i) {
    game->enterWord("abaft");
  }
  REQUIRE_FALSE(game->won());
  REQUIRE_THROWS_AS(game->enterWord("abaft"), GuessLimitReachedException);
}
