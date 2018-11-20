import os
import shutil

from conans import ConanFile,tools,AutoToolsBuildEnvironment

class MuslConan(ConanFile):
    settings= "compiler","arch","build_type","os"
    name = "musl"
    version = "v1.1.18"
    license = 'MIT'

    description = 'musl - an implementation of the standard library for Linux-based systems'
    url = "https://www.musl-libc.org/"
    exports_sources=['../../../etc*musl*musl.patch', '../../../etc*musl*endian.patch','../../../api*syscalls.h','../../../etc*musl*syscall.h']

    def build_requirements(self):
        self.build_requires("binutils/2.31@%s/%s"%(self.user,self.channel))

    def imports(self):
        self.copy("*",dst=".",src=".")

    def source(self):
        git = tools.Git(folder="musl")
        git.clone("git://git.musl-libc.org/musl/",branch=self.version)

        # Replace syscall API's
        tools.patch(base_path="musl",patch_file="etc/musl/musl.patch")
        tools.patch(base_path="musl",patch_file="etc/musl/endian.patch")
        shutil.copy("api/syscalls.h","musl/src/internal/includeos_syscalls.h")
        shutil.copy("etc/musl/syscall.h","musl/src/internal")
        os.unlink("musl/arch/x86_64/syscall_arch.h")
        os.unlink("musl/arch/i386/syscall_arch.h")

    def build(self):
        triple = str(self.settings.arch)+"-elf"
        env_build = AutoToolsBuildEnvironment(self)
        env_build.configure(configure_dir=self.source_folder+"/musl",target=triple,args=["--enable-debug","--disable-shared"]) #what goes in here preferably
        env_build.make()
        env_build.install()

    def package(self):
        self.copy("*.h",dst="include",src="musl/include")
        self.copy("*.a",dst="lib",src="lib")
        self.copy("*.o",dst="lib",src="lib")

    def deploy(self):
        self.copy("*.h",dst="include/musl",src="include")
        self.copy("*.a",dst="lib",src="lib")
        self.copy("*.o",dst="lib",src="lib")