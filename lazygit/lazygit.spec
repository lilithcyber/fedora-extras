%global debug_package %{nil}

Name: lazygit
Version: 0.56.0
Release: %autorelease
Summary: Simple terminal UI for Git commands
License: MIT
URL: https://github.com/jesseduffield/lazygit
Source0: %{url}/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
ExclusiveArch: %{go_arches}

BuildRequires: golang >= 1.25
BuildRequires: go-rpm-macros

%description
Lazygit is a simple terminal UI for Git commands, written in Go. It provides an intuitive interface for managing Git repositories from the command line.

%prep
%autosetup -p1

%build
export GO111MODULE=on
export CGO_ENABLED=0
LDFLAGS="-s -w -X main.version=%{version} -X main.date=$(date -u +%%Y-%%m-%%dT%%H:%%M:%%SZ) -X main.buildSource=binaryRelease"
%gobuild -ldflags "$LDFLAGS" -o %{name}

%install
install -Dpm 0755 %{name} %{buildroot}%{_bindir}/%{name}

%check
./%{name} --version >/dev/null 2>&1 || :

%files
%doc README.md
%license LICENSE
%{_bindir}/%{name}

%changelog
%autochangelog
