import glob
configfile: 'config/config.yaml'

d = {}
for sample_dir in config['fast5']:
    all_samples_dir = glob.glob(sample_dir+ "/*")
    for samples_dir in all_samples_dir:
        basename = os.path.splitext(sample_name)
        basename = os.path.basename(basename[0])
        d[basename] = sample_name

OD = config['output_dir']

rule all:
    input:
        expand(OD + "basecalled/{sample}.fastq", sample=list((d.keys())))

rule dorado_basecaller:
    input:
        lambda wildcards: d[wildcards.sample]
    output:
        basecalled_fastq = OD + "basecalled/{sample}.fastq"
    params:
        dorado_path = "/opt/ont/dorado-0.5.3-linux-x64/bin/dorado",
        model_path = "~/projects/dorado/dna_r10.4.1_e8.2_400bps_fast@v4.1.0/"
    shell:
        "{params.dorado_path} basecaller {params.model_path} {input.fast5} > {output.basecalled_fastq}"