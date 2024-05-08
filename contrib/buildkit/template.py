pkgname = "buildkit"
pkgver = "0.13.2"
pkgrel = 1
build_style = "go"
make_build_args = ["./cmd/..."]
hostmakedepends = ["go"]
depends = ["containerd"]
pkgdesc = "Concurrent, cache-efficient, and Dockerfile-agnostic builder toolkit"
maintainer = "psykose <alice@ayaya.dev>"
license = "Apache-2.0"
url = "https://github.com/moby/buildkit"
source = f"https://github.com/moby/buildkit/archive/refs/tags/v{pkgver}.tar.gz"
sha256 = "e680efb849d809baa9294a9de8cf125f0884e17bd7ab6ee26bedff4b2be34bbb"
# debug: objcopy ppc64
# check: cannot work in bwrap
options = ["!debug", "!check"]


def post_extract(self):
    # delete stray incomplete vendor dir
    self.rm("vendor/", recursive=True)


def post_install(self):
    self.install_dir("var/lib/buildkit", empty=True)
    self.install_service(self.files_path / "buildkitd")
