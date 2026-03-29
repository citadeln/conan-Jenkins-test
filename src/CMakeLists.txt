# CMakeLists.txt - Конфигурация проекта для сборки CLI инструмента
# Совместим с Conan CMakeToolchain и CMakeDeps (автоматическая обработка зависимостей)

cmake_minimum_required(VERSION 3.21)
project(CLI_Tool VERSION 1.0.0 LANGUAGES CXX)

# Устанавливаем стандарт C++17 строго без расширений
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Автоматическое обнаружение зависимостей через Conan (CMakeDeps)
find_package(Boost CONFIG REQUIRED
    COMPONENTS headers system
    CONFIG_DEBUG_POSTFIX "_d")
find_package(OpenSSL CONFIG REQUIRED)

# Создаем исполняемый файл
add_executable(${PROJECT_NAME}
    src/main.cpp
    src/cli_parser.cpp
    src/crypto_handler.cpp
)

# Линкуем библиотеки через Conan псевдонимы
target_link_libraries(${PROJECT_NAME} PRIVATE
    Boost::headers
    Boost::system
    OpenSSL::SSL
    OpenSSL::Crypto
)

# Устанавливаем исполняемый файл для Conan пакета (в bin/)
install(TARGETS ${PROJECT_NAME}
        RUNTIME DESTINATION bin
        COMPONENT Runtime)

# Опционально: устанавливаем заголовочные файлы, если они нужны потребителям
# install(DIRECTORY include/ DESTINATION include)
