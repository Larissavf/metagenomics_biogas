import os
import tourch

torch.cuda.empty_cache()

pod5_out_bov = "/students/2023-2024/Thema07/biogas/output/new_fast5/Boven2/"
pod5_out_mid = "/students/2023-2024/Thema07/biogas/output/new_fast5/Midden3/"
pod5_out_onder = "/students/2023-2024/Thema07/biogas/output/new_fast5/Onder1/"
pod5_out_pac = "/students/2023-2024/Thema07/biogas/output/new_fast5/"

fastq_out_bov = "/students/2023-2024/Thema07/biogas/output/boven"
fastq_out_mid = "/students/2023-2024/Thema07/biogas/output/midden"
fastq_out_onder = "/students/2023-2024/Thema07/biogas/output/onder"
fastq_out_pac = "/students/2023-2024/Thema07/biogas/output/new_fast5/basecalled/"

samples_bov = [f.replace(".pod5", "") for f in os.listdir(pod5_out_bov)]
samples_mid = [f.replace(".pod5", "") for f in os.listdir(pod5_out_mid)]
samples_onder = [f.replace(".pod5", "") for f in os.listdir(pod5_out_onder)]
samples_pac = [f.replace(".pod5", "") for f in os.listdir(pod5_out_pac)]

def run_dorado(sample, input_dir, output_dir):
	
    dorado_path = "/opt/ont/dorado-0.5.3-linux-x64/bin/dorado"
    model_path = "/homes/sschoonen/projects/dorado/dna_r10.4.1_e8.2_400bps_fast@v4.1.0/"
    input_file = os.path.join(input_dir, f"{sample}.pod5")
    output_file = os.path.join(output_dir, f"{sample}.fastq")
    cmd = f"{dorado_path} basecaller {model_path} {input_file} --emit-fastq > {output_file} -I 4G -x cuda:0 --batchsize 64"
    os.system(cmd)

for sample in samples_bov:
    run_dorado(sample, pod5_out_bov, fastq_out_bov)

for sample in samples_mid:
    run_dorado(sample, pod5_out_mid, fastq_out_mid)

for sample in samples_onder:
    run_dorado(sample, pod5_out_onder, fastq_out_onder)

for sample in samples_pac:
    run_dorado(sample, pod5_out_pac, fastq_out_pac
