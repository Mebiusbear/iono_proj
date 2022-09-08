## ARatmospy
```
git clone https://github.com/shrieks/ARatmospy
```

## 生成相屏文件
```
cp /mnt/storage-work/liuyihong/FILE_1/gen_ionospheric_phase_screen_3layers.py ./
```

+ 运行gen_ionospheric_phase_screen.py就可以得到test_screen_60s.fits

## OSKAR镜像
```
mkdir OSKAR && cd OSKAR
cp /mnt/storage-work/liuyihong/FILE_1/oskar_python3_cuda114_newest.sif ./
```

## 仿真文件
```
cp /mnt/storage-work/liuyihong/FILE_1/GLEAM_EGC.fits ./

cp -r /mnt/storage-work/liuyihong/FILE_1/telescope_data ./

cp /mnt/storage-work/liuyihong/FILE_1/main.py ./
```


+ 进入singularity
```
singularity shell --nv -H $PWD oskar_python3_cuda114_newest.sif

python3 main.py
```
