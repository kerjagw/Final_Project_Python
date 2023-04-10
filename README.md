# Get_District
Script Berisi Code Untuk Menampilkan Map District Sesuai Kriteria Veronica

Struktur Script
|_district.yaml
|_main.py
|_readme.md
|_/output

Prerequisites
Instalasi dan Running Script
1. File.yaml Berisi Package
name: package
dependencies:
  - python
  - numpy
  - matplotlib
  - spyder
  - owslib
  - gdal
  - geopandas
  - rasterio
  - rasterstats
  - affine
  - osmnx
  - shapely
  - pandas
  - fiona
  - folium
  - contextily
  - os
2. Conda Evironment
mamba env create --file name.yaml

// initial configuration (only take one time)
conda config --add channels conda-forge
conda install mamba

conda activate name
3. Python (Miniconda)
sudo apt-get update
sudo apt-get install wget

wget https://repo.anaconda.com/miniconda/Miniconda3-py39_4.10.3-Linux-x86_64.sh

bash Miniconda3-py39_4.10.3-Linux-x86_64.sh
  
Running File
Pada Directory Buka Terminal
conda activate folder
spyder

Built With
- Miniconda 
- Ubuntu Linux

Authors
Rizki Gilang Wijaya
rizkigilangwijaya@gmail.com
