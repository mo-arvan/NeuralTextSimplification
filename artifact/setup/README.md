# Setup

We advise against rebuilding the docker container as it  may introduce other variables into the process. 

Regardless, here are the instructions required for rebuilding the container. 

## Docker
```bash
# Clone the repository 
git clone https://github.com/mo-arvan/NeuralTextSimplification.git
source NeuralTextSimplification/artifact/scripts/env.sh
docker build --no-cache -t ${PROJECT_NAME}_image -f NeuralTextSimplification/artifact/setup/dockerfile NeuralTextSimplification/
docker save --output ${PROJECT_NAME}_image.tar ${PROJECT_NAME}_image
```
Please refer to artifacts README file for instructions on how to run the container.