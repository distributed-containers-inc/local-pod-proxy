import os
import random
import sys

from kubernetes import client, config


def _err_write(msg):
  sys.stderr.write(str(msg))
  sys.stderr.write(os.linesep)
  sys.stderr.flush()


def main():
  pod_namespace = os.getenv('MY_POD_NAMESPACE')
  if pod_namespace is None:
    _err_write('MY_POD_NAMESPACE is not set, see example/deploy.yaml')
    exit(1)

  host_ip = os.getenv('MY_HOST_IP')
  if host_ip is None:
    _err_write('MY_HOST_IP is not set, see example/deploy.yaml')
    exit(1)

  label_selector = os.getenv('LABEL_SELECTOR')
  if label_selector is None:
    _err_write('LABEL_SELECTOR is not set, see example/deploy.yaml')
    exit(1)

  source_port = os.getenv('SOURCE_PORT')
  if source_port is None:
    _err_write('SOURCE_PORT is not set, see example/deploy.yaml')
    exit(1)

  target_port = os.getenv('TARGET_PORT')
  if target_port is None:
    _err_write('TARGET_PORT is not set, see example/deploy.yaml')
    exit(1)

  config.load_incluster_config()
  v1 = client.CoreV1Api()

  pods = v1.list_namespaced_pod(label_selector=label_selector,
      namespace=pod_namespace)
  pods = [pod.to_dict() for pod in pods.items]
  pods = [
    pod for pod in pods
    if pod.get('status', {}).get('host_ip', '') == host_ip
  ]
  pods = [
    pod for pod in pods
    if pod.get('status', {}).get('phase', '') == 'Running'
  ]
  proxy_to = random.choice(pods)['status']['pod_ip']
  print('will proxy 127.0.0.1:{} to {}:{}'.format(source_port, proxy_to, target_port))
  sys.stdout.flush()

  os.execvp('socat', [
    'socat', '-d',
    'TCP4-LISTEN:{},bind=127.0.0.1,reuseaddr,fork'.format(source_port),
    'TCP4:{}:{}'.format(proxy_to, target_port)
  ])
