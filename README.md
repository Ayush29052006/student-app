\# Student Info App - CI/CD Pipeline (CCA 2)



TYCSE, Cloud Computing and DevOps. Automated CI/CD pipeline using GitHub, Jenkins, Docker, Docker Hub and Minikube on AWS EC2.



\## 1. Project

A small Flask web app (Student Info) with routes `/`, `/students` and `/health`. Three pytest tests check the routes.



\## 2. Repository layout

\- `app.py`, `requirements.txt`, `test\_app.py`: application and tests

\- `Dockerfile`: builds the container image

\- `Jenkinsfile`: declarative pipeline

\- `k8s/deployment.yaml`, `k8s/service.yaml`: Kubernetes manifests



\## 3. Pipeline stages (Jenkinsfile)

1\. \*\*Checkout\*\*: Jenkins pulls the latest code from GitHub (`main`).

2\. \*\*Build and Test\*\*: creates a Python virtual environment, installs requirements and runs `pytest`.

3\. \*\*Docker Build\*\*: builds `kanadeayush29/studentapp:<BUILD\_NUMBER>`.

4\. \*\*Push Image\*\*: logs in to Docker Hub with the Jenkins credential `dockerhub-creds` and pushes the image.

5\. \*\*Deploy to Minikube\*\*: updates the image tag in `k8s/deployment.yaml` and runs `kubectl apply -f k8s/`, then waits for the rollout.

6\. \*\*Verify\*\*: runs `kubectl get pods`, `get deployment` and `get svc`.



\## 3a. Automatic trigger

A GitHub webhook (`http://<EC2-IP>:8080/github-webhook/`, push event) starts the pipeline on every push.



\## 4. Jenkins setup on AWS

\- EC2 instance: Ubuntu, c7i-flex.large, 30 GiB disk, region ap-south-1 (Mumbai)

\- Security group inbound ports: 22 (SSH), 8080 (Jenkins), 30007 (app)

\- Installed: OpenJDK 21, Docker, Jenkins (LTS), kubectl, Minikube (docker driver)

\- Jenkins user added to the `docker` group and given the kubeconfig for Minikube

\- Pipeline job `student-app-pipeline`: "Pipeline script from SCM", Git, branch `\*/main`, script path `Jenkinsfile`

\- Docker Hub access token stored in Jenkins as "Username with password" (ID `dockerhub-creds`). No secrets are kept in the repo.



\## 5. Image push

Jenkins tags each image with the build number and pushes it to Docker Hub: `kanadeayush29/studentapp:<BUILD\_NUMBER>`.



\## 6. Deployment and access

\- Deployment `studentapp-deployment` (2 replicas) pulls the image from Docker Hub.

\- Service `studentapp-service` (NodePort 30007) exposes the pods.

\- Minikube runs inside Docker on the EC2 server, so port 30007 is forwarded to the server's public IP with `socat`:

&#x20; `socat TCP-LISTEN:30007,fork,reuseaddr TCP:$(minikube ip):30007`

\- Open `http://<EC2-Public-IP>:30007`



\## 7. Verification

`kubectl get pods`, `kubectl get deployment` and `kubectl get svc` show 2/2 pods running; the app responds in the browser.



\## 8. Second run (code change)

Changed the home page text from "Version 1" to "Version 2" in `app.py` and pushed to GitHub. The webhook triggered build #2 automatically, which pushed image tag `2`, rolled out the new pods, and the browser showed "Student Info App - Version 2".

