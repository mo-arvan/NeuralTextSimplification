"""
Loads a base search config, changes the model_name, gpuid, and the random seed for two gpus

# save_model = /workspace/models/nts
# log_file = /workspace/models/nts.log
# gpuid = 1
# seed = 3435
"""
import os


def main():
    with open("/workspace/configs/nts_search_base.cfg") as base_config_file:
        base_config = base_config_file.readlines()
    nts_search_config_dir = "/workspace/configs/nts_search_configs"
    if not os.path.isdir(nts_search_config_dir):
        os.makedirs(nts_search_config_dir)
    if not os.path.isdir(os.path.join(nts_search_config_dir, "0")):
        os.makedirs(os.path.join(nts_search_config_dir, "0"))
    if not os.path.isdir(os.path.join(nts_search_config_dir, "1")):
        os.makedirs(os.path.join(nts_search_config_dir, "1"))

    for i in range(50):
        # copy the base config without reference
        experiment_config = list(base_config)

        output_dir = "/workspace/models/nts_search_{}".format(i)
        experiment_config.insert(1, "save_model = {} \n".format(output_dir))
        experiment_config.insert(1, "log_file = {}_train.log \n".format(output_dir, i))
        experiment_config.insert(1, "gpuid = {} \n".format(i % 2 + 1))
        experiment_config.insert(1, "seed = {} \n".format(2022 + i))

        with open(os.path.join(nts_search_config_dir,
                               "{}".format(i % 2),
                               "nts_search_{}.cfg".format(i)), "w") as search_config_file:
            search_config_file.writelines(experiment_config)


if __name__ == "__main__":
    main()
