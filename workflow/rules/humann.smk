import glob
configfile: 'config/config.yaml'

d = {}
for sample_name in config['fastq_all']:
    basename = os.path.splitext(sample_name)
    basename = os.path.basename(basename[0])
    d[basename] = sample_name

OD = config['output_dir']


rule all:
    input:
        expand(OD + 'human3_2/{sample}', sample=list((d.keys())))

# human3 is a package in biobakery
rule human3:
   input:
        lambda wildcards: d[wildcards.sample]
   output:
       directory(OD + 'human3_2/{sample}')
   shell:
    #    "humann_databases --download chocophlan full {config["choco"]} && "
    #    "humann_databases --download uniref uniref50_ec_filtered_diamond reduced {config["uniref"]} && "
        "humann --input {input} --output {output} --nucleotide-database {config[choco]} --protein-database {config[uniref]} --bowtie-options very-fast 2>human.txt"
    
