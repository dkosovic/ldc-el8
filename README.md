### Building on Fedora Copr

Select **Custom** for the source type.

Copy and paste the following script into the custom script text box:

```sh
#! /bin/sh

set -x # verbose output
set -e # fail the whole script if some command fails
                 
git clone https://github.com/dkosovic/ldc-el8.git
mv ldc-el8/* .
rm -rf ldc-el8

version=`grep Version: ldc.spec | awk '{ print $2 }'`
source=`grep Source0: ldc.spec | awk '{print $2}' | sed "s/%{version}/$version/g"`

curl -OL $source
```

Copy and paste the following into the build dependencies field:
```
git
bash-completion
cmake
gcc
gcc-c++
ldc
libconfig-devel
libcurl-devel
libedit-devel
llvm-devel
llvm-static
make
zlib-devel
```
