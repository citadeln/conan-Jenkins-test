#!/usr/bin/env python
# conanfile.py - Рецепт Conan для CLI инструмента
# Содержит метаданные, настройки сборки, зависимости и логику упаковки

from conan import ConanFile
from conan.errors import ConanInvalidConfiguration
from conan.tools.build import can_run, cross_building
from conan.tools.cmake import CMake, cmake_layout, CMakeToolchain, CMakeDeps
from conan.tools.files import copy, export_conandata_patches, get, save, rmdir
from conan.tools.env import VirtualBuildEnv, VirtualRunEnv
from conan.tools.postmarketos.gcc import GccDevel
from conan.tools.postmarketos import SystemPackageTool
import os

class CLIToolConan(ConanFile):
    """Conan рецепт для CLI инструмента с зависимостями Boost и OpenSSL"""

    # === МЕТАДАННЫЕ ПАКЕТА ===
    name = "cli-tool"
    version = "1.0.0"
    package_type = "application"
    description = "CLI инструмент для криптографических операций с использованием Boost и OpenSSL"
    topics = ("cli", "openssl", "boost", "crypto")
    url = "https://github.com/your-org/cli-tool"  # ✅ ЗАПОЛНЕНО: замените на реальный репозиторий
    license = "MIT"  # ✅ ЗАПОЛНЕНО: стандартная лицензия MIT
    author = "Your Name <your.email@domain.com>"  # ✅ ЗАПОЛНЕНО: укажите ваше имя/контакт
    settings = "os", "compiler", "build_type", "arch"
    options = {
        "fPIC": [True, False],
        "shared": [True, False],
        "cppstd": ["11", "14", "17", "20", "23"]
    }
    default_options = {
        "fPIC": True,
        "shared": False,
        "cppstd": "17",
        # Зависимости тоже имеют дефолтные опции
        "boost/*:shared": False,
        "openssl/*:shared": False
    }

    # === ЗАВИСИМОСТИ ===
    requires = (
        "boost/1.85.0",  # ✅ Обновлено до стабильной версии
        "openssl/3.3.2"  # ✅ Используем стабильную версию из conan-center
    )
    # Убрали tool-requires, так как CMakeToolchain обрабатывает это автоматически

    # === ИСХОДНЫЕ ФАЙЛЫ ===
    exports_sources = "CMakeLists.txt", "src/*", "include/*", "conanfile.py"

    def config_options(self):
        """Конфигурация опций в зависимости от платформы"""
        if self.settings.os == "Macos":
            del self.options.fPIC

    def configure(self):
        """Дополнительная конфигурация опций зависимостей"""
        if self.options.shared:
            self.options.rm_safe("fPIC")

    def layout(self):
        """Структура директорий Conan (стандартная для CMake)"""
        cmake_layout(self, src_folder="src")

    def generate(self):
        """Генерация toolchain и зависимостей для CMake"""
        tc = CMakeToolchain(self)

        # Устанавливаем C++ стандарт
        tc.variables["CMAKE_CXX_STANDARD"] = self.options.cppstd
        tc.variables["CMAKE_CXX_STANDARD_REQUIRED"] = "ON"
        tc.variables["CMAKE_CXX_EXTENSIONS"] = "OFF"

        # Отключаем тестирование и примеры для ускорения сборки
        tc.cache_variables["BUILD_TESTING"] = False

        # Генерируем toolchain файл
        tc.generate()

        # Генерируем зависимости для CMake
        deps = CMakeDeps(self)
        deps.generate()

    def build(self):
        """Сборка проекта"""
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        """Упаковка артефактов"""
        # Стандартная установка через CMake
        cmake = CMake(self)
        cmake.install()

        # ✅ УДАЛЕНО: ручное копирование, cmake.install() достаточно

    def package_info(self):
        """Информация о пакете для потребителей"""
        self.cpp_info.set_property("cmake_file_name", "CLI-Tool")

        # Для application пакета libs обычно пустой
        self.cpp_info.libs = []

        # Исполняемый файл находится в bin/
        self.cpp_info.bindirs = ["bin"]
        self.cpp_info.includedirs = ["include"]

        # Запусковой файл (для Linux)
        bin_path = os.path.join(self.package_folder, "bin", f"{self.name}")
        self.runenv_info.define_path("PATH", bin_path)
