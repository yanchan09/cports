pkgname = "curl"
pkgver = "7.84.0"
pkgrel = 0
build_style = "gnu_configure"
configure_args = [
    "--enable-threaded-resolver",
    "--enable-ipv6",
    "--with-libssh2",
    "--with-ssl",
    "--with-zstd",
    "--with-ca-bundle=/etc/ssl/certs/ca-certificates.crt",
    "ac_cv_path_NROFF=/usr/bin/mandoc",
    "ac_cv_sizeof_off_t=8",
]
make_check_env = {"USER": "nobody"}
hostmakedepends = ["pkgconf", "perl", "mandoc"]
makedepends = [
    "nghttp2-devel", "zlib-devel", "libzstd-devel",
    "openssl-devel", "libssh2-devel"
]
checkdepends = ["python", "nghttp2"]
depends = ["ca-certificates"]
pkgdesc = "Command line tool for transferring data with URL syntax"
maintainer = "q66 <q66@chimera-linux.org>"
license = "MIT"
url = "https://curl.haxx.se"
source = f"{url}/download/{pkgname}-{pkgver}.tar.bz2"
sha256 = "702fb26e73190a3bd77071aa146f507b9817cc4dfce218d2ab87f00cd3bc059d"
# missing some checkdepends
options = ["!check"]

def post_install(self):
    self.install_license("COPYING")

    # patch curl-config for cross
    if not self.profile().cross:
        return

    with open(self.destdir / "usr/bin/curl-config") as inf:
        with open(self.destdir / "usr/bin/curl-config.new", "w") as outf:
            for l in inf:
                l = l.replace(f"-L{self.profile().sysroot / 'usr/lib'} ", "")
                l = l.replace(f"{self.profile().triplet}-", "")
                outf.write(l)

    self.rm(self.destdir / "usr/bin/curl-config")
    self.mv(
        self.destdir / "usr/bin/curl-config.new",
        self.destdir / "usr/bin/curl-config"
    )
    self.chmod(self.destdir / "usr/bin/curl-config", 0o755)

@subpackage("libcurl")
def _libcurl(self):
    self.pkgdesc = "Multiprotocol file transfer library"

    return self.default_libs()

@subpackage("libcurl-devel")
def _devel(self):
    self.depends += makedepends
    self.pkgdesc = "Multiprotocol file transfer library (development files)"

    return self.default_devel()
