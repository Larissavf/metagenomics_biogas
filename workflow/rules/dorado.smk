FAST5_DIRS = config["directories"]["fast5"]
OUTPUT_DIRS = [
    config["directories"]["pod5_out_bov"],
    config["directories"]["pod5_out_mid"],
    config["directories"]["pod5_out_onder"],
    config["directories"]["pod5_out_pac"]
]

rule all:
    input:
        expand(OUTPUT_POD5_DIRS[i] + "/{sample}.pod5", i=range(len(OUTPUT_POD5_DIRS)))

# fast 5 to pod5
rule convert_to_pod5:
    input:
        fast5 = FAST5_DIRS[i] + "{sample}.fast5"
    output:
        pod5 = OUTPUT_POD5_DIRS[i] + "{sample}.pod5"
    shell:
        "pod5 convert fast5 {input.fast5} -o {output.pod5}"
