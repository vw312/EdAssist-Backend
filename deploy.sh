docker build -t vw312/edassist-backend:latest -t vw312/edassist-backend:$SHA ./client 

docker push vw312/edassist-backend:latest

docker push vw312/edassist-backend:$SHA

kubectl apply -f k8s

kubectl set image deployments/edassist-deployment edassist-backend=vw312/edassist-backend:$SHA