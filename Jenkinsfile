pipeline {
  agent {
    node {
      label 'base'
    }

  }
  stages {
    stage('拉取代码') {
      steps {
        git(url: 'ssh://git@git.antiy.org.cn:10022/blank135/cd-abnormal-abnormal.git', credentialsId: 'gitlab-ssh', changelog: true, poll: false, branch: '${Branch}')
      }
    }
    stage('构建镜像') {
      steps {
        container('base') {
          sh 'echo "10.255.175.136 harbor.antiy.cn" >> /etc/hosts'
          withCredentials([usernamePassword(credentialsId : 'harbor' ,passwordVariable : 'password' ,usernameVariable : 'username' ,)]) {
            sh 'docker login -u ${username} -p ${password} harbor.antiy.cn'
          }

        }

      }
    }
  }
}
