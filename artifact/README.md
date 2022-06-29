# Projects Artifacts

## Loading the docker image

Download the file from URL, then load the docker image using the command below:

```bash
source NeuralTextSimplification/artifact/scripts/env.sh
docker load --input ${PROJECT_NAME}_image.tar

docker run --rm --ipc=host --gpus all -v ${PWD}/output:/workspace/nts_output -it ${PROJECT_NAME}_image bash

```
