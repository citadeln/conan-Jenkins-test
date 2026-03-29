cmake_minimum_required(VERSION 3.20)
project(pbkdf2_cli LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

find_package(Boost REQUIRED COMPONENTS program_options)
find_package(OpenSSL REQUIRED)

add_executable(pbkdf2 main.cxx args_parser.cxx)

target_link_libraries(pbkdf2 PRIVATE 
    Boost::program_options 
    OpenSSL::SSL 
    OpenSSL::Crypto
)

target_compile_definitions(pbkdf2 PRIVATE BOOST_JSON_STANDALONE=1)
