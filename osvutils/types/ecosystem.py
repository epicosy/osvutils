from enum import Enum

from typing import Optional
from pydantic import BaseModel


class EcosystemType(Enum):
    """
        See https://google.github.io/osv.dev/data/#covered-ecosystems
    """
    ALMALINUX = 'AlmaLinux'
    ALPINE = 'Alpine'
    ANDROID = 'Android'
    BIOCONDUCTOR = 'Bioconductor'
    BITNAMI = 'Bitnami'
    CHAINGUARD = 'Chainguard'
    CONAN_CENTER = 'Conan Center'
    CRAN = 'CRAN'
    CRATES = 'crates.io'
    DEBIAN = 'Debian'
    GHC = 'GHC'
    GIT = 'GIT'
    GITHUB_ACTIONS = 'GitHub Actions'
    GO = 'Go'
    HACKAGE = 'Hackage'
    HEX = 'Hex'
    LINUX = 'Linux'
    MAGEIA = 'Mageia'
    MAVEN = 'Maven'
    NPM = 'npm'
    NUGET = 'NuGet'
    OSS_FUZZ = 'OSS-Fuzz'
    OPENSUSE = 'openSUSE'
    PACKAGIST = 'Packagist'
    PHOTON_OS = 'Photon OS'
    PUB = 'Pub'
    PYPI = 'PyPI'
    RED_HAT = 'Red Hat'
    ROCKY_LINUX = 'Rocky Linux'
    RUBYGEMS = 'RubyGems'
    SUSE = 'SUSE'
    SWIFTURL = 'SwiftURL'
    UBUNTU = 'Ubuntu'


# Ecosystem model to store ecosystem and version separately
class Ecosystem(BaseModel):
    ecosystem: EcosystemType
    version: Optional[str] = None  # Version is optional
