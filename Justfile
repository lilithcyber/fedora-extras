set shell := ["bash", "-c"]
mock_root := "fedora-43-x86_64"
mock_binary := shell('id -nG | grep -qw mock && echo "mock" || echo "sudo mock"')

default: list

list:
    @echo "Available packages:"
    @find . -maxdepth 2 -name "*.spec" -print0 | xargs -0 -n1 dirname | xargs -n1 basename | sort | uniq

build package:
    @echo "==> Building {{package}} using {{mock_binary}} in {{mock_root}}"
    @if [ ! -d "{{package}}" ]; then \
        echo "Error: Directory '{{package}}' does not exist"; \
        exit 1; \
    fi
    @cd {{package}} && \
    if ! ls *.spec >/dev/null 2>&1; then \
        echo "Error: No .spec file found in {{package}}"; \
        exit 1; \
    fi
    
    @echo "--> Downloading sources..."
    @cd {{package}} && spectool -g *.spec
    
    @mkdir -p {{package}}/results
    
    @echo "--> Building SRPM..."
    @cd {{package}} && {{mock_binary}} -r {{mock_root}} \
        --buildsrpm \
        --spec *.spec \
        --sources . \
        --resultdir results \
        --no-clean
        
    @echo "--> Building RPMs..."
    @cd {{package}} && {{mock_binary}} -r {{mock_root}} \
        --rebuild results/*.src.rpm \
        --resultdir results \
        --no-clean \
        --enable-network
        
    @echo "==> Build finished for {{package}}. Artifacts are in {{package}}/results"

build-all:
    @echo "==> Building all packages..."
    @find . -maxdepth 2 -name "*.spec" -print0 | xargs -0 -n1 dirname | xargs -n1 basename | sort | uniq | while read pkg; do \
        just build "$pkg"; \
    done

clean package:
    @echo "Cleaning {{package}}..."
    @rm -rf {{package}}/results

clean-all:
    @echo "Cleaning all artifacts..."
    @find . -name "results" -type d -exec rm -rf {} +
    @find . -name "*.tar.gz" -type f -exec rm -rf {} +
