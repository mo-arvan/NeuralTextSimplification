"""
Converts the dev files to usable format for translation evaluation
"""


def main():
    with open("/workspace/data/dev.en", "r") as f:
        lines = f.readlines()

    lines = [lines[i].lower() for i in range(0, len(lines), 8)]

    with open("/workspace/data/dev_eval.en", "w") as f:
        f.writelines(lines)

    with open("/workspace/data/dev.sen", "r") as f:
        lines = f.readlines()

    lines = [lines[i].lower() for i in range(0, len(lines), 8)]

    with open("/workspace/data/dev_eval.sen", "w") as f:
        f.writelines(lines)


if __name__ == "__main__":
    main()
