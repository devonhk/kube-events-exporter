### Quickstart

**Install mongodb in your cluster** 

More information here: https://github.com/bitnami/charts/tree/master/bitnami/mongodb
1. `helm repo add bitnami https://charts.bitnami.com/bitnami`'
2. `helm repo update`
3. `helm install mongodb bitnami/mongodb`

**Create secrets containing mongodb credentials**

`kubectl create secret generic mongodb-credentials --from-literal=MONGO_PASSWORD=$(kubectl get secret --namespace default mongodb -o jsonpath="{.data.mongodb-root-password}" | base64 --decode) --namespace=k8s-event-exporter`

**Install the kube-events-exporter**

`kubectl apply -f https://raw.githubusercontent.com/pydo/kube-events-exporter/master/k8s_event_logger/manifests/manifest.yaml`