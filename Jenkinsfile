pipeline {
    agent { dockerfile true }
    stages {
        step([$class: 'DockerComposeBuilder', dockerComposeFile: 'docker-compose.dev.yml', option: [$class: 'StartAllServices'], useCustomDockerComposeFile: true])
    }
}