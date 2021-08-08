"""Watch multiple K8s event streams without threads."""
import asyncio
import traceback
import uvloop
from functools import wraps

from kubernetes_asyncio import client, config, watch

from config import NAMESPACE_DENYLIST
from database.db import events, insert_k8s_event


def _core_v1_api(f):
    @wraps(f)
    async def wrapper(*args, **kwargs):
        async with client.ApiClient() as api:
            v1 = client.CoreV1Api(api)
            func_return = await f(v1, *args, **kwargs)
            return func_return

    return wrapper


def _apps_v1_api(f):
    @wraps(f)
    async def wrapper(*args, **kwargs):
        async with client.ApiClient() as api:
            v1 = client.AppsV1Api(api)
            func_return = await f(v1, *args, **kwargs)
            return func_return

    return wrapper


@_core_v1_api
async def watch_namespaces(core_v1_api):
    await generic_watch_resource(resources_to_stream=core_v1_api.list_namespace,
                                 object_type=events.NAMESPACE_EVENT)


@_core_v1_api
async def watch_pods(core_v1_api):
    await generic_watch_resource(resources_to_stream=core_v1_api.list_pod_for_all_namespaces,
                                 object_type=events.POD_EVENT)


@_core_v1_api
async def watch_configmaps(core_v1_api):
    await generic_watch_resource(resources_to_stream=core_v1_api.list_config_map_for_all_namespaces,
                                 object_type=events.CONFIGMAP_EVENT)


@_core_v1_api
async def watch_secrets(core_v1_api):
    await generic_watch_resource(resources_to_stream=core_v1_api.list_secret_for_all_namespaces,
                                 object_type=events.SECRET_EVENT)


@_apps_v1_api
async def watch_deployments(apps_v1_api):
    await generic_watch_resource(resources_to_stream=apps_v1_api.list_deployment_for_all_namespaces,
                                 object_type=events.DEPLOYMENT_EVENT)


@_apps_v1_api
async def watch_replicasets(apps_v1_api):
    await generic_watch_resource(resources_to_stream=apps_v1_api.list_replica_set_for_all_namespaces,
                                 object_type=events.REPLICASET_EVENT)


async def generic_watch_resource(resources_to_stream,
                                 object_type):
    while True:
        print(f'Starting resource watch on {object_type}')
        async with watch.Watch().stream(resources_to_stream) as stream:
            try:
                async for event in stream:

                    if 'namespace' in event['raw_object']['metadata'] and \
                            event['raw_object']['metadata']['namespace'] in NAMESPACE_DENYLIST:
                        continue

                    if 'namespace' in event['raw_object']['metadata'] and \
                            event['raw_object']['metadata']['namespace'] in NAMESPACE_DENYLIST:
                        continue

                    evt, obj = event['type'], event['object']
                    print(f"{evt} {obj.kind} {obj.metadata.name} in NS {obj.metadata.namespace}")

                    insert_k8s_event(obj_type=object_type,
                                     raw_obj=event['raw_object'],
                                     event_type=evt)

            except client.exceptions.ApiException as err:
                if err.status == 410:
                    print('happens sometimes, idk why')
                    raise
                if err.status == 401:
                    print("auth TOKEN probably expired")
                    print('refreshing auth TOKEN')
                    # await config.load_kube_config()
                    raise


async def rerun_on_exception(coro, *args, **kwargs):
    """Source: https://stackoverflow.com/a/55185488"""
    while True:
        try:
            await coro(*args, **kwargs)
        except asyncio.CancelledError:
            # don't interfere with cancellations
            raise
        except Exception:  # noqa
            print("Caught exception")
            traceback.print_exc()
        except client.exceptions.ApiException as err:
            if err.status == 401:
                await config.load_kube_config()  # refresh k8s auth token


def main():
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    loop = asyncio.get_event_loop()

    # Load the kubeconfig file specified in the KUBECONFIG environment
    # variable, or fall back to `~/.kube/config`.
    loop.run_until_complete(config.load_kube_config())

    # Define the tasks to watch namespaces and pods.
    tasks = [
        asyncio.ensure_future(rerun_on_exception(watch_namespaces())),
        asyncio.ensure_future(rerun_on_exception(watch_pods())),
        asyncio.ensure_future(rerun_on_exception(watch_configmaps())),
        asyncio.ensure_future(rerun_on_exception(watch_replicasets())),
        asyncio.ensure_future(rerun_on_exception(watch_deployments()))
    ]

    # Push tasks into event loop.
    loop.run_forever()
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()


if __name__ == '__main__':
    main()
