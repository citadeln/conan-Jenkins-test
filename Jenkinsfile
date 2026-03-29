pipeline {
    agent {
        docker {
            image 'conanio/gcc13:latest'
            args '-u root --group-add $(id -g docker) -v /var/run/docker.sock:/var/run/docker.sock'
        }
    }

    options {
        buildDiscarder(logRotator(numToKeepStr: '10', artifactNumToKeepStr: '5'))
        disableConcurrentBuilds()
        timeout(time: 30, unit: 'MINUTES')
        timestamps()
    }

    environment {
        CONAN_USER_HOME = "${WORKSPACE}/.conan"
        CONAN_PROFILE = "default"
        CONAN_GENERATORS = "cmake_find_package_multi"
    }

    stages {
        stage('Validate') {
            parallel {
                stage('Files') {
                    steps {
                        sh '''
                            [[ -f CMakeLists.txt ]] || { echo "CMakeLists.txt missing"; exit 1; }
                            [[ -f conanfile.py ]] || { echo "conanfile.py missing"; exit 1; }
                            conan inspect . --raw | jq -r '.name, .version'
                        '''
                    }
                }
                stage('Profile') {
                    steps {
                        sh 'conan profile detect --force && conan profile show default'
                    }
                }
            }
        }

        stage('Conan Install') {
            steps {
                sh '''
                    mkdir -p build && cd build
                    conan install .. \
                        --build=missing \
                        -s build_type=Release \
                        -pr=default \
                        -of=. \
                        --generator-set cmake_find_package_multi
                '''
            }
        }

        stage('Build & Test') {
            parallel {
                stage('Build') {
                    steps {
                        dir('build') {
                            sh '''
                                cmake .. -DCMAKE_BUILD_TYPE=Release -DCMAKE_TOOLCHAIN_FILE=conan_toolchain.cmake
                                cmake --build . --parallel $(nproc)
                            '''
                        }
                    }
                }
                stage('Test') {
                    steps {
                        dir('build') {
                            sh './pbkdf2 --help && ./pbkdf2 --password test123 --iter 10'
                        }
                    }
                }
            }
        }

        stage('Package') {
            when { anyOf { branch 'main'; branch 'develop' } }
            steps {
                sh '''
                    conan create . monroe/testing --build=missing -pr=default
                    mkdir -p conan_repo
                    conan upload "*"@monroe/testing --all -r local_ci_repo --confirm
                '''
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'build/**, conan_repo/**', allowEmptyArchive: true
            junit 'build/test-results.xml'
            publishHTML([
                allowMissing: false,
                alwaysLinkToLastBuild: true,
                keepAll: true,
                reportDir: 'build',
                reportFiles: 'index.html',
                reportName: 'Build Report'
            ])
        }
        success {
            slackSend channel: '#ci', message: "${env.JOB_NAME} #${env.BUILD_NUMBER} SUCCESS"
        }
        failure {
            slackSend channel: '#ci-failures', message: "${env.JOB_NAME} #${env.BUILD_NUMBER} FAILED"
        }
        cleanup {
            sh 'docker system prune -f || true'
        }
    }
}
