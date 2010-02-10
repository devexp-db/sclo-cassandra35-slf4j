# Copyright (c) 2000-2009, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

Name:           slf4j
Version:        1.5.10
Release:        3%{?dist}
Epoch:          0
Summary:        Simple Logging Facade for Java
Group:          Development/Libraries
License:        MIT
URL:            http://www.slf4j.org/
Source0:        http://www.slf4j.org/dist/%{name}-%{version}.tar.gz
Source1:        %{name}-settings.xml
Source2:        %{name}-jpp-depmap.xml
Source3:        slf4j-component-info.xml
Patch0:         %{name}-pom_xml.patch
Patch1:         slf4j-1.5.8-skip-integration-tests.patch
Requires(post): jpackage-utils >= 0:1.7.5
Requires(postun): jpackage-utils >= 0:1.7.5
BuildRequires:  jpackage-utils >= 0:1.7.5
BuildRequires:  java-devel >= 0:1.5.0
BuildRequires:  ant >= 0:1.6.5
BuildRequires:  ant-junit >= 0:1.6.5
BuildRequires:  javassist >= 0:3.4
BuildRequires:  junit >= 0:3.8.2
BuildRequires:  maven2 >= 2.0.7
BuildRequires:  maven2-plugin-antrun
BuildRequires:  maven2-plugin-compiler
BuildRequires:  maven2-plugin-install
BuildRequires:  maven2-plugin-jar
BuildRequires:  maven2-plugin-javadoc
BuildRequires:  maven2-plugin-resources
BuildRequires:  maven2-plugin-source
BuildRequires:  maven-doxia-sitetools
BuildRequires:  maven-surefire-maven-plugin
BuildRequires:  maven-surefire-provider-junit
BuildRequires:  maven-plugin-build-helper
BuildRequires:  log4j
BuildRequires:  jakarta-commons-logging
BuildRequires:  cal10n
Requires:       jpackage-utils
Requires:       java
BuildArch:      noarch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

%description
The Simple Logging Facade for Java or (SLF4J) is intended to serve
as a simple facade for various logging APIs allowing to the end-user
to plug in the desired implementation at deployment time. SLF4J also
allows for a gradual migration path away from
Jakarta Commons Logging (JCL).

Logging API implementations can either choose to implement the
SLF4J interfaces directly, e.g. NLOG4J or SimpleLogger. Alternatively,
it is possible (and rather easy) to write SLF4J adapters for the given
API implementation, e.g. Log4jLoggerAdapter or JDK14LoggerAdapter..

%package javadoc
Group:          Documentation
Summary:        Javadoc for %{name}

%description javadoc
API documentation for %{name}.

%package manual
Group:          Documentation
Summary:        Documents for %{name}

%description manual
Manual for %{name}.

%prep
%setup -q
%patch0 -p0  -b .sav
%patch1 -p1
find . -name "*.jar" | xargs rm
cp -p %{SOURCE1} settings.xml

sed -i -e "s|<url>__JPP_URL_PLACEHOLDER__</url>|<url>file://`pwd`/.m2/repository</url>|g" \
    settings.xml
sed -i -e "s|<url>__JAVADIR_PLACEHOLDER__</url>|<url>file://`pwd`/external_repo</url>|g" \
    settings.xml
sed -i -e "s|<url>__MAVENREPO_DIR_PLACEHOLDER__</url>|<url>file://`pwd`/.m2/repository</url>|g" \
    settings.xml
sed -i -e "s|<url>__MAVENDIR_PLUGIN_PLACEHOLDER__</url>|<url>file:///usr/share/maven2/plugins</url>|g" \
    settings.xml
sed -i -e "s|<url>__ECLIPSEDIR_PLUGIN_PLACEHOLDER__</url>|<url>file:///usr/share/eclipse/plugins</url>|g" \
    settings.xml

mkdir external_repo
ln -s %{_javadir} external_repo/JPP

export MAVEN_REPO_LOCAL=$(pwd)/.m2/repository
mkdir -p $MAVEN_REPO_LOCAL/org.slf4j
ln -sf $(build-classpath maven2/empty-dep) \
  $MAVEN_REPO_LOCAL/org.slf4j/slf4j-api.jar
ln -sf $(build-classpath maven2/empty-dep) \
  $MAVEN_REPO_LOCAL/org.slf4j/slf4j-simple.jar
ln -sf $(build-classpath maven2/empty-dep) \
  $MAVEN_REPO_LOCAL/org.slf4j/slf4j-log4j12.jar
ln -sf $(build-classpath maven2/empty-dep) \
  $MAVEN_REPO_LOCAL/org.slf4j/slf4j-nop.jar

%{_bindir}/find -name "*.css" -o -name "*.js" -o -name "*.txt" | \
    %{_bindir}/xargs -t %{__perl} -pi -e 's/\r$//g'

%build
export MAVEN_REPO_LOCAL=$(pwd)/.m2/repository
mvn-jpp \
        -e \
        -s $(pwd)/settings.xml \
        -P skipTests \
        -Dmaven2.jpp.mode=true \
        -Dmaven2.jpp.depmap.file=%{SOURCE2} \
        -Dmaven.repo.local=$MAVEN_REPO_LOCAL \
        -Dmaven.test.skip=true \
        install javadoc:javadoc

%install
rm -rf $RPM_BUILD_ROOT

# jars
install -d -m 0755 $RPM_BUILD_ROOT%{_javadir}/%{name}

#install -m 644 jcl104-over-slf4j/target/jcl104-over-slf4j-%{version}.jar
#  $RPM_BUILD_ROOT%{_javadir}/%{name}/jcl104-over-slf4j-%{version}.jar
ln -sf jcl-over-slf4j-%{version}.jar \
   $RPM_BUILD_ROOT%{_javadir}/%{name}/jcl104-over-slf4j-%{version}.jar
install -m 644 jcl-over-slf4j/target/jcl-over-slf4j-%{version}.jar \
   $RPM_BUILD_ROOT%{_javadir}/%{name}/jcl-over-slf4j-%{version}.jar
install -m 644 jul-to-slf4j/target/jul-to-slf4j-%{version}.jar \
   $RPM_BUILD_ROOT%{_javadir}/%{name}/jul-to-slf4j-%{version}.jar
install -m 644 log4j-over-slf4j/target/log4j-over-slf4j-%{version}.jar \
   $RPM_BUILD_ROOT%{_javadir}/%{name}/log4j-over-slf4j-%{version}.jar
install -m 644 slf4j-api/target/%{name}-api-%{version}.jar \
   $RPM_BUILD_ROOT%{_javadir}/%{name}/api-%{version}.jar
install -m 644 slf4j-api/target/%{name}-api-%{version}-tests.jar \
   $RPM_BUILD_ROOT%{_javadir}/%{name}/api-tests-%{version}.jar
install -m 644 slf4j-ext/target/%{name}-ext-%{version}.jar \
   $RPM_BUILD_ROOT%{_javadir}/%{name}/ext-%{version}.jar
install -m 644 slf4j-jcl/target/%{name}-jcl-%{version}.jar \
   $RPM_BUILD_ROOT%{_javadir}/%{name}/jcl-%{version}.jar
install -m 644 slf4j-jdk14/target/%{name}-jdk14-%{version}.jar \
   $RPM_BUILD_ROOT%{_javadir}/%{name}/jdk14-%{version}.jar
install -m 644 slf4j-log4j12/target/%{name}-log4j12-%{version}.jar \
   $RPM_BUILD_ROOT%{_javadir}/%{name}/log4j12-%{version}.jar
install -m 644 slf4j-migrator/target/%{name}-migrator-%{version}.jar \
   $RPM_BUILD_ROOT%{_javadir}/%{name}/migrator-%{version}.jar
install -m 644 slf4j-nop/target/%{name}-nop-%{version}.jar \
   $RPM_BUILD_ROOT%{_javadir}/%{name}/nop-%{version}.jar
install -m 644 slf4j-simple/target/%{name}-simple-%{version}.jar \
   $RPM_BUILD_ROOT%{_javadir}/%{name}/simple-%{version}.jar

(cd $RPM_BUILD_ROOT%{_javadir}/%{name} && for jar in *-%{version}*; \
    do ln -sf ${jar} `echo $jar| sed "s|-%{version}||g"`; done)

%add_to_maven_depmap org.slf4j jcl104-over-slf4j %{version} JPP/slf4j jcl104-over-slf4j
%add_to_maven_depmap org.slf4j jcl-over-slf4j %{version} JPP/slf4j jcl-over-slf4j
%add_to_maven_depmap org.slf4j jul-to-slf4j %{version} JPP/slf4j jul-to-slf4j
%add_to_maven_depmap org.slf4j log4j-over-slf4j %{version} JPP/slf4j log4j-over-slf4j
%add_to_maven_depmap org.slf4j %{name}-parent %{version} JPP/slf4j parent
%add_to_maven_depmap org.slf4j %{name}-api %{version} JPP/slf4j api
%add_to_maven_depmap org.slf4j %{name}-ext %{version} JPP/slf4j ext
%add_to_maven_depmap org.slf4j %{name}-jcl %{version} JPP/slf4j jcl
%add_to_maven_depmap org.slf4j %{name}-jdk14 %{version} JPP/slf4j jdk14
%add_to_maven_depmap org.slf4j %{name}-log4j12 %{version} JPP/slf4j log4j12
%add_to_maven_depmap org.slf4j %{name}-migrator %{version} JPP/slf4j migrator
%add_to_maven_depmap org.slf4j %{name}-nop %{version} JPP/slf4j nop
%add_to_maven_depmap org.slf4j %{name}-simple %{version} JPP/slf4j simple

# poms
install -d -m 755 $RPM_BUILD_ROOT%{_datadir}/maven2/poms
install -pm 644 pom.xml \
    $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.%{name}-parent.pom
install -pm 644 jcl104-over-slf4j/pom.xml \
    $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.%{name}-jcl104-over-slf4j.pom
install -pm 644 jcl-over-slf4j/pom.xml \
    $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.%{name}-jcl-over-slf4j.pom
install -pm 644 jul-to-slf4j/pom.xml \
    $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.%{name}-jul-to-slf4j.pom
install -pm 644 log4j-over-slf4j/pom.xml \
    $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.%{name}-log4j-over-slf4j.pom
install -pm 644 slf4j-api/pom.xml \
    $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.%{name}-api.pom
install -pm 644 slf4j-ext/pom.xml \
    $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.%{name}-ext.pom
install -pm 644 slf4j-jcl/pom.xml \
    $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.%{name}-jcl.pom
install -pm 644 slf4j-jdk14/pom.xml \
    $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.%{name}-jdk14.pom
install -pm 644 slf4j-log4j12/pom.xml \
    $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.%{name}-log4j12.pom
install -pm 644 slf4j-migrator/pom.xml \
    $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.%{name}-migrator.pom
install -pm 644 slf4j-nop/pom.xml \
    $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.%{name}-nop.pom
install -pm 644 slf4j-simple/pom.xml \
    $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.%{name}-simple.pom

# javadoc
install -d -m 0755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr target/site/api*/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}/
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name}
rm -rf target/site/api*

# manual
install -d -m 0755 $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}
rm -f target/site/.htaccess
cp -pr target/site $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/
install -m 644 LICENSE.txt $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_maven_depmap

%postun
%update_maven_depmap

%files
%defattr(-,root,root,-)
%dir %{_docdir}/%{name}-%{version}
%doc %{_docdir}/%{name}-%{version}/LICENSE.txt
%{_javadir}/%{name}
%{_datadir}/maven2/poms/*
%{_mavendepmapfragdir}/*

%files javadoc
%defattr(-,root,root,-)
%{_javadocdir}/%{maven-plugin-build-helpername}-%{version}
%{_javadocdir}/%{name}

%files manual
%defattr(-,root,root,-)
%{_docdir}/%{name}-%{version}/site

%changelog
* Wed Feb 10 2010 Alexander Kurtakov <akurtako@redhat.com> 0:1.5.10-3
- BR maven-plugin-build-helper.

* Wed Feb 10 2010 Alexander Kurtakov <akurtako@redhat.com> 0:1.5.10-2
- BR cal10n.

* Wed Feb 10 2010 Alexander Kurtakov <akurtako@redhat.com> 0:1.5.10-1
- Update to upstream 1.5.10.

* Fri Sep 4 2009 Alexander Kurtakov <akurtako@redhat.com> 0:1.5.8-5
- Skip tests.

* Wed Sep 2 2009 Alexander Kurtakov <akurtako@redhat.com> 0:1.5.8-4
- Fix other line lenghts.

* Wed Sep 2 2009 Alexander Kurtakov <akurtako@redhat.com> 0:1.5.8-3
- Fix permissions.
- Fixed descriptions.
- Fix file lengths.

* Wed Sep 2 2009 Alexander Kurtakov <akurtako@redhat.com> 0:1.5.8-2
- Adapt for Fedora.

* Wed Jul 29 2009 Yong Yang <yyang@redhat.com> 0:1.5.8-1
- 1.5.8
- Replace slf4j-1.5.6-integration-tests-current-only.patch with
  slf4j-1.5.8-skip-integration-tests.patch because of the failure of "testMatch"

* Fri Jun 12 2009 Ralph Apel <r.apel at r-apel.de> 0:1.5.6-2
- Add -ext jar, depmap and pom
- Save jcl104-over-slf4j as symlink

* Tue Feb 18 2009 David Walluck <dwalluck@redhat.com> 0:1.5.6-1
- 1.5.6
- add repolib
- fix file eol
- fix Release tag

* Fri Jul 18 2008 David Walluck <dwalluck@redhat.com> 0:1.5.2-2
- use excalibur for avalon
- remove javadoc scriptlets
- GCJ fixes
- fix maven directory ownership
- fix -bc --short-circuit by moving some of %%build to %%prep

* Sun Jul 06 2008 Ralph Apel <r.apel at r-apel.de> 0:1.5.2-1.jpp5
- 1.5.2

* Mon Feb 04 2008 Ralph Apel <r.apel at r-apel.de> 0:1.4.2-2jpp
- Fix macro misprint
- Add maven2-plugin BRs

* Wed Jul 18 2007 Ralph Apel <r.apel at r-apel.de> 0:1.4.2-1jpp
- Upgrade to 1.4.2
- Build with maven2
- Add poms and depmap frags
- Add gcj_support option

* Mon Jan 30 2006 Ralph Apel <r.apel at r-apel.de> 0:1.0-0.rc5.1jpp
- First JPackage release.
