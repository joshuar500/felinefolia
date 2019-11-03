pipeline {
    agent { dockerfile true }
    stages {
        stage('Build') {
            steps {
                step([$class: 'DockerComposeBuilder', dockerComposeFile: 'docker-compose.dev.yml', option: [$class: 'StartAllServices'], useCustomDockerComposeFile: true])
            }
        }
    }
}