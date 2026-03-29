cd ~/projects/conan-Jenkins-test/src

# 1. Замени файл (nano conanfile.py или cat > conanfile.py)
# 2. Очисти
rm -rf build
mkdir build && cd build

# 3. Установи зависимости
conan install .. --build=boost -s build_type=Release

# 4. Собери
cmake .. -DCMAKE_TOOLCHAIN_FILE=Release/generators/conan_toolchain.cmake -DCMAKE_BUILD_TYPE=Release

# Сборка
cmake --build . --parallel

# Тест
./bin/pbkdf2 --help

# 5. Запусти новый контейнер Jenkins
docker stop jenkins
docker rm jenkins

Запусти ПРАВИЛЬНЫЙ Jenkins (из ~/projects/conan-Jenkins-test/src)
docker run -d \
  --name jenkins \
  -p 8080:8080 -p 50000:50000 \
  -v jenkins_home:/var/jenkins_home \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v $(pwd)/../..:/workspace \
  jenkins/jenkins:lts-jdk17

# 6. Открой http://localhost:8080
В Jenkins UI:

New Item → Pipeline → OK

Pipeline → Pipeline script → вставь Jenkinsfile выше

Save → Build Now