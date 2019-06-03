#!/bin/bash
#SBATCH --job-name=tsd_archives_text_extractor    # Job name
#SBATCH --mail-type=END,FAIL          # Mail events (NONE, BEGIN, END, FAIL, ALL)
#SBATCH --ntasks=2                    # Run on a single CPU
#SBATCH --mem=1600mb                     # Job memory request
#SBATCH --time=40:00:00               # Time limit hrs:min:sec
#SBATCH --output=slurm_logs/%A_%a.log   # Standard output and error log
pwd; hostname; date

node extract-text.js $((YEAR_START + SLURM_ARRAY_TASK_ID))
