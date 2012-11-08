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
Version:        1.7.2
Release:        2%{?dist}
Epoch:          0
Summary:        Simple Logging Facade for Java
Group:          Development/Libraries
# the log4j-over-slf4j and jcl-over-slf4j submodules are ASL 2.0, rest is MIT
License:        MIT and ASL 2.0
URL:            http://www.slf4j.org/
Source0:        http://www.slf4j.org/dist/%{name}-%{version}.tar.gz
Requires(post): jpackage-utils >= 0:1.7.5
Requires(postun): jpackage-utils >= 0:1.7.5
BuildRequires:  jpackage-utils >= 0:1.7.5
BuildRequires:  java-devel >= 0:1.5.0
BuildRequires:  ant >= 0:1.6.5
BuildRequires:  ant-junit >= 0:1.6.5
BuildRequires:  javassist >= 0:3.4
BuildRequires:  junit >= 0:3.8.2
BuildRequires:  maven
BuildRequires:  maven-antrun-plugin
BuildRequires:  maven-compiler-plugin
BuildRequires:  maven-install-plugin
BuildRequires:  maven-jar-plugin
BuildRequires:  maven-javadoc-plugin
BuildRequires:  maven-resources-plugin
BuildRequires:  maven-source-plugin
BuildRequires:  maven-site-plugin
BuildRequires:  maven-doxia-sitetools
BuildRequires:  maven-surefire-plugin
BuildRequires:  maven-surefire-provider-junit
BuildRequires:  maven-plugin-build-helper
BuildRequires:  log4j
BuildRequires:  apache-commons-logging
BuildRequires:  cal10n
Requires:       jpackage-utils
Requires:       cal10n
Requires:       java
BuildArch:      noarch

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
Requires:       jpackage-utils
BuildRequires:  java-javadoc
Requires:       java-javadoc

%description javadoc
API documentation for %{name}.

%package manual
Group:          Documentation
Summary:        Documents for %{name}

%description manual
Manual for %{name}.

%prep
%setup -q
find . -name "*.jar" | xargs rm

%pom_disable_module integration
%pom_disable_module osgi-over-slf4j
%pom_remove_plugin :maven-source-plugin

# Because of a non-ASCII comment in slf4j-api/src/main/java/org/slf4j/helpers/MessageFormatter.java
%pom_xpath_inject "pom:project/pom:properties" "
    <project.build.sourceEncoding>ISO-8859-1</project.build.sourceEncoding>"

# Fix javadoc links
%pom_xpath_remove "pom:links"
%pom_xpath_inject "pom:plugin[pom:artifactId[text()='maven-javadoc-plugin']]/pom:configuration" "
    <detectJavaApiLink>false</detectJavaApiLink>
    <isOffline>false</isOffline>
    <links><link>/usr/share/javadoc/java</link></links>"

# dos2unix
%{_bindir}/find -name "*.css" -o -name "*.js" -o -name "*.txt" | \
    %{_bindir}/xargs -t %{__perl} -pi -e 's/\r$//g'

%build
mvn-rpmbuild \
        -P skipTests \
        -Dmaven.test.skip=true \
        install javadoc:aggregate

%install
# jars
install -d -m 0755 $RPM_BUILD_ROOT%{_javadir}/%{name}

install -m 644 jcl-over-slf4j/target/jcl-over-slf4j-%{version}.jar \
   $RPM_BUILD_ROOT%{_javadir}/%{name}/jcl-over-slf4j.jar
install -m 644 jul-to-slf4j/target/jul-to-slf4j-%{version}.jar \
   $RPM_BUILD_ROOT%{_javadir}/%{name}/jul-to-slf4j.jar
install -m 644 log4j-over-slf4j/target/log4j-over-slf4j-%{version}.jar \
   $RPM_BUILD_ROOT%{_javadir}/%{name}/log4j-over-slf4j.jar
install -m 644 slf4j-api/target/%{name}-api-%{version}.jar \
   $RPM_BUILD_ROOT%{_javadir}/%{name}/api.jar
install -m 644 slf4j-ext/target/%{name}-ext-%{version}.jar \
   $RPM_BUILD_ROOT%{_javadir}/%{name}/ext.jar
install -m 644 slf4j-jcl/target/%{name}-jcl-%{version}.jar \
   $RPM_BUILD_ROOT%{_javadir}/%{name}/jcl.jar
install -m 644 slf4j-jdk14/target/%{name}-jdk14-%{version}.jar \
   $RPM_BUILD_ROOT%{_javadir}/%{name}/jdk14.jar
install -m 644 slf4j-log4j12/target/%{name}-log4j12-%{version}.jar \
   $RPM_BUILD_ROOT%{_javadir}/%{name}/log4j12.jar
install -m 644 slf4j-migrator/target/%{name}-migrator-%{version}.jar \
   $RPM_BUILD_ROOT%{_javadir}/%{name}/migrator.jar
install -m 644 slf4j-nop/target/%{name}-nop-%{version}.jar \
   $RPM_BUILD_ROOT%{_javadir}/%{name}/nop.jar
install -m 644 slf4j-simple/target/%{name}-simple-%{version}.jar \
   $RPM_BUILD_ROOT%{_javadir}/%{name}/simple.jar

# poms
install -d -m 755 $RPM_BUILD_ROOT%{_mavenpomdir}
install -pm 644 pom.xml \
    $RPM_BUILD_ROOT%{_mavenpomdir}/JPP.%{name}-parent.pom
install -pm 644 jcl-over-slf4j/pom.xml \
    $RPM_BUILD_ROOT%{_mavenpomdir}/JPP.%{name}-jcl-over-slf4j.pom
install -pm 644 jul-to-slf4j/pom.xml \
    $RPM_BUILD_ROOT%{_mavenpomdir}/JPP.%{name}-jul-to-slf4j.pom
install -pm 644 log4j-over-slf4j/pom.xml \
    $RPM_BUILD_ROOT%{_mavenpomdir}/JPP.%{name}-log4j-over-slf4j.pom
install -pm 644 slf4j-api/pom.xml \
    $RPM_BUILD_ROOT%{_mavenpomdir}/JPP.%{name}-api.pom
install -pm 644 slf4j-ext/pom.xml \
    $RPM_BUILD_ROOT%{_mavenpomdir}/JPP.%{name}-ext.pom
install -pm 644 slf4j-jcl/pom.xml \
    $RPM_BUILD_ROOT%{_mavenpomdir}/JPP.%{name}-jcl.pom
install -pm 644 slf4j-jdk14/pom.xml \
    $RPM_BUILD_ROOT%{_mavenpomdir}/JPP.%{name}-jdk14.pom
install -pm 644 slf4j-log4j12/pom.xml \
    $RPM_BUILD_ROOT%{_mavenpomdir}/JPP.%{name}-log4j12.pom
install -pm 644 slf4j-migrator/pom.xml \
    $RPM_BUILD_ROOT%{_mavenpomdir}/JPP.%{name}-migrator.pom
install -pm 644 slf4j-nop/pom.xml \
    $RPM_BUILD_ROOT%{_mavenpomdir}/JPP.%{name}-nop.pom
install -pm 644 slf4j-simple/pom.xml \
    $RPM_BUILD_ROOT%{_mavenpomdir}/JPP.%{name}-simple.pom

%add_maven_depmap JPP.%{name}-parent.pom
%add_maven_depmap JPP.%{name}-jcl-over-slf4j.pom %{name}/jcl-over-slf4j.jar
%add_maven_depmap JPP.%{name}-jul-to-slf4j.pom %{name}/jul-to-slf4j.jar
%add_maven_depmap JPP.%{name}-log4j-over-slf4j.pom %{name}/log4j-over-slf4j.jar
%add_maven_depmap JPP.%{name}-api.pom %{name}/api.jar
%add_maven_depmap JPP.%{name}-ext.pom %{name}/ext.jar
%add_maven_depmap JPP.%{name}-jcl.pom %{name}/jcl.jar
%add_maven_depmap JPP.%{name}-jdk14.pom %{name}/jdk14.jar
%add_maven_depmap JPP.%{name}-log4j12.pom %{name}/log4j12.jar
%add_maven_depmap JPP.%{name}-migrator.pom %{name}/migrator.jar
%add_maven_depmap JPP.%{name}-nop.pom %{name}/nop.jar
%add_maven_depmap JPP.%{name}-simple.pom %{name}/simple.jar

# javadoc
install -d -m 0755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}
cp -pr target/site/api*/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}/
rm -rf target/site/api*

# manual
install -d -m 0755 $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}
rm -f target/site/.htaccess
cp -pr target/site $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/

%files -f .mfiles
%doc LICENSE.txt
%dir %{_javadir}/%{name}

%files javadoc
%{_javadocdir}/%{name}

%files manual
%{_docdir}/%{name}-%{version}/site

%changelog
* Thu Nov 08 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:1.7.2-2
- Fix license to ASL 2.0 and MIT
- Update to add_maven_depmap macro
- Use generated .mfiles list
- Small packaging cleanups

* Mon Oct 15 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.7.2-1
- Update to upstream version 1.7.2

* Mon Sep 17 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.7.1-1
- Update to upstream version 1.7.1

* Mon Sep 10 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.7.0-1
- Update to upstream version 1.7.0

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.6.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jul 11 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.6.6-1
- Update to upstream version 1.6.6
- Convert patches to POM macros

* Fri Jan 13 2012 Ville Skyttä <ville.skytta@iki.fi> - 0:1.6.1-5
- Crosslink with local JDK API docs.

* Fri Jan 13 2012 Ville Skyttä <ville.skytta@iki.fi> - 0:1.6.1-4
- Specify explicit source encoding to fix build with Java 1.7.
- Remove no longer needed javadoc dir upgrade hack.

* Wed Jun 8 2011 Alexander Kurtakov <akurtako@redhat.com> 0:1.6.1-3
- Build with maven 3.x.

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jan 25 2011 Alexander Kurtakov <akurtako@redhat.com> 0:1.6.1-1
- Update to new upstream version.
- Various guidelines fixes.

* Wed Sep 8 2010 Alexander Kurtakov <akurtako@redhat.com> 0:1.5.11-3
- Add maven-site-pugin BR.
- Use new package names.

* Wed Sep 8 2010 Alexander Kurtakov <akurtako@redhat.com> 0:1.5.11-2
- Skip installing tests jar that is no longer produced.
- Use javadoc aggregate.
- Use mavenpomdir macro.

* Thu Feb 25 2010 Alexander Kurtakov <akurtako@redhat.com> 0:1.5.11-1
- Update to 1.5.11.
- Drop depmap and component info files.

* Wed Feb 10 2010 Mary Ellen Foster <mefoster at gmail.com> 0:1.5.10-5
- Require cal10n

* Wed Feb 10 2010 Alexander Kurtakov <akurtako@redhat.com> 0:1.5.10-4
- Fix javadoc files.

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
