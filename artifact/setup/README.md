# Setup

We advise against rebuilding the docker container as it introduces a lot of other variables. Regardless, here are the instructions required for rebuilding the container. 

## Docker
```bash
# Clone the repository 

source NeuralTextSimplification/artifact/scripts/env.sh
docker build -t ${PROJECT_NAME}_image -f NeuralTextSimplification/artifact/setup/dockerfile NeuralTextSimplification/

docker save --output ${PROJECT_NAME}_image.tar ${PROJECT_NAME}_image

# inside the container, run the required commands

```
