### Overview

Logs every state of a given watched resource in mongodb. This allows us to construct timelines of what happened during
incidents. This component is might to provide the data to observability tools. Some more examples:
- A given workload started logging lots of errors 20mins after the last deployment. Go through all the states of related objects that changed
in that time period to see what could have led to the incident
- Correlate state changes of k8s objects with external events (metrics from newrelic, stackdriver, etc)


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

**Screencast**

asciinema