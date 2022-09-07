# Hot to use iono_proj

```
git clone https://github.com/Mebiusbear/iono_ptoj.git
export PYTHONPATH=$PYTHONPATH: /path/to/iono_proj
```

## mac run
```
python main.py -np 4000 -s 5 -nw 16 -bs 800 -mr  
```

## linux run
```
python main.py -np 4000 -s 5 -nw 16 -bs 800 -lr  
```

## just see picture
```
python main.py -np 4000 -s 5 -po -mmp
```

# How to download GIM

```python
ionox.download_codg(year=2022,begin=10,end=11)
ionox.unzip_Z(filename)
```
+ args(begin, end) is which date range you want to downloads

# How to read GIM

```python
tecarray, rmsarray, lonarray, latarray, timearray = ionox.read_tec_file(filename)
```
<!-- + tecarray.shape =  -->


# How to use spherical harmonic to fits GIM

## Part 1 (Find out where to fit)

```python
tec_dataset = tecarray[4][40:55,35:50]
lon_dataset = lonarray[35:50]
lat_dataset = latarray[40:55]
```
## Part 2 (zip longititue and latitude with spherical)

```python
beta_c_arr, lam_c_arr = spherical_triangle_transform(lon_dataset,lat_dataset,p_lat=np.radians(10),p_lon=np.radians(10))
point_zip = zip_point(beta_c_arr, lam_c_arr)
```

## Part 3 (concatenate cos & sin)

+ xdata_2 : sin 1x , sin 2x , ... , sin nx , cos 1x , cos 2x, ... , cos nx
```python
xdata_2 = list()
for beta_c,lam_c in point_zip:
    xdata_2.append(concat_dataset(beta_c,lam_c,steps=5))
    xdata_2 = np.array(xdata_2,dtype=np.float64)
```

## Part 4 (reshape)

```python
ans_shape = answer.shape[0]
xdata_2 = data.reshape(-1,ans_shape)
```

## Part 5 (Last)

```python
res_data_2 = np.dot(xdata_2,answer.T)
res_data_2 = res_data_2.reshape(npixel,npixel)
```

# Draw picture

```python
plt.figure(figsize=(16,9))

plt.subplot(131)
plt.title("origin")
plt.axis("off")
plt.imshow(np.array(ydata).reshape(15,14))

plt.subplot(132)
plt.title("210 point")
plt.axis("off")
res_data_1 = np.dot(xdata_1,answer.T)
plt.imshow(res_data_1.reshape(15,14))

plt.subplot(133)
plt.title("40000point")
plt.axis("off")
plt.imshow(res_data_2.reshape(200,200))

plt.show()
```
