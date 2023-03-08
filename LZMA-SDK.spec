
Name:           LZMA-SDK
Version:        22.00
Release:        3
Summary:        SDK for lzma compression
License:        Public Domain
URL:            http://sourceforge.net/projects/sevenzip/
Source0:        https://sourceforge.net/projects/sevenzip/files/LZMA%20SDK/lzma2200.7z
BuildRequires:  gcc-c++ p7zip

%description
The LZMA SDK provides the documentation, samples, header files, libraries, and
tools you need to develop applications that use LZMA compression.

LZMA is default and general compression methods of 7z format in the 7-Zip program.
LZMA provides a high compression ratio and fast decompression, so it is very
suitable for embedded applications.

%package doc
Summary:        The help file of %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description doc
The help file of %{name}.

%package devel
Summary:        Development headers for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
 
%description devel
Development headers for %{name}.
 
%prep
%setup -q -c -n lzma2200
%define debug_package %{nil} 

for f in .c .cpp .cs .dsp .dsw .h .java .txt makefile; do
   find . -iname "*$f" | xargs chmod -x
done
 
# correct end-of-file encoding for txt files in the DOC.
sed -i 's/\r//' DOC/*.txt 
 
# The following files in lzma belong to the iso-8859-1 character set.
# They are currently converted to utf-8 character set type.
for FILE in \
DOC/7zC.txt \
DOC/7zFormat.txt \
DOC/lzma.txt \
DOC/lzma-history.txt \
DOC/Methods.txt \
C/Util/7z/makefile.gcc \
C/Util/Lzma/makefile.gcc \
C/Util/LzmaLib/LzmaLib.def \
C/Util/LzmaLib/resource.rc \
CPP/Build.mak \
CPP/7zip/MyVersionInfo.rc \
CPP/7zip/Archive/Archive.def \
CPP/7zip/Archive/Archive2.def \
CPP/7zip/Bundles/Alone7z/resource.rc \
CPP/7zip/Bundles/Format7zR/resource.rc \
CPP/7zip/Bundles/Format7zExtractR/resource.rc \
CS/7zip/Compress/LzmaAlone/LzmaAlone.sln \
CPP/7zip/Bundles/LzmaCon/makefile.gcc; do
    iconv -f iso-8859-1 -t utf-8 $FILE > $FILE.utf8
    touch -r $FILE $FILE.utf8
    mv $FILE.utf8 $FILE
done
 
%build
make -f makefile.gcc clean all CXX="g++ %{optflags} -fPIC" CXX_C="gcc %{optflags} -fPIC" LDFLAGS="%{?__global_ldflags}" -C CPP/7zip/Bundles/LzmaCon
 
%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_bindir}
install -m 0755 CPP/7zip/Bundles/LzmaCon/_o/lzma %{buildroot}%{_bindir}/LZMA-SDK
mkdir -p %{buildroot}/%{_includedir}/lzma/
find -iname '*.h' | xargs -I {} install -m 0755 -D {} %{buildroot}/%{_includedir}/lzma/{}

%files
%{_bindir}/*
 
%files devel
%{_includedir}/lzma/

%files doc
%doc DOC/7z*.txt DOC/Methods.txt DOC/lzma.txt DOC/lzma-history.txt

%changelog
* Mon Mar 06 2023 peijiankang <peijiankang@kylinos.cn> - 22.00-3
- reslove the conflict between xz-lzma-compat and LZMA-SDK

* Wed Aug 03 2022 tanjinghui1 <tanjinghui1@huawei.com> - 22.00-2
- change header file path lzma2200 to lzma

* Thu Jul 14 2022 tanjinghui1 <tanjinghui1@huawei.com> - 22.00-1
- upgrade to 22.00

* Fri May 27 2022 tanjinghui1 <tanjinghui1@h-partners.com> - 21.07-1
- upgrade to 21.07

* Fri Dec 4 2020 tangmeng5 <tangmeng5@huawei.com> - 19.00-1
- package init
