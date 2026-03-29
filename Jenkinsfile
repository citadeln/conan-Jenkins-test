// --- Jenkins Pipeline Definition ---
// Defines the Continuous Integration and Continuous Deployment pipeline for pbkdf2_cli.
// This pipeline orchestrates Conan packaging and the creation of a local Conan repository.
// Assumes Jenkins agent has Docker DIND (Docker-in-Docker) capabilities enabled and 'conan' client installed.

pipeline {
    agent {
        // Use a Docker agent for a consistent and isolated build environment.
        // The 'docker.image' should contain the necessary build tools (GCC, CMake, Conan).
        // 'args "-u root -v /var/run/docker.sock:/var/run/docker.sock"' enables Docker DIND to create/manage containers.
        // The '/usr/bin/conan' should be mapped if it's not in the Docker image's PATH.
        // Example using a hypothetical image with GCC 13 and CMake, and having Conan installed:
        docker {
            image 'myregistry/conan-builder:gcc-13-cmake' // TODO: Replace with actual Docker image name
            args '-u root -v /var/run/docker.sock:/var/run/docker.sock -v $HOME/.conan:/root/.conan'
            reuseNode true // Re-use the node if possible to speed up subsequent builds.
        }
    }

    options {
        // Keep a limited number of logs to save disk space.
        buildDiscarder(logRotator(numToKeepStr: '10'))
        // Disable concurrent builds for this job.
        disableConcurrentBuilds()
    }

    environment {
        // Define environment variables for the build.
        // Ensure this matches the expected layout and conventions.
        // Conan settings might be overridden here if not correctly detected by Conan.
        CONAN_USER_HOME = "/root/.conan" // Standard location for Conan cache within Docker container.
        BUILD_TYPE = "Release" // Default build type. Can be parameterized if needed.
        // Example OS/Arch to build for (can be parameterized based on agent or pipeline input)
        TARGET_ARCH = "x86_64"
        TARGET_OS = "Linux" // Assuming Linux agent environment. Adjust if cross-compiling.

        // --- Local Conan Repository Configuration ---
        // Name for the local repository that will be created/used.
        LOCAL_REPO_NAME = "local_ci_repo"
        // Path in workspace where the local repo will be hosted (relative from workspace root).
        LOCAL_REPO_PATH = "conan_repo"
    }

    stages {
        // --- Stage 1: Prepare Environment ---
        stage('Prepare Environment') {
            steps {
                echo "Starting preparation for ${env.JOB_NAME} build #${env.BUILD_NUMBER}"
                script {
                    // Ensure Conan user home is accessible.
                    sh "mkdir -p \$CONAN_USER_HOME"
                    // Create the local Conan repository directory.
                    sh "mkdir -p ${env.LOCAL_REPO_PATH}"

                    // Add the local repository to Conan remotes.
                    // --force is used in case the repo already exists from a previous run on the same node.
                    // `--system` flag implies it's just a folder, not a remote server.
                    try {
                        sh "conan remote add --force ${env.LOCAL_REPO_NAME} ${env.WORKSPACE}/${env.LOCAL_REPO_PATH}"
                        echo "Local Conan repository '${env.LOCAL_REPO_NAME}' added at ${env.WORKSPACE}/${env.LOCAL_REPO_PATH}"
                    } catch (err) {
                        echo "Warning: Could not add local Conan repository '${env.LOCAL_REPO_NAME}'. It might already exist or be configured differently. Error: ${err}"
                        // It's possible the repo is already added; if so, we can proceed.
                        // If it fails for other reasons, the build should likely fail.
                    }
                }
            }
        }

        // --- Stage 2: Configure and Build Package ---
        stage('Build Conan Package (Release x86_64)') {
            steps {
                echo "Configuring and building Conan package for ${env.JOB_NAME}..."
                script {
                    // Construct the conan install command.
                    // Dependencies (Boost, OpenSSL) will be built by Conan if not found in cache.
                    // The specific architectures and OS are implicitly handled by the agent and environment settings.
                    // '--build=missing' ensures that if a dependency is not found pre-compiled, Conan will attempt to build it.
                    sh """
                        conan install . \
                        --install-folder=build \
                        --build=missing \
                        -s arch=${env.TARGET_ARCH} \
                        -s os=${env.TARGET_OS} \
                        -s compiler.cppstd=17 \
                        -s compiler.libcxx=libstdc++11 \
                        -c tools.native_pkg_management.apt:disabled=True \
                        -c tools.native_pkg_management.yum:disabled=True \
                        --output-folder=${env.WORKSPACE}/build \
                        -o *:fPIC=${env.options_fPIC_default} # Use default fPIC from conanfile.py
                        -o *:shared=False
                    """
                    // The actual build and install happens via CMake during the 'conan install' process
                    // when a CMakeToolchain is used and the source folder is specified.
                    // If you have a separate build step after 'conan install', you might need it:
                    // cmake --build build --config ${env.BUILD_TYPE} --target install
                }
            }
        }

        // --- Stage 3: Upload Package to Local Repository ---
        stage('Upload Package') {
            steps {
                echo "Uploading Conan package to local repository '${env.LOCAL_REPO_NAME}'..."
                script {
                    // Upload the newly created package.
                    sh """
                         conan upload ${env.name}/${env.version} \
                         --all \
                         --remote=${env.LOCAL_REPO_NAME} \
                         --confirm \
                         --build=missing
                    """
                    echo "Package ${env.name}/${env.version} uploaded to ${env.LOCAL_REPO_NAME}."
                }
            }
        }
    }

    post {
        // --- Post-build Actions ---
        always {
            echo "Pipeline finished."
            // Clean up local Conan repository or other temporary artifacts if necessary.
            // Example: Delete the local repo folder if it's only for this build node.
            // sh "rm -rf ${env.LOCAL_REPO_PATH}"
            // Archive build artifacts if needed (e.g., logs, generated files outside of Conan packaging)
            // archiveArtifacts artifacts: 'build/**/*', allowEmptyArchive: true
        }
        success {
            echo "Pipeline succeeded!"
        }
        failure {
            echo "Pipeline failed!"
            // Trigger notifications or other actions on failure.
        }
    }
}
