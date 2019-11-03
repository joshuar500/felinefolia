pipeline {
    agent { dockerfile true }
    stages {
        stage('Build') {
            steps {
                step([$class: 'DockerComposeBuilder', dockerComposeFile: 'docker-compose.ci.yml', option: [$class: 'StartAllServices'], useCustomDockerComposeFile: true])
            }
        }
    }
}