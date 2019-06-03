# Farmshare instructions
We can run these as batch jobs to save time!

## Getting started
ssh ashwin99@rice.stanford.edu
git clone https://github.com/TheStanfordDaily/archives.git
cd archives
mkdir slurm_logs
YEAR_START=1892 sbatch --array=0-122 slurm-script.sh

## Quick ref
ssh ashwin99@rice.stanford.edu
sacct -u ashwin99 | grep RUNNING | wc -l # 512
squeue -u ashwin99 | wc -l # 259
tail -f slurm_logs/1479134.log
