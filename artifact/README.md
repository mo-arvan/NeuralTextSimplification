# Projects Artifacts

## Loading the docker image

Download the file from [Zenodo](https://zenodo.org/record/6618321), then load the docker image using the command below:
```bash
source NeuralTextSimplification/artifact/scripts/env.sh
docker load --input ${PROJECT_NAME}_image.tar

mkdir output
```

Now you can generate the results of table 3 and 4 using the commands below.
```bash
docker run --rm --ipc=host --gpus all -v ${PWD}/output:/workspace/nts_output -it ${PROJECT_NAME}_image bash artifact/scrip
ts/table_3_4.sh
```

Further instructions on achieving the other results of other table are available in [GitHub](https://github.com/mo-arvan/NeuralTextSimplification/tree/master/artifact). 