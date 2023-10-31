# K8s Base Template

Base Template for Kubernetes-based Projects

> If you have no experience with Gitlab Pipelines and Kubernetes, but still want to get the most out of this template, try to find computer science students from TH Lübeck who have either taken the master courses **"Cloud-native Programming"**, **"Cloud-native Architectures"** or the bachelor module **"Web and Cloud Computing Project"**.
> This group of students has experience with this tool chain and DevOps experience. They would not have passed these modules otherwise.

## Getting started

To make it easy for you to get started with this template, here's a list of recommended next steps.

Already a pro? Just edit this README.md and make it your own.

## Where do you find what?

- `.gitlab-ci.yaml`: The deployment pipeline composed of `prepare`, `build`, `deployment` and `expose` stages.
- `deploy/`: K8s manifest files that deploy an out-of-the-box ChatBot server and a containerized indexing job (if you plan to apply Retrieval Augmented Generation).
- `kira-ui/`: A simple Python ChatBot (streamlit based). Take this as a base camp for your own projects.
- `indexer`: A simple indexing Job that crawls German Jokes and indexes them using ChromaDB. Take this as a base camp for your own indexers.

The ChatBot and the indexer mount both the same volume, so the ChatBot has read-access to the Chroma-Database while the indexer has write access.

## Deploy

Just start a new [deployment pipeline](../../../-/pipelines/new) to deploy

- the example `kira` service (ChatBot) and 
- an `index` Job.

The pipeline is already prepared for automatic deployments. Feel free to adapt it according to your needs.

## Configure `kubectl` or `Lens`

You find your `KUBECONFIG` in Gitlab under Settings -> [VARIABLES](../../../-/settings/ci_cd).
Copy it and import it into [Lens](https://k8slens.dev) or set it as an environment variable on your local system.

You have then access to your connected Kubernetes namespace via `kubectl` or the Lens IDE. We recommend the Lens IDE.

```bash
kubectl get svc
# Should return kira service
```

```bash
kubectl get pod
# Should return a kira-ui pod and an indexer pod
```

You can forward service ports to your local system using `kubectl port-forward`

```bash
kubectl port-forward svc/kira 8080:80
```

Now, you can access your personal Kira ChatBot service on:

- [http://localhost:8080](http://localhost:8080)

You can also use the port-forwarding features from the Lens-UI.

## Expose your service to the public via an Ingress

By default, your services are made accessible to the general public externally by setting up an ingress. The pipeline provides a manually triggered ingress job in the expose stage. This makes your service available under the following externable reachable URL:

`https://demo-<< PROJECT_ID >>.llm.mylab.th-luebeck.dev` (You find your project id in Gitlab! If you read this README.md in Gitlab (web browser), just scroll all the way up now. You will find the ID directly under the name of this repo.)

Furthermore, you can add additional routes to the Ingress as needed and also set the update to automatic by commenting out the `when: manual` entry in the Ingress manifest `deploy/project-ing.yaml` or otherwise modifying the manifest file to suit your needs.

If you do not want this. Deactive the expose job in the pipeline. And delete the ingress using the Lens UI or via `kubectl`.

```bash
kubectl delete ing/demo
```

## Adapt

You are now ready to use this repo as a base camp for your Hanseatic Hackathon 2023 project.

Code strong!
