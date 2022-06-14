"""
Converts the dev files to usable format for translation evaluation
"""


def main():
    with open("/workspace/data/references/references.tsv", "r", encoding='utf-8') as f:
        lines = f.readlines()

    # lines = [l.encode("ascii", "ignore") for l in lines]

    lines = [l.split("\t") for l in lines]

    for i in range(len(lines[0])):
        with open("/workspace/data/references/test_references_{}".format(i),
                  "w",
                  encoding='utf-8') as f:
            ref_i = "\n".join([l[i].strip() for l in lines])
            f.write(ref_i)


if __name__ == "__main__":
    main()
