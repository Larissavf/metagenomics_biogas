configfile: 'config/config.yaml'

rule nanofilt:
    input:
        expand('{dir}', dir=config['test'])
    output:
        '/students/2023-2024/Thema07/biogas/qc/nanofilt/test.fastq'
    shell:
        'NanoFilt --headcrop 40 --tailcrop 20 --quality 15 {input} > {output}' 


# rule kraken2:
#     input:
#         directory('/students/2023-2024/Thema07/biogas/qc/chopper')
#     output:
#         directory('/students/2023-2024/Thema07/biogas/taxonomy/k2_output.txt')
#     shell:
#         'KRAKEN2_DEFAULT_DB="/data/datasets/KRAKEN2_INDEX/k2_standard_20231009"'
#         'kraken2 --db Standard --report k2_report.txt --output {output} {input}'

# expand('{dir}{sample}.fastq , dir=config['fastq'], sample=config['sample']')
#vraag is dan of de dir en sample random gaan of niet:)

