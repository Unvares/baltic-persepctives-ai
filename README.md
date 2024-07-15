# Baltic Hackathon 2024 Base Camp

Base Template for Kubernetes-based Projects

This repo contains the examples from the videos:

- ["How to build a chatbot"](https://youtu.be/Fz3aux9CxDM) and
- ["How to cure hallucinations of your chatbot"](https://youtu.be/JWM2VamdM8c)

> If you have no experience with Gitlab Pipelines and Kubernetes, but still want to get the most out of this template, try to find computer science students from TH Lübeck who have either taken the master courses **"Cloud-native Programming"**, **"Cloud-native Architectures"** or the bachelor module **"Web and Cloud Computing Project"**.
> This group of students has experience with this tool chain and DevOps experience.

## Getting started

To make it easy for you to get started with this template, here's a list of recommended next steps.

First, we recommend to install:

- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- The Kubernetes IDE [Lens](https://k8slens.dev/) (you need to register, but more dev comfort) or [OpenLens](https://github.com/MuhammedKalkan/OpenLens) (no need to register, but older and less dev comfort)
- [Python](https://www.python.org/downloads/)
- [vscode](https://code.visualstudio.com/) with [Python extension](https://marketplace.visualstudio.com/items?itemName=ms-python.python) installed

Already a pro? Just edit this README.md and make it your own.

### Where do you find what?

- `.gitlab-ci.yaml`: The deployment pipeline composed of `prepare`, `build`, `deployment` and `expose` stages (do not touch if you do not know what you are doing)
- `deploy/`: K8s manifest files that deploy an ChatBot (do not touch if you do not know what you are doing)
- `chatbot/`: A simple Python ChatBot (streamlit based). Take this as a base camp for your own projects (customise as you see fit)
- `chatbot-rag/`: A simple Python ChatBot with a Prompt Engineering knowledge based (Streamlit and RAG-based). Take this as a base camp for your own projects if you want to make use of retrieval augmentend generation. This example stores the contents of [promptingguide.ai](https://www.promptingguide.ai/) in a vector store (customise as you see fit)
- `notebooks/`: Examples of how to use language models programmatically (we recommend trying it out on our [JupyterHub](https://jhub.mylab.th-luebeck.de) system)

### Build and run the basic chatbot locally

To build and run the basic Chatbot do the following: 

```
cd chatbot
docker build -t chatbot .
docker run -p 8501:8501 chatbot
```

*The container build can take some time, especially during the first build on a host.*

Now you can access the chatbot using this link [http://localhost:8501](http://localhost:8501).

### Build and run the Prompt Engineering Chatbot locally

To build and run the Prompt Engineering Chatbot with Retrieval Augmented Generation do the following: 

```
cd chatbot-rag
docker build --build-arg EMBEDDING_EP=https://bge-m3-embedding.llm.mylab.th-luebeck.dev/ -t chatbot-rag .
docker run -p 8502:8501 chatbot-rag
```

*The container build can even take some more time, especially during the first build on a host.*

Now you can access the chatbot using this link [http://localhost:8502](http://localhost:8502).


### Deploy

This repo contains a pipeline that is already prepared for automatic deployments. Whenever you push a commit to this repo, the pipeline is automatically started.

However, you can trigger this process manually. Just start a new [deployment pipeline](../../../-/pipelines/new) to deploy the example `chatbot` service (ChatBot).

***Be aware:** A pipeline run can take some time (up to 10 minutes). The necessary libraries compromise some machine learning libraries that have noteworthy download volumes.*

### Configure `kubectl` or `Lens`

You find your `KUBECONFIG` in Gitlab under Settings -> [VARIABLES](../../../-/settings/ci_cd).
Copy it and import it into [Lens](https://k8slens.dev) or set it as an environment variable on your local system.

You have then access to your connected Kubernetes namespace via `kubectl` or the Lens IDE. We recommend the Lens IDE.

```bash
kubectl get svc
# Should return chatbot and chatbot-rag service
```

```bash
kubectl get pod
# Should return a chatbot pod and a chatbot-rag pod
```

You can forward service ports to your local system using `kubectl port-forward`

```bash
kubectl port-forward svc/chatbot 8501:8501
kubectl port-forward svc/chatbot-rag 8502:8501
```

Now, you can access your personal ChatBot service on:

- [http://localhost:8501](http://localhost:8501)
- [http://localhost:8502](http://localhost:8502) (The prompt engineering knowledge base version)


You can also use the port-forwarding features from the Lens-UI.

### Expose your service to the public via an Ingress

By default, your services are made accessible to the general public externally by setting up an ingress. The pipeline provides a manually triggered ingress job in the expose stage. This makes your service available under the following externable reachable URL:

`https://chatbot-<< PROJECT_ID >>.llm.mylab.th-luebeck.dev` or `https://chatbot-rag-<< PROJECT_ID >>.llm.mylab.th-luebeck.dev` (You find your project id in Gitlab! If you read this README.md in Gitlab (web browser), just scroll all the way up now. You will find the ID under the burger menu (&vellip;) next to the fork menu of this repo.

Furthermore, you can add additional routes to the Ingress as needed and also set the update to automatic by commenting out the `when: manual` entry in the Ingress manifest `deploy/project-ing.yaml` or otherwise modifying the manifest file to suit your needs.

If you do not want this. Deactive the expose job in the pipeline. And delete the ingress using the Lens UI or via `kubectl`.

```bash
kubectl delete ing/demo
```

### Adapt

You are now ready to use this repo as a base camp for your Baltic Hackathon 2024 project.

Code strong!
