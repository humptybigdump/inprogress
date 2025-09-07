//
// Created by Marcel Auer on 04.03.2025.
//

#include <catch2/catch_all.hpp>
#include <stdexcept>
#include "Checker.h"
#include "NormalGame.h"
#include "Wordle.h"

/**
 * @brief Fixture for setting up a NormalGame instance for testing.
 *
 * This struct initializes the necessary components (Wordle, Checker, and
 * NormalGame) with a fixed seed for reproducibility.
 */
struct NormalGameFixture {
  /**
   * @brief Constructor for the fixture.
   *
   * Sets up a Wordle instance with a fixed seed, a Checker instance, and a
   * NormalGame instance.
   */
  NormalGameFixture() {
    wordle =
        std::make_unique<Wordle>(12345);  ///< Fixed seed for reproducibility.
    solution = wordle->solution;  ///< Store the solution for testing.
    valid_guesses = wordle->wordle_valid_guesses;  ///< Store valid guesses.
    checker = std::make_unique<Checker>();
    game = std::make_unique<NormalGame>(6, std::move(checker), std::move(wordle));
  }

  std::unique_ptr<Wordle> wordle;    ///< Pointer to the Wordle instance.
  std::unique_ptr<Checker> checker;  ///< Pointer to the Checker instance.
  std::unique_ptr<NormalGame> game;    ///< Pointer to the EasyGame instance.
  std::string solution;              ///< The solution word for the game.
  std::unordered_set<std::string> valid_guesses;
};

/**
 * @brief Tests that entering a valid word does not throw an exception.
 */
TEST_CASE_METHOD(NormalGameFixture, "NormalGame_EnterValidWord") {
  const std::string validWord = "apple";
  REQUIRE_NOTHROW(game->enterWord(validWord));
}

/**
 * @brief Tests that entering a word with an invalid length throws a
 * NotAFiveLetterWordException.
 */
TEST_CASE_METHOD(NormalGameFixture, "NormalGame_EnterWordWithInvalidLength") {
  const std::string invalidWord = "app";
  REQUIRE_THROWS_AS(game->enterWord(invalidWord), NotAFiveLetterWordException);
}

/**
 * @brief Tests that entering more words than the guess limit throws a
 * GuessLimitReachedException.
 */
TEST_CASE_METHOD(NormalGameFixture, "NormalGame_EnterWordExceedingGuessLimit") {
  for (int i = 0; i < 6; ++i) {
    game->enterWord("apple");
  }
  REQUIRE_THROWS_AS(game->enterWord("apple"), GuessLimitReachedException);
}

/**
 * @brief Tests that entering a word not in the valid guesses list throws a
 * NotAValidWordException.
 */
TEST_CASE_METHOD(NormalGameFixture, "NormalGame_EnterWordNotInValidGuesses") {
  const std::string invalidWord = "zzzzz";
  REQUIRE_THROWS_AS(game->enterWord(invalidWord), NotAValidWordException);
}

/**
 * @brief Tests that entering the correct word returns the correct result and
 * marks the game as won.
 */
TEST_CASE_METHOD(NormalGameFixture, "NormalGame_EnterWordWithCorrectGuess") {
  const std::string correctWord = solution;
  const std::array<int, 5> result = game->enterWord(correctWord);
  for (int i = 0; i < 5; ++i) {
    REQUIRE(result[i] == 2);
  }
  REQUIRE(game->won());
}

/**
 * @brief Tests that entering a word with non-letter characters throws a
 * WordContainsNonLetterException.
 */
TEST_CASE_METHOD(NormalGameFixture,
                 "NormalGame_EnterWordWithNonLetterCharacters") {
  REQUIRE_THROWS_AS(game->enterWord("appl3"), WordContainsNonLetterException);
  REQUIRE_THROWS_AS(game->enterWord("appl!"), WordContainsNonLetterException);
  REQUIRE_THROWS_AS(game->enterWord("appl "), WordContainsNonLetterException);
}

/**
 * @brief Tests case-insensitivity in NormalGame.
 *
 * Ensures that uppercase and lowercase letters are treated equally.
 */
TEST_CASE_METHOD(NormalGameFixture, "NormalGame_EnterWordCaseInsensitive") {
  std::string upperCaseWord = solution;
  std::transform(upperCaseWord.begin(), upperCaseWord.end(), upperCaseWord.begin(), ::toupper);
  const std::array<int, 5> result = game->enterWord(upperCaseWord);
  for (int i = 0; i < 5; ++i) {
    REQUIRE(result[i] == 2);
  }
  REQUIRE(game->won());
}

/**
 * @brief Tests that after using all guesses without the correct word, the game
 * is not won.
 */
TEST_CASE_METHOD(NormalGameFixture, "NormalGame_UseAllGuessesWithoutWinning") {
  for (int i = 0; i < 6; ++i) {
    game->enterWord("apple");
  }
  REQUIRE_FALSE(game->won());
  REQUIRE_THROWS_AS(game->enterWord("apple"), GuessLimitReachedException);
}
