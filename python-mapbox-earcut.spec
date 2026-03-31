%global debug_package %{nil}
%define module mapbox-earcut
%define oname mapbox_earcut
%bcond tests 1

Name:		python-mapbox-earcut
Version:	2.0.0
Release:	1
Summary:	Python bindings for the mapbox earcut C++ polygon triangulation library
License:	None
Group:		Development/Python
URL:		https://pypi.org/project/mapbox-earcut/
Source0:	https://files.pythonhosted.org/packages/source/m/%{module}/%{oname}-%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildSystem:	python
BuildRequires:	cmake
BuildRequires:	ninja
BuildRequires:	dos2unix
BuildRequires:	python
BuildRequires:	pkgconfig(python3)
BuildRequires:	python%{pyver}dist(numpy)
BuildRequires:	python%{pyver}dist(nanobind)
BuildRequires:	python%{pyver}dist(scikit-build-core)
BuildRequires:	earcut-hpp-devel >= 2.2.4
BuildRequires:	earcut-hpp-static
%if %{with tests}
BuildRequires:	python%{pyver}dist(pytest)
%endif


%description
Python bindings for the mapbox earcut C++ polygon triangulation library

%prep -a
# Remove bundled earcut.hpp library as we have it packaged.
rm -rv include/mapbox

# Fix CRLF line endings.
dos2unix --keepdate README.md

%build -p
# See comments in the earcut-hpp spec file, as well as:
# https://github.com/mapbox/earcut.hpp/issues/97
# https://github.com/mapbox/earcut.hpp/issues/103
export CFLAGS="%{optflags} -ffp-contract=off"
export CXXFLAGS="%{optflags} -ffp-contract=off"

%if %{with tests}
%check
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:%{buildroot}%{_libdir}
export CI=true
export PYTHONPATH="%{buildroot}%{python_sitearch}:${PWD}"
pytest
%endif

%files
%doc README.md
%license LICENSE.md
%{python_sitearch}/%{oname}
%{python_sitearch}/%{oname}-%{version}.dist-info
