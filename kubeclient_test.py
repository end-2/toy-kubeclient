import unittest
from unittest.mock import patch
from kubeclient import Params, KubeClient

class TestKubernetesClient(unittest.TestCase):
    @patch('kubernetes.client.CoreV1Api.read_namespaced_pod')
    def test_get_pod(self, mock_read_namespaced_pod):
        mock_read_namespaced_pod.return_value = {
            "metadata": {"name": "pod1"},
            "status": {"pod_ip": "172.16.1.1"}
        }
        params = Params("node1", "namespace1", "pod1", "service1")
        kube_client = KubeClient(params)
        pod = kube_client.get_pod()
        self.assertEqual(pod["metadata"]["name"], "pod1")
        self.assertEqual(pod["status"]["pod_ip"], "172.16.1.1")

    @patch('kubernetes.client.CoreV1Api.read_namespaced_service')
    def test_get_service(self, mock_read_namespaced_service):
        mock_read_namespaced_service.return_value = {
            "metadata": {"name": "service1"},
            "spec": {"cluster_ip": "172.16.1.1"}
        }
        params = Params("node1", "namespace1", "pod1", "service1")
        kube_client = KubeClient(params)
        service = kube_client.get_service()
        self.assertEqual(service["metadata"]["name"], "service1")
        self.assertEqual(service["spec"]["cluster_ip"], "172.16.1.1")

    @patch('kubernetes.client.CoreV1Api.read_node')
    def test_get_node(self, mock_read_node):
        mock_read_node.return_value = {
            "metadata": {"name": "node1"},
            "status": {"addresses": [{"type": "InternalIP", "address": "10.0.0.1"}]}
        }
        params = Params("node1", "namespace1", "pod1", "service1")
        kube_client = KubeClient(params)
        node = kube_client.get_node()
        self.assertEqual(node["metadata"]["name"], "node1")
        self.assertEqual(node["status"]["addresses"][0]["address"], "10.0.0.1")


if __name__ == '__main__':
    unittest.main()
