# --- CMake Project Configuration ---
# This CMakeLists.txt file is designed to build the pbkdf2_cli executable.
# It's integrated with Conan for dependency management and specifies build settings.

cmake_minimum_required(VERSION 3.15) # Minimum CMake version supported by Conan's CMakeToolchain.
project(pbkdf2_cli LANGUAGES CXX) # Define project name and language.

# --- C++ Standard and Extensions ---
# Explicitly set C++ standard to C++17, as required.
# CMAKE_CXX_STANDARD_REQUIRED ON: Enforces all compilers must support C++17.
# CMAKE_CXX_EXTENSIONS OFF: Disables compiler-specific extensions for strict standard adherence.
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# --- Conan Integration ---
# Conan assumes a modern CMake layout when using CMakeToolchain.
# This line is usually not needed when using Conan's cmake_layout,
# but can be included for clarity or older Conan versions.
# include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake) # For older Conan versions
# conan_basic_setup() # For older Conan versions

# --- Package Discovery ---
# Find required dependencies: Boost and OpenSSL, using their exact versions configured by Conan.
# CONFIG mode allows CMake to find packages using generated config files (e.g., BoostConfig.cmake).
# REQUIRED: CMake will stop the build if these packages are not found.
find_package(Boost 1.82.0 CONFIG REQUIRED)
find_package(OpenSSL 3.1.2 CONFIG REQUIRED) # Assuming OpenSSL package provides config files.

# --- Source Files ---
# List the source files for the executable.
set(PBKDF2_CLI_SOURCES
    args_parser.cxx
    main.cxx
)

# --- Executable Target ---
# Define the executable target.
# Use add_executable to create the executable.
add_executable(pbkdf2_cli ${PBKDF2_CLI_SOURCES})

# --- Link Libraries ---
# Link the executable against the found dependencies.
# Conan's CMakeDeps generator creates targets for dependencies (e.g., Boost::boost, OpenSSL::SSL, OpenSSL::Crypto).
target_link_libraries(pbkdf2_cli PRIVATE
    Boost::headers # For Boost headers (often implicitly handled by linking Boost::boost)
    Boost::system  # For Boost.System, commonly used.
    # Boost::program_options # If cmd line parsing was in Boost, but here it's custom.

    OpenSSL::SSL     # Link against OpenSSL's SSL library
    OpenSSL::Crypto  # Link against OpenSSL's main crypto library
)

# --- Installation Rules ---
# Define how the executable should be installed.
# This uses CMake's install command to copy the executable to a standard location
# within the package directory when 'cmake --install' is run during packaging.
# Typically installs to <prefix>/bin for executables.
install(TARGETS pbkdf2_cli DESTINATION bin)

# --- Include Directories ---
# Add directories for header files if they are not automatically handled by find_package.
# For this setup, Boost and OpenSSL headers are usually handled by target_link_libraries.
# If args_parser.hpp were in a different folder, you'd add it here:
# target_include_directories(pbkdf2_cli PRIVATE ${CMAKE_CURRENT_SOURCE_DIR})

# --- Compiler Flags ---
# Add any specific compiler flags if necessary.
# Example:
# target_compile_options(pbkdf2_cli PRIVATE -Wall -Wextra)
