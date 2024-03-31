import glob
configfile: 'config/config.yaml'

d = {}
for sample_dir in config['fast5']:
    all_samples_dir = glob.glob(sample_dir+ "/*")
    for samples_dir in all_samples_dir:
        basename = os.path.splitext(sample_name)
        basename = os.path.basename(basename[0])
        d[basename] = sample_name

rule dorado:
    input:
        lambda wildcards: d[wildcards.sample]

