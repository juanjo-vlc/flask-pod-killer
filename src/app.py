from os import getenv

from flask import Flask, render_template, request
from kubernetes import client, config

app = Flask(__name__)

def get_running_pods(namespace):
    config.load_incluster_config()
    v1 = client.CoreV1Api()

    pods = v1.list_namespaced_pod(namespace=namespace)
    running_pods = []

    for pod in pods.items:
        if pod.status.phase == "Running":
            running_pods.append(pod.metadata.name)

    return running_pods

def kill_pod(namespace, pod_name):
    config.load_incluster_config()
    v1 = client.CoreV1Api()

    v1.delete_namespaced_pod(pod_name, namespace)

@app.route('/')
def index():
    namespace = getenv('KUBERNETES_NAMESPACE', 'default')
    running_pods = get_running_pods(namespace)
    return render_template('index.html', pods=running_pods)

@app.route('/kill', methods=['POST'])
def kill():
    namespace = getenv('KUBERNETES_NAMESPACE', 'default')
    pod_name = request.form.get('pod')

    if pod_name:
        kill_pod(namespace, pod_name)
        return f"Killed pod: {pod_name}"
    else:
        return "No pod selected."

if __name__ == '__main__':
    app.run()
