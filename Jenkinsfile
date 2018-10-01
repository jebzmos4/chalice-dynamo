#!/usr/bin/env groovy

/**

Jenkinsfile for deploying build projects to AWS S3

*/
import java.util.Date
import groovy.json.JsonOutput
import groovy.json.JsonSlurper


def displayName = env.JOB_NAME
def bucketName = env.JOB_NAME
def branchName = env.BRANCH_NAME == "dev"
def start = new Date()
def err = null


String jobInfoShort = "${env.JOB_NAME} ${env.BUILD_DISPLAY_NAME}"
String jobInfo = "${env.JOB_NAME} ${env.BUILD_DISPLAY_NAME} \n${env.BUILD_URL}"
String buildStatus
String timeSpent

currentBuild.result = "SUCCESS"

try {
    node {
        def app
                
        deleteDir()
        env.PYTHON_HOME = "${tool 'python3'}"
        env.PATH = "${env.PYTHON_HOME}/bin:${env.PATH}"

        
        // Mark the code checkout 'stage'
        
        stage ('Checkout') {
            checkout scm
        }
        
        stage ('Install Dependencies') {
            sh "pip install --user  chalice && pip install --user requirements"
        }

        stage ("Deploy with Chalice"){
            sh "cp .chalice/config.json .chalice/config.json.tmp"
            sh "python /bin/envswaper/main.py path .chalice/config.json chalice staging"
            sh "rm -rf ~/.aws/config"
            sh "export AWS_DEFAULT_REGION=eu-west-1 && chalice deploy >> chalice-export.txt"
            sh "rm -rf .chalice/config.json"
            sh "mv .chalice/config.json.tmp .chalice/config.json"
            def response = sh(returnStdout: true, script: "grep -r -A2 'Resources deployed' chalice-export.txt")
            def logResponse = JsonOutput.toJson(["ref": "ref", "description": "description", "msg": "${response}", "required_contexts": []])
            slackSend (color: 'good', message: "${response}")
            sh "rm -rf chalice-export.txt"
        }
        
    }
} catch (caughtError) {
    err = caughtError
    currentBuild.result = "FAILURE"
} finally {
    
    timeSpent = "\nTime spent: ${timeDiff(start)}"

    if (err) {
        slackSend (color: 'danger', message: "_Build failed_: ${jobInfo} ${timeSpent}")
        throw err
    } else {
        if (currentBuild.previousBuild == null) {
            buildStatus = '_First time build_'
        } else if (currentBuild.previousBuild.result == 'SUCCESS') {
            buildStatus = '_Build complete_'
        } else {
            buildStatus = '_Back to normal_'
        }

        slackSend (color: 'good', message: "${buildStatus}: ${jobInfo} ${timeSpent}")
        slackSend (color: 'good', message: "*${env.BRANCH_NAME}* branch deployed to Serverless ")
        
    }


}


def timeDiff(st) {
    def delta = (new Date()).getTime() - st.getTime()
    def seconds = delta.intdiv(1000) % 60
    def minutes = delta.intdiv(60 * 1000) % 60

    return "${minutes} min ${seconds} sec"
}



