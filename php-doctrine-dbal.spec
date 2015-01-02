#
# RPM spec file for php-doctrine-dbal
#
# Copyright (c) 2013-2015 Shawn Iwinski <shawn.iwinski@gmail.com>
#                         Adam Williamson <awilliam@redhat.com>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global github_owner     doctrine
%global github_name      dbal
# Additional commits after v2.5.0 tag. Using version 2.5.1 pre-release because
#   lib/Doctrine/DBAL/Version.php::VERSION = 2.5.1-DEV
%global github_version   2.5.1
%global github_commit    185b886e57e9557c4fad7a39d118000f652b72de
%global github_release   .20150101git%(c=%{github_commit}; echo ${c:0:7})

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

%{!?phpdir:     %global phpdir     %{_datadir}/php}
%{!?__phpunit:  %global __phpunit  %{_bindir}/phpunit}

# Build using "--without tests" to disable tests
%global with_tests %{?_without_tests:0}%{!?_without_tests:1}

Name:          php-%{composer_vendor}-%{composer_project}
Version:       %{github_version}
Release:       0.2%{?github_release}%{?dist}
Summary:       Doctrine Database Abstraction Layer (DBAL)

Group:         Development/Libraries
License:       MIT
URL:           http://www.doctrine-project.org/projects/dbal.html

# Run "php-doctrine-dbal-get-source.sh" to create source
Source0:       %{name}-%{version}-%{github_commit}.tar.gz
Source1:       %{name}-get-source.sh

# Update bin script:
# 1) Add she-bang
# 2) Auto-load using Doctrine\Common\ClassLoader
Patch0:        %{name}-bin.patch

BuildArch: noarch
%if %{with_tests}
BuildRequires: php-phpunit-PHPUnit
# composer.json
BuildRequires: php(language)                 >= %{php_min_ver}
BuildRequires: php-composer(doctrine/common) >= %{doctrine_common_min_ver}
BuildRequires: php-composer(doctrine/common) <  %{doctrine_common_max_ver}
# composer.json (optional)
BuildRequires: php-symfony-console           >= %{symfony_console_min_ver}
BuildRequires: php-symfony-console           <  %{symfony_console_max_ver}
# phpcompatinfo (computed from version 2.5.1 commit 185b886e57e9557c4fad7a39d118000f652b72de)
BuildRequires: php-date
BuildRequires: php-json
BuildRequires: php-pcre
BuildRequires: php-pdo
BuildRequires: php-reflection
BuildRequires: php-spl
%endif

# composer.json
Requires:      php(language)                 >= %{php_min_ver}
Requires:      php-composer(doctrine/common) >= %{doctrine_common_min_ver}
Requires:      php-composer(doctrine/common) <  %{doctrine_common_max_ver}
# composer.json (optional)
Requires:      php-symfony-console           >= %{symfony_console_min_ver}
Requires:      php-symfony-console           <  %{symfony_console_max_ver}
# phpcompatinfo (computed from version 2.5.1 commit 185b886e57e9557c4fad7a39d118000f652b72de)
Requires:      php-date
Requires:      php-json
Requires:      php-pcre
Requires:      php-pdo
Requires:      php-reflection
Requires:      php-spl

# Composer
Provides:      php-composer(%{composer_vendor}/%{composer_project}) = %{version}
# PEAR
Provides:      php-pear(pear.doctrine-project.org/DoctrineDBAL) = %{version}
# Rename
Obsoletes:     php-doctrine-DoctrineDBAL < %{version}
Provides:      php-doctrine-DoctrineDBAL = %{version}

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

# Patch bin script
%patch0 -p1

# Remove empty file
rm -f lib/Doctrine/DBAL/README.markdown


%build
# Empty build section, nothing required


%install
mkdir -p %{buildroot}/%{phpdir}
cp -rp lib/Doctrine %{buildroot}/%{phpdir}/

mkdir -p %{buildroot}/%{_bindir}
install -pm 0755 bin/doctrine-dbal.php %{buildroot}/%{_bindir}/doctrine-dbal


%check
%if %{with_tests}
# Rewrite "tests/Doctrine/Tests/TestInit.php"
mv tests/Doctrine/Tests/TestInit.php tests/Doctrine/Tests/TestInit.php.dist
cat > tests/Doctrine/Tests/TestInit.php <<'TEST_INIT'
<?php

spl_autoload_register(function ($class) {
    $src = str_replace('\\', '/', $class).'.php';
    @include_once $src;
});
TEST_INIT

%{__phpunit} --include-path %{buildroot}%{phpdir}:./tests
%else
: Tests skipped
%endif


%files
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc *.md composer.json
%{phpdir}/Doctrine/DBAL
%{_bindir}/doctrine-dbal


%changelog
* Fri Jan 02 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 2.5.1-0.2.20150101git185b886
- Updated to latest snapshot
- Fixed bin script
- Added tests

* Tue Dec 30 2014 Adam Williamson <awilliam@redhat.com> - 2.5.1-0.1.20141230gitdd4d106
- bump to 2.5 branch (with latest fixes, some of which look big; BZ #1153987)

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
