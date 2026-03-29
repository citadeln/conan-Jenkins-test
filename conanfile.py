import os
from conan import ConanFile
from conan.tools.cmake import CMake, CMakeToolchain, cmake_layout
from conan.tools.files import copy, get
from conan.tools.build import build_sln

# --- Conan Profile Configuration ---
# This file describes how to build the pbkdf2_cli Conan package.
# It leverages CMake for the build system and specifies exact versions
# for external dependencies (Boost and OpenSSL).

class Pbkdf2CliConan(ConanFile):
    name = "pbkdf2_cli"
    version = "1.0.0" # Placeholder version for the CLI tool itself.

    # --- Package Metadata ---
    license = "<your_license>" # TODO: Specify the actual license.
    author = "<your_name> <your_email>" # TODO: Specify your contact details.
    url = "<repository_url>" # TODO: Specify the project repository URL.
    description = "A command-line tool for generating PBKDF2 password hashes."
    topics = ("cryptography", "hashing", "cli", "pbkdf2")

    # --- Build Settings ---
    # Specify required settings for building the package.
    settings = "os", "compiler", "build_type", "arch"

    # --- Dependencies ---
    # Specify direct dependencies with exact versions.
    # If these are not found in the cache, Conan will attempt to build them.
    requires = [
        "boost/1.82.0",
        "openssl/3.1.2@_@_" # Using generic openssl/3.1.2, assumes it's available or will be built.
        # If a specific channel/user is required for openssl, specify it here.
        # Example: "openssl/3.1.2@conan/stable"
    ]

    # --- Options ---
    # Define package options. Shared binary is typically not desired for CLI tools.
    options = {
        "shared": [True, False],
        "fPIC": [True, False]
    }
    default_options = {
        "shared": False,
        "fPIC": True # Enable FPIC by default for shared libraries on POSIX systems.
    }

    # --- Source Handling ---
    # For this example, assuming source code is available locally.
    # If it were a separate component, you might use .get() or .export_sources()
    exports_sources = "CMakeLists.txt", "args_parser.hpp", "args_parser.cxx", "main.cxx"

    def config_options(self):
        # Disable fPIC option on Windows as it's not applicable.
        if self.settings.os == "Windows":
            del self.options.fPIC

    def layout(self):
        # Use a standard CMake layout for the build directory.
        # This simplifies management of build artifacts.
        cmake_layout(self)

    def generate(self):
        # --- Toolchain Generation ---
        # CMakeToolchain automatically generates a toolchain file that
        # configures CMake with Conan's build settings and dependencies.
        tc = CMakeToolchain(self)
        tc.variables["CMAKE_CXX_STANDARD"] = "17"
        tc.variables["CMAKE_CXX_STANDARD_REQUIRED"] = "ON"
        tc.variables["CMAKE_CXX_EXTENSIONS"] = "OFF"

        # Define compiler flags explicitly if needed for specific compilers.
        # Example for GCC/Clang (can be added to tc.generate()):
        # if self.settings.compiler == "gcc" or self.settings.compiler == "clang":
        #     tc.preprocessor_definitions["_GLIBCXX_USE_CXX11_ABI"] = "0" # Example: disable C++11 ABI

        tc.generate()

    def build(self):
        # --- Build Process ---
        # Initialize and configure CMake.
        cmake = CMake(self)
        cmake.configure() # Dependencies and settings are automatically picked up.
        cmake.build()     # Build the project using the configured CMake generator.

    def package(self):
        # --- Packaging ---
        # Copy the build artifacts (executables, libraries) to the package directory.
        # For a CLI tool, we typically copy the executable.
        cmake = CMake(self)
        cmake.install() # This command typically installs artifacts based on CMake's install rules.

        # If CMake install doesn't cover it, manual copying can be done:
        # copy(self, "pbkdf2_cli*", os.path.join(self.build_folder, "bin"), os.path.join(self.package_folder, "bin"))

        # Copy license and README if they exist and are relevant for the package.
        # copy(self, "LICENSE", self.source_folder, os.path.join(self.package_folder, "licenses"))
        # copy(self, "README.md", self.source_folder, os.path.join(self.package_folder, "readme"))

    def package_info(self):
        # --- Package Information ---
        # Define information about the built package, like executables, libraries, etc.
        # This helps consumers of the package link against it or find executables.
        self.cpp_info.libs = [] # No libraries to link for a CLI tool.
        # Find the executable path relative to the package folder.
        # This is useful if the consumer needs to run the CLI tool directly.
        self.cpp_info.bindirs = ["bin"]

        # Ensure that the generated CMake config files from CMakeDeps (if any) are found.
        # For a simple CLI tool, this is often not strictly necessary, but good practice.
        # self.cpp_info.builddirs = ["lib/cmake/pbkdf2_cli"] # Example if it were a library.
