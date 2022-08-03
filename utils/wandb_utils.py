import os
from typing import List

import wandb


def wandb_log_artifact(wandb_run_instance: wandb.sdk.wandb_run.Run,
                       artifact_name: str,
                       description: str,
                       file_path: List[str],
                       artifact_type: str = "data",
                       metadata: dict = None,
                       remove_logged_file: bool = True):
    artifact = wandb.Artifact(name=artifact_name, type=artifact_type, description=description, metadata=metadata)
    for fp in file_path:
        artifact.add_file(fp)
    wandb_run_instance.log_artifact(artifact)
    artifact.wait()
    if remove_logged_file:
        for fp in file_path:
            os.remove(fp)


def get_wandb_artifact(wandb_run_instance: wandb.sdk.wandb_run.Run,
                       artifact_name: str,
                       file_name: str,
                       tag: str = "latest",
                       artifact_type='data'):

    target_artifact = "{}:{}".format(artifact_name, tag)

    artifact = wandb_run_instance.use_artifact(target_artifact, type=artifact_type)
    artifact_dir = artifact.download()
    return artifact, os.path.join(artifact_dir, file_name)
