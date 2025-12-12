%global debug_package %{nil}
%define module mapbox_earcut
%define oname mapbox_earcut
%bcond_without tests

Name:		python-mapbox-earcut
Version:	1.0.3
Release:	2
Source0:	https://files.pythonhosted.org/packages/source/m/mapbox-earcut/%{oname}-%{version}.tar.gz
Summary:	Python bindings for the mapbox earcut C++ polygon triangulation library
URL:		https://pypi.org/project/mapbox-earcut/
License:	None
Group:		Development/Python

BuildRequires:	cmake
BuildRequires:	ninja
BuildRequires:  dos2unix
BuildRequires:	python
BuildRequires:	pkgconfig(python3)
BuildRequires:	python%{pyver}dist(numpy)
BuildRequires:	python%{pyver}dist(pybind11)
BuildRequires:	python%{pyver}dist(scikit-build-core)
BuildRequires:	earcut-hpp-devel >= 2.2.4
BuildRequires:	earcut-hpp-static
BuildRequires:	pkgconfig(pybind11)
%if %{with tests}
BuildRequires:	python%{pyver}dist(pytest)
%endif


%description
Python bindings for the mapbox earcut C++ polygon triangulation library

%prep
%autosetup -n %{oname}-%{version} -p1

# Remove git badges remote images from README
sed -i '2,3d;' README.md

# Remove bundled earcut.hpp library as we have it packaged
rm -rv include/mapbox

# Fix CRLF line endings in files that will be installed.
dos2unix --keepdate *.md

%build
# See comments in the earcut-hpp spec file, as well as:
# https://github.com/mapbox/earcut.hpp/issues/97
# https://github.com/mapbox/earcut.hpp/issues/103
export CFLAGS="${CFLAGS-} -ffp-contract=off"
export CXXFLAGS="${CXXFLAGS-} -ffp-contract=off"
%py_build

%install
%py_install

%if %{with tests}
%check
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:%{buildroot}%{_libdir}
export CI=true
export PYTHONPATH="%{buildroot}%{python_sitearch}:${PWD}"
pytest -v
%endif

%files
%{python_sitearch}/%{oname}.*.so
%{python_sitearch}/%{oname}-%{version}.dist-info
%doc README.md
%license LICENSE.md
