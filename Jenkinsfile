pipeline {
    agent {
        docker {
            // Используем официальный Jenkins + устанавливаем Conan
            image 'jenkins/jenkins:lts-jdk17'
            args '''
                -v /var/run/docker.sock:/var/run/docker.sock 
                -v $HOME/.conan:/root/.conan 
                --user root
            '''
            // Устанавливаем Conan и зависимости в контейнере
            runArgs '-v /var/run/docker.sock:/var/run/docker.sock'
        }
    }

    options {
        // Сохраняем только 10 последних сборок
        buildDiscarder(logRotator(numToKeepStr: '10'))
        // Отключаем параллельные сборки для этого job
        disableConcurrentBuilds()
    }

    environment {
        // ГОТОВО К ЗАПУСКУ: стандартные настройки
        CONAN_USER_HOME = "/root/.conan"
        BUILD_TYPE = "Release"
        TARGET_ARCH = "x86_64"
        TARGET_OS = "Linux"

        // Локальный Conan репозиторий для CI
        LOCAL_REPO_NAME = "local_ci_repo"
        LOCAL_REPO_PATH = "conan_repo"
    }

    stages {
        stage('Prepare Environment') {
            steps {
                echo "Подготовка окружения для сборки ${env.JOB_NAME} #${env.BUILD_NUMBER}"
                script {
                    // Создаем директории
                    sh "mkdir -p \$CONAN_USER_HOME"
                    sh "mkdir -p ${env.LOCAL_REPO_PATH}"

                    // УСТАНОВКА CONAN (для Jenkins образа)
                    sh '''
                        apt-get update && apt-get install -y wget gnupg ca-certificates python3 python3-pip build-essential cmake curl
                        pip3 install conan
                        conan --version
                    '''

                    // Добавляем локальный репозиторий
                    sh "conan remote add --force ${env.LOCAL_REPO_NAME} ${env.WORKSPACE}/${env.LOCAL_REPO_PATH}"
                    echo "Локальный репозиторий '${env.LOCAL_REPO_NAME}' готов"
                }
            }
        }

        stage('Build Conan Package (Release x86_64)') {
            steps {
                echo "Сборка Conan пакета ${env.name}/${env.version}..."
                script {
                    sh '''
                        conan install . \
                            --install-folder=build \
                            --build=missing \
                            -s arch=x86_64 \
                            -s os=Linux \
                            -s compiler.cppstd=17 \
                            -s compiler.libcxx=libstdc++11 \
                            -c tools.native_pkg_management.apt:disabled=True \
                            -o *:fPIC=True \
                            -o *:shared=False
                    '''
                }
            }
        }

        stage('Upload Package') {
            steps {
                echo "Загрузка пакета в локальный репозиторий '${env.LOCAL_REPO_NAME}'..."
                sh '''
                    conan upload cli-tool/1.0.0 \
                        --all \
                        --remote=${LOCAL_REPO_NAME} \
                        --confirm \
                        --build=missing
                '''
                echo "Пакет cli-tool/1.0.0 успешно загружен!"
            }
        }
    }

    post {
        always {
            echo "Пайплайн завершен."
        }
        success {
            echo "Сборка успешно завершена!"
        }
        failure {
            echo "Ошибка сборки!"
        }
    }
}
