#!/bin/bash

#! 作业名称
#SBATCH --job-name Iono_fit
#! 计费账号
#SBATCH --account astro
#! 需要的节点数
#SBATCH --nodes=2
#! 总任务数
#SBATCH --ntasks=2
#! 内存限制
##SBATCH --mem 100000M
#! 时间限制
#SBATCH --time=00:00:00
#! 邮箱
#SBATCH --mail-type=FAIL,END
#SBATCH --mail-user=liuyihong@cnlab.net
#! 不重新排队
##SBATCH --no-requeue
#! 指定分区
#SBATCH --partition astro-cpu
#! 集群名称
#SBATCH --clusters astrolab
#! 最大switches数
#SBATCH --switches=1
#! 优先使用那个node
#SBATCH --nodelist astrolab-hpc-[2-3]
#! 避开哪个node
##SBATCH --exclude astrolab-hpc-[9-13]
#! 输出文件名
#SBATCH --output ./slurm/slurm_out/slurm-sim-%A.out
#! 是否独占节点
##SBATCH --exclusive
#SBATCH --cpus-per-task=32


source /home/${USER}/.bashrc

#! Set up python
echo -e "Running python: `which python`"
echo -e "Running dask-scheduler: `which dask-scheduler`"
cd $SLURM_SUBMIT_DIR
echo -e "Changed directory to `pwd`.\n"
JOBID=${SLURM_JOB_ID}
echo ${SLURM_JOB_NODELIST}
 
mkdir local
 
 
# Start dask-scheduler on first node.
 
scheduler=$(hostname)
port=8786
outfile=${SLURM_JOB_NAME}_${SLURM_JOB_ID}_scheduler.out
#dask-scheduler --host $scheduler --port $port &> $outfile &
dask-scheduler --host $scheduler --port $port &
echo dask-scheduler started on ${scheduler}:${port}
sleep 5
 
# Start dask-worker on all nodes using srun.
 
srun -o %x_%j_worker_%n.out dask-worker --nprocs 16 --nthreads 1 --interface ib0 --memory-limit 100GB --local-directory ${SLURM_SUBMIT_DIR}/local ${scheduler}:${port} &
echo dask-worker started on all nodes
sleep 5
 
 
sleep 1
echo "Scheduler and workers now running"
 
 
#! We need to tell dask Client (inside python) where the scheduler is running
echo "Scheduler is running at ${scheduler}"
 
echo "run dask-worker"
python cluster_dask_test.py ${scheduler}:8786 | tee cluster_dask_test.log