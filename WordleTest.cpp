// Created by Marcel Auer on 04.03.2025.

  #include <catch2/catch_all.hpp>
  #include "Wordle.h"

  // =============================
  // --- Solution Words Tests ---
  // =============================

  /**
   * @brief Checks that the solution word list is loaded with the correct number of entries.
   */
  TEST_CASE("Wordle_SolutionWords_LoadedCorrectly")
  {
    auto wordle = std::make_unique<Wordle>(12345);
    REQUIRE(wordle->wordle_solution_words.size() == 2315);
  }

  /**
   * @brief Ensures all solution words have exactly five letters.
   */
  TEST_CASE("Wordle_SolutionWords_AllAreFiveLetters")
  {
    auto wordle = std::make_unique<Wordle>(12345);
    for (const auto& word : wordle->wordle_solution_words) {
      REQUIRE(word.length() == 5);
    }
  }

  /**
   * @brief Verifies all solution words are lowercase and contain no whitespace.
   */
  TEST_CASE("Wordle_SolutionWords_AreLowercaseAndTrimmed")
  {
    auto wordle = std::make_unique<Wordle>(12345);
    for (const auto& word : wordle->wordle_solution_words) {
      REQUIRE(std::all_of(word.begin(), word.end(), ::islower));
      REQUIRE(word.find_first_of(" \t\n\r\f\v") == std::string::npos);
    }
  }

  /**
   * @brief Checks that the selected solution is present in the solution word set.
   */
  TEST_CASE("Wordle_SolutionWords_SolutionIsInSet")
  {
    auto wordle = std::make_unique<Wordle>(12345);
    REQUIRE(wordle->wordle_solution_words.count(wordle->solution) > 0);
  }

  /**
   * @brief Checks that the solution contains no letters with multiple occurrences.
   */
  TEST_CASE("Wordle_SolutionWords_LettersWithMultipleOccurrences")
  {
    const auto wordle_temp = std::make_unique<Wordle>(0);
    auto it = std::find(wordle_temp->wordle_solution_words.begin(),
                        wordle_temp->wordle_solution_words.end(), "datum");
    REQUIRE(it != wordle_temp->wordle_solution_words.end());
    int index = std::distance(wordle_temp->wordle_solution_words.begin(), it);
    auto wordle = std::make_unique<Wordle>(index);
    std::cout << "Index: " << index << std::endl;
    REQUIRE(wordle->solution == "datum");
    REQUIRE(wordle->letters_with_multiple_occurrences.empty());
  }

  /**
   * @brief Checks that the solution contains letters with multiple occurrences and detects them.
   */
  TEST_CASE("Wordle_SolutionWords_LettersWithMultipleOccurrences_2")
  {
    const auto wordle_temp = std::make_unique<Wordle>(0);
    auto it = std::find(wordle_temp->wordle_solution_words.begin(),
                        wordle_temp->wordle_solution_words.end(), "catty");
    REQUIRE(it != wordle_temp->wordle_solution_words.end());
    int index = std::distance(wordle_temp->wordle_solution_words.begin(), it);
    auto wordle = std::make_unique<Wordle>(index);
    std::cout << "Index: " << index << std::endl;
    REQUIRE(wordle->solution == "catty");
    REQUIRE(wordle->letters_with_multiple_occurrences.find('t') != wordle->letters_with_multiple_occurrences.end());
    REQUIRE_FALSE(wordle->letters_with_multiple_occurrences.empty());
  }

  // =============================
  // --- Valid Guesses Tests ---
  // =============================

  /**
   * @brief Checks that the valid guesses list is loaded with the correct number of entries.
   */
  TEST_CASE("Wordle_ValidGuesses_LoadedCorrectly")
  {
    auto wordle = std::make_unique<Wordle>(12345);
    REQUIRE(wordle->wordle_valid_guesses.size() == 12972);
  }

  /**
   * @brief Ensures all valid guesses have exactly five letters.
   */
  TEST_CASE("Wordle_ValidGuesses_AllAreFiveLetters")
  {
    auto wordle = std::make_unique<Wordle>(12345);
    for (const auto& word : wordle->wordle_valid_guesses) {
      REQUIRE(word.length() == 5);
    }
  }

  /**
   * @brief Verifies all valid guesses are lowercase and contain no whitespace.
   */
  TEST_CASE("Wordle_ValidGuesses_AreLowercaseAndTrimmed")
  {
    auto wordle = std::make_unique<Wordle>(12345);
    for (const auto& word : wordle->wordle_valid_guesses) {
      REQUIRE(std::all_of(word.begin(), word.end(), ::islower));
      REQUIRE(word.find_first_of(" \t\n\r\f\v") == std::string::npos);
    }
  }

  /**
   * @brief Checks that the selected solution is present in the valid guesses set.
   */
  TEST_CASE("Wordle_ValidGuesses_SolutionIsInSet")
  {
    auto wordle = std::make_unique<Wordle>(12345);
    REQUIRE(wordle->wordle_valid_guesses.count(wordle->solution) > 0);
  }