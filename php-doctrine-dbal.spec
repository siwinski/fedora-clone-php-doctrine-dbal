#
# RPM spec file for php-doctrine-dbal
#
# Copyright (c) 2013-2014 Shawn Iwinski <shawn.iwinski@gmail.com>
#                         Adam Williamson <awilliam@redhat.com>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global github_owner     doctrine
%global github_name      dbal
# yes, upstream messed up their commit: the commit tagged with the 2.5.0
# release tag is the one that bumps the version to 2.5.1.
%global github_version   2.5.1
%global github_date      20141230
%global github_commit    dd4d1062ccd5018ee7f2bb05a54258dc839d7b1e
%global shortcommit %(c=%{github_commit}; echo ${c:0:7})

%global composer_vendor  doctrine
%global composer_project dbal

# "php": ">=5.3.2"
%global php_min_ver             5.3.2
# "doctrine/common": ">=2.4,<2.6-dev"
%global doctrine_common_min_ver 2.4
%global doctrine_common_max_ver 2.6
# "symfony/console": "2.*"
%global symfony_console_min_ver 2.0
%global symfony_console_max_ver 3.0

Name:      php-%{composer_vendor}-%{composer_project}
Version:   %{github_version}
Release:   0.1.%{github_date}git%{shortcommit}%{?dist}
Summary:   Doctrine Database Abstraction Layer (DBAL)

Group:     Development/Libraries
License:   MIT
URL:       http://www.doctrine-project.org/projects/dbal.html
Source0:   https://github.com/%{github_owner}/%{github_name}/archive/%{github_commit}/%{name}-%{github_version}-%{github_commit}.tar.gz

BuildArch: noarch

Requires:  php(language)                 >= %{php_min_ver}
Requires:  php-composer(doctrine/common) >= %{doctrine_common_min_ver}
Requires:  php-composer(doctrine/common) <  %{doctrine_common_max_ver}
Requires:  php-symfony-console           >= %{symfony_console_min_ver}
Requires:  php-symfony-console           <  %{symfony_console_max_ver}
# phpcompatinfo (computed from v2.4.2)
Requires:  php-date
Requires:  php-json
Requires:  php-pcre
Requires:  php-pdo
Requires:  php-spl

# Composer
Provides:  php-composer(%{composer_vendor}/%{composer_project}) = %{version}
# PEAR
Provides:  php-pear(pear.doctrine-project.org/DoctrineDBAL) = %{version}
# Rename
Obsoletes: php-doctrine-DoctrineDBAL < %{version}
Provides:  php-doctrine-DoctrineDBAL = %{version}

%description
The Doctrine database abstraction & access layer (DBAL) offers a lightweight
and thin runtime layer around a PDO-like API and a lot of additional, horizontal
features like database schema introspection and manipulation through an OO API.

The fact that the Doctrine DBAL abstracts the concrete PDO API away through the
use of interfaces that closely resemble the existing PDO API makes it possible
to implement custom drivers that may use existing native or self-made APIs. For
example, the DBAL ships with a driver for Oracle databases that uses the oci8
extension under the hood.


%prep
%setup -qn %{github_name}-%{github_commit}

# Make a single executable
echo '#!%{_bindir}/php' > bin/doctrine-dbal
sed 's#Doctrine/Common/ClassLoader.php#%{_datadir}/php/Doctrine/Common/ClassLoader.php#' \
    bin/doctrine-dbal.php >> bin/doctrine-dbal

# Remove empty file
rm -f lib/Doctrine/DBAL/README.markdown

# Remove executable bits
chmod a-x \
    lib/Doctrine/DBAL/Types/JsonArrayType.php \
    lib/Doctrine/DBAL/Types/SimpleArrayType.php


%build
# Empty build section, nothing required


%install
mkdir -p %{buildroot}/%{_datadir}/php
cp -rp lib/Doctrine %{buildroot}/%{_datadir}/php/

mkdir -p %{buildroot}/%{_bindir}
install -pm 0755 bin/doctrine-dbal %{buildroot}/%{_bindir}/


%check
# Upstream drops tests from distribution tarballs:
# https://github.com/doctrine/doctrine2/pull/543


%files
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc *.md composer.json
%{_datadir}/php/Doctrine/DBAL
%{_bindir}/doctrine-dbal


%changelog
* Tue Dec 30 2014 Adam Williamson <awilliam@redhat.com> - 2.5.1-0.1.20141230gitdd4d106
- bump to 2.5 branch (with latest fixes, some of which look big)

* Tue Jul 29 2014 Adam Williamson <awilliam@redhat.com> - 2.4.2-6
- really apply the patch

* Tue Jul 29 2014 Adam Williamson <awilliam@redhat.com> - 2.4.2-5
- backport another OwnCloud-related pgsql fix from upstream master

* Fri Jun 20 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 2.4.2-4
- Added php-composer(%%{composer_vendor}/%%{composer_project}) virtual provide
- Updated Doctrine dependencies to use php-composer virtual provides

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Jan 07 2014 Adam Williamson <awilliam@redhat.com> - 2.4.2-2
- primary_index: one OwnCloud patch still isn't in upstream

* Sat Jan 04 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 2.4.2-1
- Updated to 2.4.2
- Conditional %%{?dist}

* Tue Dec 31 2013 Shawn Iwinski <shawn.iwinski@gmail.com> - 2.4.1-2.20131231gitd08b11c
- Updated to latest snapshot
- Removed patches (pulled into latest snapshot)

* Sun Dec 29 2013 Shawn Iwinski <shawn.iwinski@gmail.com> - 2.4.1-1
- Initial package
