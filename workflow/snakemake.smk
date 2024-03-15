configfile: 'config/config.yaml'

rule nanoplot_qc:
    input:
        expand('{dir}', dir=config['seqsum_file'])
    output:
        directory('/students/2023-2024/Thema07/biogas/qc/nanoqc')
    conda:
        '..conda/envs/trimming.yaml' 
    shell:
        'Nanoplot --summary {input} -o {output}'
