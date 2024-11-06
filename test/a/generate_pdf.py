from fpdf import FPDF

# Create instance of FPDF class
pdf = FPDF()

# Add a page
pdf.add_page()

# Title and Introduction
pdf.set_font("Arial", "B", 14)
pdf.cell(200, 10, "Deploy a Mule API using Jenkins", ln=True, align="C")

# Adding content with steps
pdf.set_font("Arial", "", 12)
content = [
    "To deploy a Mule API using Jenkins, you’ll need to set up a Jenkins pipeline that builds, tests, "
    "and deploys your Mule API to your target environment (e.g., CloudHub, Anypoint Runtime Fabric, or an on-premise server). "
    "Here's a step-by-step guide:",

    "Prerequisites",
    "1. Mule Project: A MuleSoft project (e.g., Mule 4) with a properly configured pom.xml file if you're using Maven.",
    "2. Jenkins Setup: Jenkins should be installed and configured with required plugins:",
    "- Maven (if using a Maven-based Mule project)",
    "- Anypoint CLI (for deploying to CloudHub or Runtime Fabric)",
    "- Git (if you’re using version control)",
    "3. Anypoint Platform: An account in Anypoint Platform with API deployment permissions.",

    "Steps",

    "1. Set Up Jenkins Pipeline",
    "- Create a New Pipeline Job in Jenkins by going to New Item -> Pipeline.",
    "- Configure Source Code Management (SCM) to point to your Mule project repository (e.g., GitHub or Bitbucket).",

    "2. Write Jenkins Pipeline Script",
    "In the Pipeline section, use a Pipeline script like the following example:",

    '''pipeline {
    agent any

    environment {
        ANYPOINT_USERNAME = credentials('anypoint-username')
        ANYPOINT_PASSWORD = credentials('anypoint-password')
    }

    stages {
        stage('Checkout') {
            steps {
                // Pulls the latest code from the repository
                git branch: 'main', url: 'https://github.com/your-org/your-mule-app.git'
            }
        }

        stage('Build') {
            steps {
                // Use Maven to build the Mule application
                sh 'mvn clean package'
            }
        }

        stage('Test') {
            steps {
                // Run unit tests
                sh 'mvn test'
            }
        }

        stage('Deploy to CloudHub') {
            steps {
                // Deploy the Mule application to CloudHub
                sh '''
    anypoint-cli --username=$ANYPOINT_USERNAME --password=$ANYPOINT_PASSWORD \ \
    runtime-mgr cloudhub-application deploy \ \
    --file target/your-mule-app.jar \ \
    --target sandbox \ \
    --name your-mule-app-name
'''
}
}
}

post {
always {
echo 'Cleaning up workspace...'
cleanWs()
}
success {
echo 'Deployment successful!'
}
failure {
echo 'Deployment failed.'
}
}
}''',

"3. Configure Jenkins Credentials",
"- Go to Jenkins Dashboard > Manage Jenkins > Manage Credentials.",
"- Add credentials for ANYPOINT_USERNAME and ANYPOINT_PASSWORD for Anypoint CLI to access your Anypoint Platform account.",

"4. Build and Deploy",
"- Save the pipeline configuration.",
"- Click Build Now to start the deployment pipeline.",
"- Monitor the console output to track the stages and detect any issues in the process.",

"Notes",
"- Environment Target: Replace 'sandbox' with your actual target environment (e.g., 'prod').",
"- Error Handling: Customize the post steps to send notifications (e.g., via email or Slack) for success/failure.",

"This setup will automate the deployment of your Mule API from Jenkins, integrating with the Anypoint Platform for easy management."
]

# Add each section of content to the PDF
for paragraph in content:
    pdf.multi_cell(0, 10, paragraph)
    pdf.ln(5)

# Save the PDF
pdf.output("Mule_API_Deployment_Guide.pdf")
