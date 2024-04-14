import os 

configfile: 'config/config.yaml'

fastq_out_bov = "/students/2023-2024/Thema07/biogas/output/boven"
fastq_out_mid = "/students/2023-2024/Thema07/biogas/output/midden"
fastq_out_onder = "/students/2023-2024/Thema07/biogas/output/onder"
fastq_out_pac = "/students/2023-2024/Thema07/biogas/output/basecalled/"

pod5_out_bov : "/students/2023-2024/Thema07/biogas/output/new_fast5/Boven2/"
pod5_out_mid : "/students/2023-2024/Thema07/biogas/output/new_fast5/Midden3/"
pod5_out_onder : "/students/2023-2024/Thema07/biogas/output/new_fast5/Onder1/"
pod5_out_pac :"/students/2023-2024/Thema07/biogas/output/new_fast5/"

SAMPLES_b = [os.path.basename(f) for f in os.listdir(pod5_out_bov) if os.path.isfile(os.path.join(pod5_out_bov, f))]
SAMPLES_m = [os.path.basename(f) for f in os.listdir(pod5_out_mid) if os.path.isfile(os.path.join(pod5_out_mid, f))]
SAMPLES_o = [os.path.basename(f) for f in os.listdir(pod5_out_onder) if os.path.isfile(os.path.join(pod5_out_onder, f))]
SAMPLES_p = [os.path.basename(f) for f in os.listdir(pod5_out_pac) if os.path.isfile(os.path.join(pod5_out_pac, f))]

SAMPLES_b = [sample.replace('.fast5', '') for sample in SAMPLES_b]

SAMPLES_m = [sample.replace('.fast5', '') for sample in SAMPLES_m]

SAMPLES_o = [sample.replace('.fast5', '') for sample in SAMPLES_o]

SAMPLES_p = [sample.replace('.fast5', '') for sample in SAMPLES_p]

rule all:
    input:
        expand("{output_dir}/pod5_out_bov/{sample}.fastq", output_dir=config['output_dir'], sample=SAMPLES),
        expand("{output_dir}/pod5_out_mid/{sample}.fastq", output_dir=config['output_dir'], sample=SAMPLES),
        expand("{output_dir}/pod5_out_onder/{sample}.fastq", output_dir=config['output_dir'], sample=SAMPLES),
        expand("{output_dir}/pod5_out_pac/{sample}.fastq", output_dir=config['output_dir'], sample=SAMPLES)

rule dorado:
    input:
        bov = expand(config['pod5_out_bov'] + "{sample}.pod5", sample=SAMPLES_b),
        mid = expand(config['pod5_out_mid'] + "{sample}.pod5", sample=SAMPLES_m),
        onder = expand(config['pod5_out_onder'] + "{sample}.pod5", sample=SAMPLES_o),
        pac = expand(config['pod5_out_pac'] + "{sample}.pod5", sample=SAMPLES_p)
    output:
        bov_out = expand(config['fastq_out_bov'] + "{sample}.fastq", sample=SAMPLES_b),
        mid_out = expand(config['fastq_out_mid'] + "{sample}.fastq", sample=SAMPLES_m),
        onder_out = expand(config['fastq_out_onder'] + "{sample}.fastq", sample=SAMPLES_o),
        pac_out = expand(config['fastq_out_pac'] + "{sample}.fastq", sample=SAMPLES_p)
    params:
        dorado_path = "/opt/ont/dorado-0.5.3-linux-x64/bin/dorado",
        model_path = "/homes/sschoonen/projects/dorado/dna_r10.4.1_e8.2_400bps_sup@v4.1.0/"
    shell:
        "
        {params.dorado_path} basecaller {params.model_path} {input.bov} --emit-fastq > {output.bov_out} -I 4G -x cuda:0 --batchsize 64
        {params.dorado_path} basecaller {params.model_path} {input.mid} --emit-fastq > {output.mid_out} -I 4G -x cuda:0 --batchsize 64
        {params.dorado_path} basecaller {params.model_path} {input.onder} --emit-fastq > {output.onder_out} -I 4G -x cuda:0 --batchsize 64
        {params.dorado_path} basecaller {params.model_path} {input.pac} --emit-fastq > {output.pac_out} -I 4G -x cuda:0 --batchsize 64
        "
