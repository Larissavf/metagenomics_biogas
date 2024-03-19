configfile: 'config/config.yaml'

rule nanoplot_qc:
    input:
        expand('{dir}', dir=config['test'])
    output:
        directory('/students/2023-2024/Thema07/biogas/qc/nanoqc')
    shell:
        'Nanoplot --fastq {input} -o {output}'


  --maxlength N         Hide reads longer than length specified.
  --minlength N         Hide reads shorter than length specified.
  --minqual N           Drop reads with an average quality lower than specified.
