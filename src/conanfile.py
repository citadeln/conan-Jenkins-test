#!/usr/bin/env python3
from conan import ConanFile
from conan.tools.cmake import CMake, cmake_layout, CMakeToolchain, CMakeDeps

class Pbkdf2CliConan(ConanFile):
    name = "pbkdf2_cli"
    version = "1.0.0"
    
    settings = "os", "compiler", "build_type", "arch"
    requires = "boost/1.82.0", "openssl/3.1.2"
    
    exports_sources = "CMakeLists.txt", "main.cxx", "args_parser.cxx", "args_parser.hpp"
    
    def layout(self):
        cmake_layout(self)
    
    def generate(self):
        tc = CMakeToolchain(self)
        tc.variables["CMAKE_CXX_STANDARD"] = "17"
        tc.variables["CMAKE_CXX_STANDARD_REQUIRED"] = "ON"
        tc.variables["CMAKE_CXX_EXTENSIONS"] = "OFF"
        tc.variables["BOOST_JSON_STANDALONE"] = "1"
        tc.generate()
        
        deps = CMakeDeps(self)
        deps.generate()
    
    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()
    
    def package(self):
        cmake = CMake(self)
        cmake.install()
    
    def package_info(self):
        self.cpp_info.bindirs = ["bin"]
        