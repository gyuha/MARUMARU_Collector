from cx_Freeze import setup, Executable
import sys

buildOptions = dict(packages = 
	[
        "bs4",
        "glob",
        "idna",
        "img2pdf",
        "multiprocessing", 
        "os",
        "re",
        "requests",
        "selenium", 
        "sys",
        "urllib",
        "zipfile" 
    ], 
	excludes = [])
exe = [Executable("mmc.py")]

setup(
    name='MARUMARU_Collector',
    version = '0.1',
    author = "IML",
    description = 'MARUMARU Web Crawler',
    options = dict(build_exe = buildOptions),
    executables = exe
)
