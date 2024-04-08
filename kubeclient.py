import os

import logging

from kubernetes import config, client

logger = logging.getLogger(__name__)


class Params:
    def __init__(self, node, namespace, name, service):
        self.node = node
        self.namespace = namespace
        self.name = name
        self.service = service

    def __str__(self):
        return f"node: {self.node}, namespace: {self.namespace}, name: {self.name}, service: {self.service}"


class KubeClient:
    def __init__(self, params: Params):
        self.params = params
        self.kubeconfig = os.getenv("KUBECONFIG")
        if self.kubeconfig == "":
            self.kubeconfig = "~/.kube/config"

        self.core_v1 = client.CoreV1Api(
            client.ApiClient(
                configuration=config.load_kube_config(config_file=self.kubeconfig)
            )
        )

    def get_pod(self):
        pod = self.core_v1.read_namespaced_pod(
            name=self.params.name, namespace=self.params.namespace
        )
        return pod

    def get_service(self):
        service = self.core_v1.read_namespaced_service(
            name=self.params.service, namespace=self.params.namespace
        )
        return service

    def get_node(self):
        node = self.core_v1.read_node(name=self.params.node)
        return node
