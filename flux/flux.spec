%global debug_package %{nil}

Name: flux
Version: 2.7.5
Release: %autorelease
Summary: Open and extensible continuous delivery solution for Kubernetes. Powered by GitOps Toolkit. 
License: MIT
URL: https://github.com/fluxcd/flux2
Source0: %{url}/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
ExclusiveArch: %{go_arches}

BuildRequires: golang >= 1.25
BuildRequires: go-rpm-macros
BuildRequires: kustomize

%description
DESCRIPTION HERE

%prep
%autosetup -p1 -n flux2-%{version}

%build
export GO111MODULE=on
export CGO_ENABLED=0
LDFLAGS="-s -w -X main.VERSION=%{version}"
# Generate embedded manifests required by go:embed before building
./manifests/scripts/bundle.sh
pushd cmd/flux >/dev/null
%gobuild -ldflags "$LDFLAGS" -o %{name} .
popd >/dev/null

%install
install -Dpm 0755 cmd/flux/%{name} %{buildroot}%{_bindir}/%{name}

%check
./%{name} --version >/dev/null 2>&1 || :

%files
%doc README.md
%license LICENSE
%{_bindir}/%{name}

%changelog
%autochangelog
