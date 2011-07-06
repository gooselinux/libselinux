%define ruby_sitearch %(ruby -rrbconfig -e "puts Config::CONFIG['sitearchdir']")
%define libsepolver 2.0.32-1
%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Summary: SELinux library and simple utilities
Name: libselinux
Version: 2.0.94
Release: 2%{?dist}
License: Public Domain
Group: System Environment/Libraries
Source: http://www.nsa.gov/research/selinux/%{name}-%{version}.tgz
Patch: libselinux-rhat.patch
Patch1: libselinux-ruby.patch
URL: http://www.selinuxproject.org

BuildRequires: python-devel ruby-devel ruby libsepol-static >= %{libsepolver} swig
Requires: libsepol >= %{libsepolver}
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
Security-enhanced Linux is a feature of the Linux® kernel and a number
of utilities with enhanced security functionality designed to add
mandatory access controls to Linux.  The Security-enhanced Linux
kernel contains new architectural components originally developed to
improve the security of the Flask operating system. These
architectural components provide general support for the enforcement
of many kinds of mandatory access control policies, including those
based on the concepts of Type Enforcement®, Role-based Access
Control, and Multi-level Security.

libselinux provides an API for SELinux applications to get and set
process and file security contexts and to obtain security policy
decisions.  Required for any applications that use the SELinux API.

%package utils
Summary: SELinux libselinux utilies
Group: Development/Libraries
Requires: libselinux = %{version}-%{release} 

%description utils
The libselinux-utils package contains the utilities

%package python
Summary: SELinux python bindings for libselinux
Group: Development/Libraries
Requires: libselinux = %{version}-%{release} 

%description python
The libselinux-python package contains the python bindings for developing 
SELinux applications. 

%package ruby
Summary: SELinux ruby bindings for libselinux
Group: Development/Libraries
Requires: libselinux = %{version}-%{release} 
Provides: ruby(selinux)

%description ruby
The libselinux-ruby package contains the ruby bindings for developing 
SELinux applications. 

%package devel
Summary: Header files and libraries used to build SELinux
Group: Development/Libraries
Requires: libselinux = %{version}-%{release} 
Requires: libsepol-devel >= %{libsepolver}

%description devel
The libselinux-devel package contains the libraries and header files
needed for developing SELinux applications. 

%package static
Summary: Static libraries used to build SELinux
Group: Development/Libraries
Requires: libselinux-devel = %{version}-%{release}

%description static
The libselinux-static package contains the static libraries
needed for developing SELinux applications. 

%prep
%setup -q
%patch -p1 -b .rhat
%patch1 -p1 -b .ruby

%build
make clean
make LIBDIR="%{_libdir}" CFLAGS="-g %{optflags}" %{?_smp_mflags} swigify
make LIBDIR="%{_libdir}" CFLAGS="-g %{optflags}" %{?_smp_mflags} all pywrap
make LIBDIR="%{_libdir}" CFLAGS="-g %{optflags}" %{?_smp_mflags} rubywrap

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/%{_lib} 
mkdir -p %{buildroot}/%{_libdir} 
mkdir -p %{buildroot}%{_includedir} 
mkdir -p %{buildroot}%{_sbindir}
mkdir -p %{buildroot}/var/run/setrans

make DESTDIR="%{buildroot}" LIBDIR="%{buildroot}%{_libdir}" SHLIBDIR="%{buildroot}/%{_lib}" BINDIR="%{buildroot}%{_sbindir}" install install-pywrap
make DESTDIR="%{buildroot}" LIBDIR="%{buildroot}%{_libdir}" SHLIBDIR="%{buildroot}/%{_lib}" BINDIR="%{buildroot}%{_sbindir}" install install-rubywrap

# Nuke the files we don't want to distribute
rm -f %{buildroot}%{_sbindir}/compute_*
rm -f %{buildroot}%{_sbindir}/deftype
rm -f %{buildroot}%{_sbindir}/execcon
rm -f %{buildroot}%{_sbindir}/getenforcemode
rm -f %{buildroot}%{_sbindir}/getfilecon
rm -f %{buildroot}%{_sbindir}/getpidcon
rm -f %{buildroot}%{_sbindir}/mkdircon
rm -f %{buildroot}%{_sbindir}/policyvers
rm -f %{buildroot}%{_sbindir}/setfilecon
rm -f %{buildroot}%{_sbindir}/selinuxconfig
rm -f %{buildroot}%{_sbindir}/selinuxdisable
rm -f %{buildroot}%{_sbindir}/getseuser
rm -f %{buildroot}%{_sbindir}/selinux_check_securetty_context
mv %{buildroot}%{_sbindir}/getdefaultcon %{buildroot}%{_sbindir}/selinuxdefcon
mv %{buildroot}%{_sbindir}/getconlist %{buildroot}%{_sbindir}/selinuxconlist

%clean
rm -rf %{buildroot}

%post
/sbin/ldconfig
exit 0

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
/%{_lib}/libselinux.so.*
/var/run/setrans
/sbin/matchpathcon

%files utils
%defattr(-,root,root,-)
%{_sbindir}/avcstat
%{_sbindir}/getenforce
%{_sbindir}/getsebool
%{_sbindir}/matchpathcon
%{_sbindir}/selinuxconlist
%{_sbindir}/selinuxdefcon
%{_sbindir}/selinuxenabled
%{_sbindir}/setenforce
%{_sbindir}/togglesebool
%{_mandir}/man5/*
%{_mandir}/man8/*

%files devel
%defattr(-,root,root,-)
%{_libdir}/libselinux.so
%{_libdir}/pkgconfig/libselinux.pc
%dir %{_includedir}/selinux
%{_includedir}/selinux/*
%{_mandir}/man3/*

%files static
%defattr(-,root,root,-)
%{_libdir}/libselinux.a

%files python
%defattr(-,root,root,-)
%dir %{python_sitearch}/selinux
%{python_sitearch}/selinux/*

%files ruby
%defattr(-,root,root,-)
%{ruby_sitearch}/selinux.so

%changelog
* Fri Aug 13 2010 Dan Walsh <dwalsh@redhat.com> - 2.0.94-2
- Add ruby patch to allow libselinux to build on RHEL6
Resolves: #558910

* Wed Mar 24 2010 Dan Walsh <dwalsh@redhat.com> - 2.0.94-1
	* Set errno=EINVAL for invalid contexts from Dan Walsh.
	* pkgconfig fix to respect LIBDIR from Dan Walsh.
Resolves: #593788

* Sun Mar 16 2010 Dan Walsh <dwalsh@redhat.com> - 2.0.93-1
- Update to upstream 
	* Show strerror for security_getenforce() by Colin Waters.
	* Merged selabel database support by KaiGai Kohei.
	* Modify netlink socket blocking code by KaiGai Kohei.

* Sun Mar 7 2010 Dan Walsh <dwalsh@redhat.com> - 2.0.92-1
- Update to upstream 
	* Fix from Eric Paris to fix leak on non-selinux systems.
	* regenerate swig wrappers
	* pkgconfig fix to respect LIBDIR from Dan Walsh.

* Wed Feb 24 2010 Dan Walsh <dwalsh@redhat.com> - 2.0.91-1
- Update to upstream 
	* Change the AVC to only audit the permissions specified by the
	policy, excluding any permissions specified via dontaudit or not
	specified via auditallow.
	* Fix compilation of label_file.c with latest glibc headers.

* Mon Feb 22 2010 Dan Walsh <dwalsh@redhat.com> - 2.0.90-5
- Fix potential doublefree on init

* Thu Feb 18 2010 Dan Walsh <dwalsh@redhat.com> - 2.0.90-4
- Fix libselinux.pc

* Mon Jan 18 2010 Dan Walsh <dwalsh@redhat.com> - 2.0.90-3
- Fix man page for selinuxdefcon

* Mon Jan 4 2010 Dan Walsh <dwalsh@redhat.com> - 2.0.90-2
- Free memory on disabled selinux boxes

* Tue Dec 1 2009 Dan Walsh <dwalsh@redhat.com> - 2.0.90-1
- Update to upstream 
	* add/reformat man pages by Guido Trentalancia <guido@trentalancia.com>.
	* Change exception.sh to be called with bash by Manoj Srivastava <srivasta@debian.org>

* Mon Nov 2 2009 Dan Walsh <dwalsh@redhat.com> - 2.0.89-2
- Fix selinuxdefcon man page

* Mon Nov 2 2009 Dan Walsh <dwalsh@redhat.com> - 2.0.89-1
- Update to upstream 
	* Add pkgconfig file from Eamon Walsh.

* Thu Oct 29 2009 Dan Walsh <dwalsh@redhat.com> - 2.0.88-1
- Update to upstream 
	* Rename and export selinux_reset_config()

* Tue Sep 8 2009 Dan Walsh <dwalsh@redhat.com> - 2.0.87-1
- Update to upstream 
	* Add exception handling in libselinux from Dan Walsh. This uses a
	  shell script called exception.sh to generate a swig interface file.
	* make swigify
	* Make matchpathcon print <<none>> if path not found in fcontext file.

* Tue Sep 8 2009 Dan Walsh <dwalsh@redhat.com> - 2.0.86-2
- Eliminate -pthread switch in Makefile

* Tue Sep 8 2009 Dan Walsh <dwalsh@redhat.com> - 2.0.86-1
- Update to upstream 
	* Removal of reference counting on userspace AVC SID's.

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.85-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jul 7 2009 Dan Walsh <dwalsh@redhat.com> - 2.0.85-1
- Update to upstream 
	* Reverted Tomas Mraz's fix for freeing thread local storage to avoid
	pthread dependency.
	* Removed fini_context_translations() altogether.
	* Merged lazy init patch from Stephen Smalley based on original patch
	by Steve Grubb.

* Tue Jul 7 2009 Dan Walsh <dwalsh@redhat.com> - 2.0.84-1
- Update to upstream 
	* Add per-service seuser support from Dan Walsh.
	* Let load_policy gracefully handle selinuxfs being mounted from Stephen Smalley.
	* Check /proc/filesystems before /proc/mounts for selinuxfs from Eric
	Paris.

* Wed Jun 24 2009 Dan Walsh <dwalsh@redhat.com> - 2.0.82-2
- Add provices ruby(selinux)

* Tue Jun 23 2009 Dan Walsh <dwalsh@redhat.com> - 2.0.82-1
- Update to upstream 
	* Fix improper use of thread local storage from Tomas Mraz <tmraz@redhat.com>.
	* Label substitution support from Dan Walsh.
	* Support for labeling virtual machine images from Dan Walsh.

* Mon May 18 2009 Dan Walsh <dwalsh@redhat.com> - 2.0.81-1
- Update to upstream 
	* Trim / from the end of input paths to matchpathcon from Dan Walsh.
	* Fix leak in process_line in label_file.c from Hiroshi Shinji.
	* Move matchpathcon to /sbin, add matchpathcon to clean target from Dan Walsh.
	* getdefaultcon to print just the correct match and add verbose option from Dan Walsh.

* Wed Apr 8 2009 Dan Walsh <dwalsh@redhat.com> - 2.0.80-1
- Update to upstream 
	* deny_unknown wrapper function from KaiGai Kohei.
	* security_compute_av_flags API from KaiGai Kohei.
	* Netlink socket management and callbacks from KaiGai Kohei.

* Fri Apr 3 2009 Dan Walsh <dwalsh@redhat.com> - 2.0.79-6
- Fix Memory Leak

* Thu Apr 2 2009 Dan Walsh <dwalsh@redhat.com> - 2.0.79-5
- Fix crash in python

* Sun Mar 29 2009 Dan Walsh <dwalsh@redhat.com> - 2.0.79-4
- Add back in additional interfaces

* Fri Mar 27 2009 Dan Walsh <dwalsh@redhat.com> - 2.0.79-3
- Add back in av_decision to python swig

* Thu Mar 12 2009 Dan Walsh <dwalsh@redhat.com> - 2.0.79-1
- Update to upstream 
	* Netlink socket handoff patch from Adam Jackson.
	* AVC caching of compute_create results by Eric Paris.

* Tue Mar 10 2009 Dan Walsh <dwalsh@redhat.com> - 2.0.78-5
- Add patch from ajax to accellerate X SELinux 
- Update eparis patch

* Mon Mar 9 2009 Dan Walsh <dwalsh@redhat.com> - 2.0.78-4
- Add eparis patch to accellerate Xwindows performance

* Mon Mar 9 2009 Dan Walsh <dwalsh@redhat.com> - 2.0.78-3
- Fix URL 

* Fri Mar 6 2009 Dan Walsh <dwalsh@redhat.com> - 2.0.78-2
- Add substitute pattern 
- matchpathcon output <<none>> on ENOENT

* Mon Mar 2 2009 Dan Walsh <dwalsh@redhat.com> - 2.0.78-1
- Update to upstream
	* Fix incorrect conversion in discover_class code.

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.77-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 18 2009 Dan Walsh <dwalsh@redhat.com> - 2.0.77-5
- Add 
  - selinux_virtual_domain_context_path
  - selinux_virtual_image_context_path

* Tue Jan 6 2009 Dan Walsh <dwalsh@redhat.com> - 2.0.77-3
- Throw exeptions in python swig bindings on failures

* Tue Jan 6 2009 Dan Walsh <dwalsh@redhat.com> - 2.0.77-2
- Fix restorecon python code

* Tue Jan 6 2009 Dan Walsh <dwalsh@redhat.com> - 2.0.77-1
- Update to upstream

* Tue Dec 16 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.76-6
- Strip trailing / for matchpathcon

* Tue Dec 16 2008 Dan Walsh <dwalsh@redhat.com>l - 2.0.76-5
- Fix segfault if seusers file does not work

* Fri Dec 12 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.76-4
- Add new function getseuser which will take username and service and return
- seuser and level.  ipa will populate file in future.
- Change selinuxdefcon to return just the context by default

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 2.0.76-2
- Rebuild for Python 2.6

* Mon Nov 17 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.76-1
- Update to Upstream
	* Allow shell-style wildcards in x_contexts file.

* Mon Nov 17 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.75-2
- Eamon Walsh Patch - libselinux: allow shell-style wildcarding in X names
- Add Restorecon/Install python functions from Luke Macken

* Fri Nov 7 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.75-1
- Update to Upstream
	* Correct message types in AVC log messages.
	* Make matchpathcon -V pass mode from Dan Walsh.
	* Add man page for selinux_file_context_cmp from Dan Walsh.

* Tue Sep 30 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.73-1
- Update to Upstream
	* New man pages from Dan Walsh.
	* Update flask headers from refpolicy trunk from Dan Walsh.

* Fri Sep 26 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.71-6
- Fix matchpathcon -V call 

* Tue Sep 9 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.71-5
- Add flask definitions for open, X and nlmsg_tty_audit

* Tue Sep 9 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.71-4
- Add missing get/setkeycreatecon man pages

* Tue Sep 9 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.71-3
- Split out utilities

* Tue Sep 9 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.71-2
- Add missing man page links for [lf]getfilecon

* Tue Aug 5 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.71-1
- Update to Upstream
	* Add group support to seusers using %groupname syntax from Dan Walsh.
	* Mark setrans socket close-on-exec from Stephen Smalley.
	* Only apply nodups checking to base file contexts from Stephen Smalley.

* Fri Aug 1 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.70-1
- Update to Upstream
	* Merge ruby bindings from Dan Walsh.
- Add support for Linux groups to getseuserbyname

* Fri Aug 1 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.69-2
- Allow group handling in getseuser call

* Tue Jul 29 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.69-1
- Update to Upstream
	* Handle duplicate file context regexes as a fatal error from Stephen Smalley.
	  This prevents adding them via semanage.
	* Fix audit2why shadowed variables from Stephen Smalley.
	* Note that freecon NULL is legal in man page from Karel Zak.

* Wed Jul 9 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.67-4
- Add ruby support for puppet

* Tue Jul 8 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.67-3
- Rebuild for new libsepol

* Sun Jun 29 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.67-2
- Add Karel Zak patch for freecon man page

* Sun Jun 22 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.67-1
- Update to Upstream
	* New and revised AVC, label, and mapping man pages from Eamon Walsh.
	* Add swig python bindings for avc interfaces from Dan Walsh.

* Sun Jun 22 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.65-1
- Update to Upstream
	* Fix selinux_file_context_verify() and selinux_lsetfilecon_default() to call matchpathcon_init_prefix if not already initialized.
	* Add -q qualifier for -V option of matchpathcon and change it to indicate whether verification succeeded or failed via exit status.

* Fri May 16 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.64-3
- libselinux no longer neets to telnet -u in post install

* Wed May 7 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.64-2
- Add sedefaultcon and setconlist commands to dump login context

* Tue Apr 22 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.64-1
- Update to Upstream
	* Fixed selinux_set_callback man page.
	* Try loading the max of the kernel-supported version and the libsepol-supported version when no manipulation of the binary policy is needed from Stephen Smalley.
	* Fix memory leaks in matchpathcon from Eamon Walsh.

* Wed Apr 16 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.61-4
- Add Xavior Toth patch for security_id_t in swig

* Thu Apr 10 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.61-3
- Add avc.h to swig code

* Wed Apr 9 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.61-2
- Grab the latest policy for the kernel

* Tue Apr 1 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.61-1
- Update to Upstream
	* Man page typo fix from Jim Meyering.

* Sun Mar 23 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.60-1
- Update to Upstream
	* Changed selinux_init_load_policy() to not warn about a failed mount of selinuxfs if selinux was disabled in the kernel.

* Thu Mar 13 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.59-2
- Fix matchpathcon memory leak

* Fri Feb 29 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.59-1
- Update to Upstream
	* Merged new X label "poly_selection" namespace from Eamon Walsh.

* Thu Feb 28 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.58-1
- Update to Upstream
	* Merged reset_selinux_config() for load policy from Dan Walsh.

* Thu Feb 28 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.57-2
- Reload library on loading of policy to handle chroot

* Mon Feb 25 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.57-1
- Update to Upstream
	* Merged avc_has_perm() errno fix from Eamon Walsh.

* Fri Feb 22 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.56-1
- Update to Upstream
	* Regenerated Flask headers from refpolicy flask definitions.

* Wed Feb 13 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.55-1
- Update to Upstream
	* Merged compute_member AVC function and manpages from Eamon Walsh.
	* Provide more error reporting on load policy failures from Stephen Smalley.

* Fri Feb 8 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.53-1
- Update to Upstream
	* Merged new X label "poly_prop" namespace from Eamon Walsh.

* Wed Feb 6 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.52-1
- Update to Upstream
	* Disable setlocaldefs if no local boolean or users files are present from Stephen Smalley.
	* Skip userspace preservebools processing for Linux >= 2.6.22 from Stephen Smalley.

* Tue Jan 29 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.50-1
- Update to Upstream
	* Merged fix for audit2why from Dan Walsh.

* Fri Jan 25 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.49-2
- Fix audit2why to grab latest policy versus the one selected by the kernel

* Wed Jan 23 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.49-1
* Merged audit2why python binding from Dan Walsh.

* Wed Jan 23 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.48-1
* Merged updated swig bindings from Dan Walsh, including typemap for pid_t.

* Mon Jan 21 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.47-4
- Update to use libsepol-static library

* Wed Jan 16 2008 Adel Gadllah <adel.gadllah@gmail.com> - 2.0.47-3
- Move libselinux.a to -static package
- Spec cleanups

* Tue Jan 15 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.47-2
- Put back libselinux.a

* Fri Jan 11 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.47-1
- Fix memory references in audit2why and change to use tuples
- Update to Upstream
	* Fix for the avc:  granted null message bug from Stephen Smalley.

* Fri Jan 11 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.46-6
- Fix __init__.py specification

* Tue Jan 8 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.46-5
- Add audit2why python bindings

* Tue Jan 8 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.46-4
- Add pid_t typemap for swig bindings

* Thu Jan 3 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.46-3
- smp_mflag

* Thu Jan 3 2008 Dan Walsh <dwalsh@redhat.com> - 2.0.46-2
- Fix spec file caused by spec review 

* Fri Nov 30 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.46-1
- Upgrade to upstream
	* matchpathcon(8) man page update from Dan Walsh.

* Fri Nov 30 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.45-1
- Upgrade to upstream
	* dlopen libsepol.so.1 rather than libsepol.so from Stephen Smalley.
	* Based on a suggestion from Ulrich Drepper, defer regex compilation until we have a stem match, by Stephen Smalley.
	*  A further optimization would be to defer regex compilation until we have a complete match of the constant prefix of the regex - TBD.

* Thu Nov 15 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.43-1
- Upgrade to upstream
	* Regenerated Flask headers from policy.

* Thu Nov 15 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.42-1
- Upgrade to upstream
	* AVC enforcing mode override patch from Eamon Walsh.
	* Aligned attributes in AVC netlink code from Eamon Walsh.
- Move libselinux.so back into devel package, procps has been fixed

* Tue Nov 6 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.40-1
- Upgrade to upstream
	* Merged refactored AVC netlink code from Eamon Walsh.
	* Merged new X label namespaces from Eamon Walsh.
	* Bux fix and minor refactoring in string representation code.

* Fri Oct 5 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.37-1
- Upgrade to upstream
	* Merged selinux_get_callback, avc_open, empty string mapping from Eamon Walsh.

* Fri Sep 28 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.36-1
- Upgrade to upstream
	* Fix segfault resulting from missing file_contexts file.

* Thu Sep 27 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.35-2
- Fix segfault on missing file_context file

* Wed Sep 26 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.35-1
- Upgrade to upstream
	* Make netlink socket close-on-exec to avoid descriptor leakage from Dan Walsh.
	* Pass CFLAGS when using gcc for linking from Dennis Gilmore. 

* Mon Sep 24 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.34-3
- Add sparc patch to from Dennis Gilmore to build on Sparc platform

* Mon Sep 24 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.34-2
- Remove leaked file descriptor

* Tue Sep 18 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.34-1
- Upgrade to latest from NSA
	* Fix selabel option flag setting for 64-bit from Stephen Smalley.

* Tue Sep 18 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.33-2
- Change matchpatcon to use syslog instead of syserror

* Thu Sep 13 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.33-1
- Upgrade to latest from NSA
	* Re-map a getxattr return value of 0 to a getfilecon return value of -1 with errno EOPNOTSUPP from Stephen Smalley.
	* Fall back to the compat code for security_class_to_string and security_av_perm_to_string from Stephen Smalley.
	* Fix swig binding for rpm_execcon from James Athey.

* Thu Sep 6 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.31-4
- Apply James Athway patch to fix rpm_execcon python binding

* Tue Aug 28 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.31-3
- Move libselinux.so back into main package, breaks procps

* Thu Aug 23 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.31-2
- Upgrade to upstream
	* Fix file_contexts.homedirs path from Todd Miller.

* Tue Aug 21 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.30-2
- Remove requirement on setransd,  Moved to selinux-policy-mls 

* Fri Aug 10 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.30-1
- Move libselinux.so into devel package
- Upgrade to upstream
	* Fix segfault resulting from uninitialized print-callback pointer.
	* Added x_contexts path function patch from Eamon Walsh.
	* Fix build for EMBEDDED=y from Yuichi Nakamura.
	* Fix markup problems in selinux man pages from Dan Walsh.

* Fri Aug 3 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.29-1
- Upgrade to upstream
	* Updated version for stable branch.	
	* Added x_contexts path function patch from Eamon Walsh.
	* Fix build for EMBEDDED=y from Yuichi Nakamura.
	* Fix markup problems in selinux man pages from Dan Walsh.
	* Updated av_permissions.h and flask.h to include new nscd permissions from Dan Walsh.
	* Added swigify to top-level Makefile from Dan Walsh.
	* Fix for string_to_security_class segfault on x86_64 from Stephen
	  Smalley.

* Mon Jul 23 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.24-3
- Apply Steven Smalley patch to fix segfault in string_to_security_class

* Wed Jul 18 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.24-2
- Fix matchpathcon to set default myprintf

* Mon Jul 16 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.24-1
- Upgrade to upstream
	* Fix for getfilecon() for zero-length contexts from Stephen Smalley.

* Wed Jul 11 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.23-3
- Update to match flask/access_vectors in policy

* Tue Jul 10 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.23-2
- Fix man page markup lanquage for translations

* Tue Jun 26 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.23-1
- Fix semanage segfault on x86 platform

* Thu Jun 21 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.22-1
- Upgrade to upstream
	* Labeling and callback interface patches from Eamon Walsh.

* Tue Jun 19 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.21-2
- Refactored swig

* Mon Jun 11 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.21-1
- Upgrade to upstream
	* Class and permission mapping support patches from Eamon Walsh.
	* Object class discovery support patches from Chris PeBenito.
	* Refactoring and errno support in string representation code.

* Fri Jun 1 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.18-1
- Upgrade to upstream
	* Merged patch to reduce size of libselinux and remove need for libsepol for embedded systems from Yuichi Nakamura.
	  This patch also turns the link-time dependency on libsepol into a runtime (dlopen) dependency even in the non-embedded case.

2.0.17 2007-05-31
	* Updated Lindent script and reindented two header files.

* Fri May 4 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.16-1
- Upgrade to upstream
	* Merged additional swig python bindings from Dan Walsh.
	* Merged helpful message when selinuxfs mount fails patch from Dax Kelson.

* Tue Apr 24 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.14-1
- Upgrade to upstream
	* Merged build fix for avc_internal.c from Joshua Brindle.

* Mon Apr 23 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.13-2
- Add get_context_list funcitions to swig file

* Thu Apr 12 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.13-1
- Upgrade to upstream
	* Merged rpm_execcon python binding fix, matchpathcon man page fix, and getsebool -a handling for EACCES from Dan Walsh.

* Thu Apr 12 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.12-2
- Add missing interface

* Wed Apr 11 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.12-1
- Upgrade to upstream
	* Merged support for getting initial contexts from James Carter.

* Mon Apr 9 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.11-1
- Upgrade to upstream
	* Merged userspace AVC patch to follow kernel's behavior for permissive mode in caching previous denials from Eamon Walsh.
	* Merged sidput(NULL) patch from Eamon Walsh.

* Thu Apr 5 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.9-2
- Make rpm_exec swig work

* Tue Mar 27 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.9-1
- Upgrade to upstream
	* Merged class/av string conversion and avc_compute_create patch from Eamon Walsh.

* Tue Mar 27 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.8-1
- Upgrade to upstream
	* Merged fix for avc.h #include's from Eamon Walsh.

* Thu Mar 22 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.7-2
- Add stdint.h to avc.h

* Mon Mar 12 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.7-1
	* Merged patch to drop support for CACHETRANS=0 config option from Steve Grubb.
	* Merged patch to drop support for old /etc/sysconfig/selinux and
	  /etc/security policy file layout from Steve Grubb.

* Tue Mar 8 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.5-2
- Do not fail on permission denied in getsebool

* Tue Feb 27 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.5-1
- Upgrade to upstream
	* Merged init_selinuxmnt() and is_selinux_enabled() improvements from Steve Grubb.

* Fri Feb 21 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.4-1
- Upgrade to upstream
	* Removed sending of setrans init message.
	* Merged matchpathcon memory leak fix from Steve Grubb.

* Thu Feb 20 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.2-1
- Upgrade to upstream
	* Merged more swig initializers from Dan Walsh.

* Tue Feb 20 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.1-1
- Upgrade to upstream
	* Merged patch from Todd Miller to convert int types over to C99 style.

* Wed Feb 7 2007 Dan Walsh <dwalsh@redhat.com> - 2.0.0-1
	* Merged patch from Todd Miller to remove sscanf in matchpathcon.c because
	  of the use of the non-standard format (original patch changed
	  for style).
	* Merged patch from Todd Miller to fix memory leak in matchpathcon.c.
	
* Fri Jan 19 2007 Dan Walsh <dwalsh@redhat.com> - 1.34.0-2
- Add context function to python to split context into 4 parts

* Fri Jan 19 2007 Dan Walsh <dwalsh@redhat.com> - 1.34.0-1
- Upgrade to upstream
	* Updated version for stable branch.	

* Wed Jan 17 2007 Dan Walsh <dwalsh@redhat.com> - 1.33.6-1
- Upgrade to upstream
	* Merged man page updates to make "apropos selinux" work from Dan Walsh.
* Wed Jan 15 2007 Dan Walsh <dwalsh@redhat.com> - 1.33.5-1
- Upgrade to upstream
	* Merged getdefaultcon utility from Dan Walsh.

* Mon Jan 15 2007 Dan Walsh <dwalsh@redhat.com> - 1.33.4-3
- Add Ulrich NSCD__GETSERV and NSCD__SHMEMGRP for Uli

* Fri Jan 12 2007 Dan Walsh <dwalsh@redhat.com> - 1.33.4-2
- Add reference to selinux man page in all man pages to make apropos work
Resolves: # 217881

* Thu Jan 11 2007 Dan Walsh <dwalsh@redhat.com> - 1.33.4-1
- Upstream wanted some minor changes, upgrading to keep api the same
- Upgrade to upstream
	* Merged selinux_check_securetty_context() and support from Dan Walsh.
Resolves: #200110

* Fri Jan 5 2007 Dan Walsh <dwalsh@redhat.com> - 1.33.3-3
- Cleanup patch

* Fri Jan 5 2007 Dan Walsh <dwalsh@redhat.com> - 1.33.3-2
- Add securetty handling
Resolves: #200110

* Thu Jan 4 2007 Dan Walsh <dwalsh@redhat.com> - 1.33.3-1
- Upgrade to upstream
	* Merged patch for matchpathcon utility to use file mode information
	  when available from Dan Walsh.

* Thu Dec  7 2006 Jeremy Katz <katzj@redhat.com> - 1.33.2-4
- rebuild against python 2.5

* Wed Dec 6 2006 Dan Walsh <dwalsh@redhat.com> - 1.33.2-3
- Fix matchpathcon to lstat files

* Thu Nov 30 2006 Dan Walsh <dwalsh@redhat.com> - 1.33.2-2
- Update man page

* Tue Nov 14 2006 Dan Walsh <dwalsh@redhat.com> - 1.33.2-1
- Upgrade to upstream

* Fri Nov 3 2006 Dan Walsh <dwalsh@redhat.com> - 1.33.1-2
- Add James Antill patch for login verification of MLS Levels
-  MLS ragnes need to be checked, Eg. login/cron. This patch adds infrastructure.

* Tue Oct 24 2006 Dan Walsh <dwalsh@redhat.com> - 1.33.1-1
- Upgrade to latest from NSA
	* Merged updated flask definitions from Darrel Goeddel.
 	  This adds the context security class, and also adds
	  the string definitions for setsockcreate and polmatch.

* Tue Oct 17 2006 Dan Walsh <dwalsh@redhat.com> - 1.32-1
- Upgrade to latest from NSA
	* Updated version for release.

* Sun Oct 01 2006 Jesse Keating <jkeating@redhat.com> - 1.30.29-2
- rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Fri Sep  29 2006 Dan Walsh <dwalsh@redhat.com> - 1.30.29-1
- Upgrade to latest from NSA
	* Merged av_permissions.h update from Steve Grubb,
	  adding setsockcreate and polmatch definitions.

* Wed Sep 27 2006 Jeremy Katz <katzj@redhat.com> - 1.30.28-3
- really make -devel depend on libsepol-devel

* Wed Sep  25 2006 Dan Walsh <dwalsh@redhat.com> - 1.30.28-2
- Add sgrubb patch for polmatch

* Wed Sep  13 2006 Dan Walsh <dwalsh@redhat.com> - 1.30.28-1
- Upgrade to latest from NSA
	* Merged patch from Steve Smalley to fix SIGPIPE in setrans_client

* Tue Sep  5 2006 Jeremy Katz <katzj@redhat.com> - 1.30.27-2
- have -devel require libsepol-devel

* Thu Aug 24 2006 Dan Walsh <dwalsh@redhat.com> - 1.30.27-1
- Upgrade to latest from NSA
	* Merged patch to not log avc stats upon a reset from Steve Grubb.
	* Applied patch to revert compat_net setting upon policy load.
	* Merged file context homedir and local path functions from
	  Chris PeBenito.

* Fri Aug 18 2006 Jesse Keating <jkeating@redhat.com> - 1.20.26-2
- rebuilt with latest binutils to pick up 64K -z commonpagesize on ppc*
  (#203001)

* Sat Aug  12 2006 Dan Walsh <dwalsh@redhat.com> - 1.30.25-1
- Upgrade to latest from NSA
	* Merged file context homedir and local path functions from
	  Chris PeBenito.
	* Rework functions that access /proc/pid/attr to access the
	  per-thread nodes, and unify the code to simplify maintenance.

* Fri Aug  11 2006 Dan Walsh <dwalsh@redhat.com> - 1.30.24-1
- Upgrade to latest from NSA
	* Merged return value fix for *getfilecon() from Dan Walsh.
	* Merged sockcreate interfaces from Eric Paris.

* Wed Aug  9 2006 Dan Walsh <dwalsh@redhat.com> - 1.30.22-2
- Fix translation return codes to return size of buffer

* Tue Aug  1 2006 Dan Walsh <dwalsh@redhat.com> - 1.30.22-1
- Upgrade to latest from NSA
	* Merged no-tls-direct-seg-refs patch from Jeremy Katz.
	* Merged netfilter_contexts support patch from Chris PeBenito.

* Tue Aug  1 2006 Dan Walsh <dwalsh@redhat.com> - 1.30.20-1
- Upgrade to latest from NSA
	* Merged context_*_set errno patch from Jim Meyering.

* Tue Aug  1 2006 Jeremy Katz <katzj@redhat.com> - 1.30.19-5
- only build non-fpic objects with -mno-tls-direct-seg-refs

* Tue Aug  1 2006 Jeremy Katz <katzj@redhat.com> - 1.30.19-4
- build with -mno-tls-direct-seg-refs on x86 to avoid triggering 
  segfaults with xen (#200783)  

* Mon Jul 17 2006 Dan Walsh <dwalsh@redhat.com> 1.30.19-3
- Rebuild for new gcc

* Tue Jul 11 2006 Dan Walsh <dwalsh@redhat.com> 1.30.19-2
- Fix libselinux to not telinit during installs

* Tue Jul 4 2006 Dan Walsh <dwalsh@redhat.com> 1.30.19-1
- Upgrade to latest from NSA
	* Lindent.
	* Merged {get,set}procattrcon patch set from Eric Paris.
	* Merged re-base of keycreate patch originally by Michael LeMay from Eric Paris.
	* Regenerated Flask headers from refpolicy.
	* Merged patch from Dan Walsh with:
	  - Added selinux_file_context_{cmp,verify}.
	  - Added selinux_lsetfilecon_default.
	  - Delay translation of contexts in matchpathcon.

* Wed Jun 21 2006 Dan Walsh <dwalsh@redhat.com> 1.30.15-5
- Yet another change to matchpathcon

* Wed Jun 21 2006 Dan Walsh <dwalsh@redhat.com> 1.30.15-4
- Turn off error printing in library.  Need to compile with DEBUG to get it back

* Wed Jun 21 2006 Dan Walsh <dwalsh@redhat.com> 1.30.15-3
- Fix error reporting of matchpathcon

* Mon Jun 19 2006 Dan Walsh <dwalsh@redhat.com> 1.30.15-2
- Add function to compare file context on disk versus contexts in file_contexts file.

* Fri Jun 16 2006 Dan Walsh <dwalsh@redhat.com> 1.30.15-1
- Upgrade to latest from NSA
	* Merged patch from Dan Walsh with:
	* Added selinux_getpolicytype() function.
	* Modified setrans code to skip processing if !mls_enabled.
	* Set errno in the !selinux_mnt case.
	* Allocate large buffers from the heap, not on stack.
	  Affects is_context_customizable, selinux_init_load_policy,
	  and selinux_getenforcemode.

* Thu Jun 8 2006 Dan Walsh <dwalsh@redhat.com> 1.30.12-2
- Add selinux_getpolicytype()

* Thu Jun 1 2006 Dan Walsh <dwalsh@redhat.com> 1.30.12-1
- Upgrade to latest from NSA
	* Merged !selinux_mnt checks from Ian Kent.

* Thu Jun 1 2006 Dan Walsh <dwalsh@redhat.com> 1.30.11-2
- Check for selinux_mnt == NULL

* Tue May 30 2006 Dan Walsh <dwalsh@redhat.com> 1.30.11-1
	* Merged matchmediacon and trans_to_raw_context fixes from 
	  Serge Hallyn.

* Fri May 26 2006 Dan Walsh <dwalsh@redhat.com> 1.30.10-4
- Remove getseuser

* Thu May 25 2006 Dan Walsh <dwalsh@redhat.com> 1.30.10-3
- Bump requires to grab latest libsepol

* Tue May 23 2006 Dan Walsh <dwalsh@redhat.com> 1.30.10-2
- Add BuildRequires for swig

* Tue May 23 2006 Dan Walsh <dwalsh@redhat.com> 1.30.10-1
- Upgrade to latest from NSA
	* Merged simple setrans client cache from Dan Walsh.
	  Merged avcstat patch from Russell Coker.
	* Modified selinux_mkload_policy() to also set /selinux/compat_net
	  appropriately for the loaded policy.

* Thu May 18 2006 Dan Walsh <dwalsh@redhat.com> 1.30.8-1
- More fixes for translation cache
- Upgrade to latest from NSA
	* Added matchpathcon_fini() function to free memory allocated by
	  matchpathcon_init().

* Wed May 17 2006 Dan Walsh <dwalsh@redhat.com> 1.30.7-2
- Add simple cache to improve translation speed

* Tue May 16 2006 Dan Walsh <dwalsh@redhat.com> 1.30.7-1
- Upgrade to latest from NSA
	* Merged setrans client cleanup patch from Steve Grubb.

* Tue May 9 2006 Dan Walsh <dwalsh@redhat.com> 1.30.6-2
- Add Russell's AVC patch to handle large numbers

* Mon May 8 2006 Dan Walsh <dwalsh@redhat.com> 1.30.6-1
- Upgrade to latest from NSA
	* Merged getfscreatecon man page fix from Dan Walsh.
	* Updated booleans(8) man page to drop references to the old
	  booleans file and to note that setsebool can be used to set
	  the boot-time defaults via -P.

* Mon May 8 2006 Dan Walsh <dwalsh@redhat.com> 1.30.5-1
- Upgrade to latest from NSA
	* Merged fix warnings patch from Karl MacMillan.	
	* Merged setrans client support from Dan Walsh.
	  This removes use of libsetrans.
	* Merged patch to eliminate use of PAGE_SIZE constant from Dan Walsh.
	* Merged swig typemap fixes from Glauber de Oliveira Costa.

* Wed May 3 2006 Dan Walsh <dwalsh@redhat.com> 1.30.3-3
- Change the way translations work,  Use setransd/remove libsetrans

* Tue May 2 2006 Dan Walsh <dwalsh@redhat.com> 1.30.3-2
- Add selinuxswig fixes
- Stop using PAGE_SIZE and start using sysconf(_SC_PAGE_SIZE)

* Fri Apr 14 2006 Dan Walsh <dwalsh@redhat.com> 1.30.3-1
- Upgrade to latest from NSA
	* Added distclean target to Makefile.
	* Regenerated swig files.
	* Changed matchpathcon_init to verify that the spec file is
	  a regular file.
	* Merged python binding t_output_helper removal patch from Dan Walsh.

* Mon Apr 11 2006 Dan Walsh <dwalsh@redhat.com> 1.30.1-2
- Fix python bindings for matchpathcon
- Fix booleans man page

* Mon Mar 27 2006 Dan Walsh <dwalsh@redhat.com> 1.30.1-1
	* Merged Makefile PYLIBVER definition patch from Dan Walsh.

* Fri Mar 10 2006 Dan Walsh <dwalsh@redhat.com> 1.30-1
- Make some fixes so it will build on RHEL4
- Upgrade to latest from NSA
	* Updated version for release.
	* Altered rpm_execcon fallback logic for permissive mode to also
	  handle case where /selinux/enforce is not available.

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.29.7-1.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.29.7-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Jan 20 2006 Dan Walsh <dwalsh@redhat.com> 1.29.7-1
- Upgrade to latest from NSA
	* Merged install-pywrap Makefile patch from Joshua Brindle.

* Wed Jan 18 2006 Dan Walsh <dwalsh@redhat.com> 1.29.6-1
- Upgrade to latest from NSA
	* Merged pywrap Makefile patch from Dan Walsh.

* Fri Jan 13 2006 Dan Walsh <dwalsh@redhat.com> 1.29.5-2
- Split out pywrap in Makefile

* Fri Jan 13 2006 Dan Walsh <dwalsh@redhat.com> 1.29.5-1
- Upgrade to latest from NSA
	* Added getseuser test program.

* Fri Jan 7 2006 Dan Walsh <dwalsh@redhat.com> 1.29.4-1
- Upgrade to latest from NSA
	* Added format attribute to myprintf in matchpathcon.c and
	  removed obsoleted rootlen variable in init_selinux_config().

* Wed Jan 4 2006 Dan Walsh <dwalsh@redhat.com> 1.29.3-2
- Build with new libsepol

* Wed Jan 4 2006 Dan Walsh <dwalsh@redhat.com> 1.29.3-1
- Upgrade to latest from NSA
	* Merged several fixes and improvements from Ulrich Drepper
	  (Red Hat), including:
	  - corrected use of getline
	  - further calls to __fsetlocking for local files
	  - use of strdupa and asprintf
	  - proper handling of dirent in booleans code
	  - use of -z relro
	  - several other optimizations
	* Merged getpidcon python wrapper from Dan Walsh (Red Hat).

* Sat Dec 24 2005 Dan Walsh <dwalsh@redhat.com> 1.29.2-4
- Add build requires line for libsepol-devel

* Tue Dec 20 2005 Dan Walsh <dwalsh@redhat.com> 1.29.2-3
- Fix swig call for getpidcon

* Mon Dec 19 2005 Dan Walsh <dwalsh@redhat.com> 1.29.2-2
- Move libselinux.so to base package

* Wed Dec 14 2005 Dan Walsh <dwalsh@redhat.com> 1.29.2-1
- Upgrade to latest from NSA
	* Merged call to finish_context_translations from Dan Walsh.
	  This eliminates a memory leak from failing to release memory
	  allocated by libsetrans.

* Sun Dec 11 2005 Dan Walsh <dwalsh@redhat.com> 1.29.1-3
- update to latest libsetrans  
- Fix potential memory leak

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Thu Dec 8 2005 Dan Walsh <dwalsh@redhat.com> 1.29.1-1
- Update to never version
	* Merged patch for swig interfaces from Dan Walsh.

* Wed Dec 7 2005 Dan Walsh <dwalsh@redhat.com> 1.28-1
- Update to never version

* Wed Dec 7 2005 Dan Walsh <dwalsh@redhat.com> 1.27.28-2
- Fix some of the python swig objects

* Thu Dec 1 2005 Dan Walsh <dwalsh@redhat.com> 1.27.28-1
- Update to latest from NSA
	* Added MATCHPATHCON_VALIDATE flag for set_matchpathcon_flags() and
	  modified matchpathcon implementation to make context validation/
	  canonicalization optional at matchpathcon_init time, deferring it
	  to a successful matchpathcon by default unless the new flag is set
	  by the caller.
	* Added matchpathcon_init_prefix() interface, and
	  reworked matchpathcon implementation to support selective
	  loading of file contexts entries based on prefix matching
	  between the pathname regex stems and the specified path
	  prefix (stem must be a prefix of the specified path prefix).

* Wed Nov 30 2005 Dan Walsh <dwalsh@redhat.com> 1.27.26-1
- Update to latest from NSA
	* Change getsebool to return on/off instead of active/inactive

* Tue Nov 29 2005 Dan Walsh <dwalsh@redhat.com> 1.27.25-1
- Update to latest from NSA
	* Added -f file_contexts option to matchpathcon util.
	  Fixed warning message in matchpathcon_init().
	* Merged Makefile python definitions patch from Dan Walsh.

* Mon Nov 28 2005 Dan Walsh <dwalsh@redhat.com> 1.27.23-1
- Update to latest from NSA
	* Merged swigify patch from Dan Walsh.

* Mon Nov 28 2005 Dan Walsh <dwalsh@redhat.com> 1.27.22-4
- Separate out libselinux-python bindings into separate rpm

* Thu Nov 17 2005 Dan Walsh <dwalsh@redhat.com> 1.27.22-3
- Read libsetrans requirement

* Thu Nov 17 2005 Dan Walsh <dwalsh@redhat.com> 1.27.22-2
- Add python bindings

* Wed Nov 16 2005 Dan Walsh <dwalsh@redhat.com> 1.27.22-1
- Update to latest from NSA
	* Merged make failure in rpm_execcon non-fatal in permissive mode
	  patch from Ivan Gyurdiev.

* Tue Nov 15 2005 Dan Walsh <dwalsh@redhat.com> 1.27.21-2
- Remove requirement for libsetrans

* Tue Nov 8 2005 Dan Walsh <dwalsh@redhat.com> 1.27.21-1
- Update to latest from NSA
	* Added MATCHPATHCON_NOTRANS flag for set_matchpathcon_flags()
	  and modified matchpathcon_init() to skip context translation
	  if it is set by the caller.

* Tue Nov 8 2005 Dan Walsh <dwalsh@redhat.com> 1.27.20-1
- Update to latest from NSA
	* Added security_canonicalize_context() interface and
	  set_matchpathcon_canoncon() interface for obtaining
	  canonical contexts.  Changed matchpathcon internals
	  to obtain canonical contexts by default.  Provided
	  fallback for kernels that lack extended selinuxfs context
	  interface.
- Patch to not translate mls when calling setfiles

* Mon Nov 7 2005 Dan Walsh <dwalsh@redhat.com> 1.27.19-1
- Update to latest from NSA
	* Merged seusers parser changes from Ivan Gyurdiev.
	* Merged setsebool to libsemanage patch from Ivan Gyurdiev.
	* Changed seusers parser to reject empty fields.

* Fri Nov 4 2005 Dan Walsh <dwalsh@redhat.com> 1.27.18-1
- Update to latest from NSA
	* Merged seusers empty level handling patch from Jonathan Kim (TCS).

* Thu Nov 3 2005 Dan Walsh <dwalsh@redhat.com> 1.27.17-4
- Rebuild for latest libsepol

* Mon Oct 31 2005 Dan Walsh <dwalsh@redhat.com> 1.27.17-2
- Rebuild for latest libsepol

* Wed Oct 26 2005 Dan Walsh <dwalsh@redhat.com> 1.27.17-1
- Change default to __default__

* Wed Oct 26 2005 Dan Walsh <dwalsh@redhat.com> 1.27.14-3
- Change default to __default__

* Tue Oct 25 2005 Dan Walsh <dwalsh@redhat.com> 1.27.14-2
- Add selinux_translations_path

* Tue Oct 25 2005 Dan Walsh <dwalsh@redhat.com> 1.27.14-1
- Update to latest from NSA
	* Merged selinux_path() and selinux_homedir_context_path()
	  functions from Joshua Brindle.

* Fri Oct 21 2005 Dan Walsh <dwalsh@redhat.com> 1.27.13-2
- Need to check for /sbin/telinit

* Thu Oct 20 2005 Dan Walsh <dwalsh@redhat.com> 1.27.13-1
- Update to latest from NSA
	* Merged fixes for make DESTDIR= builds from Joshua Brindle.

* Mon Oct 17 2005 Dan Walsh <dwalsh@redhat.com> 1.27.12-1
- Update to latest from NSA
	* Merged get_default_context_with_rolelevel and man pages from
	  Dan Walsh (Red Hat).
	* Updated call to sepol_policydb_to_image for sepol changes.
	* Changed getseuserbyname to ignore empty lines and to handle
	no matching entry in the same manner as no seusers file.

* Fri Oct 14 2005 Dan Walsh <dwalsh@redhat.com> 1.27.9-2
- Tell init to reexec itself in post script

* Fri Oct 7 2005 Dan Walsh <dwalsh@redhat.com> 1.27.9-1
- Update to latest from NSA
	* Changed selinux_mkload_policy to try downgrading the
	latest policy version available to the kernel-supported version.
	* Changed selinux_mkload_policy to fall back to the maximum
	policy version supported by libsepol if the kernel policy version
	falls outside of the supported range.

* Fri Oct 7 2005 Dan Walsh <dwalsh@redhat.com> 1.27.7-1
- Update to latest from NSA
	* Changed getseuserbyname to fall back to the Linux username and
	NULL level if seusers config file doesn't exist unless 
	REQUIRESEUSERS=1 is set in /etc/selinux/config.
	* Moved seusers.conf under $SELINUXTYPE and renamed to seusers.

* Thu Oct 6 2005 Dan Walsh <dwalsh@redhat.com> 1.27.6-1
- Update to latest from NSA
	* Added selinux_init_load_policy() function as an even higher level
	interface for the initial policy load by /sbin/init.  This obsoletes
	the load_policy() function in the sysvinit-selinux.patch. 
	* Added selinux_mkload_policy() function as a higher level interface
	for loading policy than the security_load_policy() interface.

* Thu Oct 6 2005 Dan Walsh <dwalsh@redhat.com> 1.27.4-1
- Update to latest from NSA
	* Merged fix for matchpathcon (regcomp error checking) from Johan
	Fischer.  Also added use of regerror to obtain the error string
	for inclusion in the error message.

* Tue Oct 4 2005 Dan Walsh <dwalsh@redhat.com> 1.27.3-1
- Update to latest from NSA
	* Changed getseuserbyname to not require (and ignore if present)
	the MLS level in seusers.conf if MLS is disabled, setting *level
	to NULL in this case.

* Mon Oct 3 2005 Dan Walsh <dwalsh@redhat.com> 1.27.2-1
- Update to latest from NSA
	* Merged getseuserbyname patch from Dan Walsh.

* Thu Sep 29 2005 Dan Walsh <dwalsh@redhat.com> 1.27.1-3
- Fix patch to satisfy upstream

* Wed Sep 28 2005 Dan Walsh <dwalsh@redhat.com> 1.27.1-2
- Update to latest from NSA
- Add getseuserbyname

* Fri Sep 12 2005 Dan Walsh <dwalsh@redhat.com> 1.26-6
- Fix patch call

* Tue Sep 12 2005 Dan Walsh <dwalsh@redhat.com> 1.26-5
- Fix strip_con call

* Tue Sep 12 2005 Dan Walsh <dwalsh@redhat.com> 1.26-3
- Go back to original libsetrans code

* Mon Sep 12 2005 Dan Walsh <dwalsh@redhat.com> 1.26-2
- Eliminate forth param from mls context when mls is not enabled.

* Tue Sep 6 2005 Dan Walsh <dwalsh@redhat.com> 1.25.7-1
- Update from NSA
	* Merged modified form of patch to avoid dlopen/dlclose by
	the static libselinux from Dan Walsh.  Users of the static libselinux
	will not have any context translation by default.

* Thu Sep 1 2005 Dan Walsh <dwalsh@redhat.com> 1.25.6-1
- Update from NSA
	* Added public functions to export context translation to
	users of libselinux (selinux_trans_to_raw_context,
	selinux_raw_to_trans_context).

* Mon Aug 29 2005 Dan Walsh <dwalsh@redhat.com> 1.25.5-1
- Update from NSA
	* Remove special definition for context_range_set; use
	common code.

* Thu Aug 25 2005 Dan Walsh <dwalsh@redhat.com> 1.25.4-1
- Update from NSA
	* Hid translation-related symbols entirely and ensured that 
	raw functions have hidden definitions for internal use.
	* Allowed setting NULL via context_set* functions.
	* Allowed whitespace in MLS component of context.
	* Changed rpm_execcon to use translated functions to workaround
	lack of MLS level on upgraded systems.

* Wed Aug 24 2005 Dan Walsh <dwalsh@redhat.com> 1.25.3-2
- Allow set_comp on unset ranges

* Wed Aug 24 2005 Dan Walsh <dwalsh@redhat.com> 1.25.3-1
	* Merged context translation patch, originally by TCS,
	  with modifications by Dan Walsh (Red Hat).

* Wed Aug 17 2005 Dan Walsh <dwalsh@redhat.com> 1.25.2-2
- Apply translation patch

* Thu Aug 11 2005 Dan Walsh <dwalsh@redhat.com> 1.25.2-1
- Update from NSA
	* Merged several fixes for error handling paths in the
	  AVC sidtab, matchpathcon, booleans, context, and get_context_list
	  code from Serge Hallyn (IBM). Bugs found by Coverity.
	* Removed setupns; migrated to pam.
	* Merged patches to rename checkPasswdAccess() from Joshua Brindle.
	  Original symbol is temporarily retained for compatibility until 
	  all callers are updated.

* Mon Jul 18 2005 Dan Walsh <dwalsh@redhat.com> 1.24.2-1
- Update makefiles

* Wed Jun 29 2005 Dan Walsh <dwalsh@redhat.com> 1.24.1-1
- Update from NSA
	* Merged security_setupns() from Chad Sellers.
- fix selinuxenabled man page

* Fri May 20 2005 Dan Walsh <dwalsh@redhat.com> 1.23.11-1
- Update from NSA
	* Merged avcstat and selinux man page from Dan Walsh.
	* Changed security_load_booleans to process booleans.local 
	  even if booleans file doesn't exist.
	
* Fri Apr 26 2005 Dan Walsh <dwalsh@redhat.com> 1.23.10-3
- Fix avcstat to clear totals

* Fri Apr 26 2005 Dan Walsh <dwalsh@redhat.com> 1.23.10-2
- Add info to man page

* Fri Apr 26 2005 Dan Walsh <dwalsh@redhat.com> 1.23.10-1
- Update from NSA
	* Merged set_selinuxmnt patch from Bill Nottingham (Red Hat).
	* Rewrote get_ordered_context_list and helpers, including
	  changing logic to allow variable MLS fields.

* Tue Apr 26 2005 Dan Walsh <dwalsh@redhat.com> 1.23.8-1
- Update from NSA

* Thu Apr 21 2005 Dan Walsh <dwalsh@redhat.com> 1.23.7-3
- Add backin matchpathcon

* Wed Apr 13 2005 Dan Walsh <dwalsh@redhat.com> 1.23.7-2
- Fix selinux_policy_root man page

* Wed Apr 13 2005 Dan Walsh <dwalsh@redhat.com> 1.23.7-1
- Change assert(selinux_mnt) to if (!selinux_mnt) return -1;

* Mon Apr 11 2005 Dan Walsh <dwalsh@redhat.com> 1.23.6-1
- Update from NSA
	* Fixed bug in matchpathcon_filespec_destroy.

* Wed Apr 6 2005 Dan Walsh <dwalsh@redhat.com> 1.23.5-1
- Update from NSA
	* Fixed bug in rpm_execcon error handling path.

* Mon Apr 4 2005 Dan Walsh <dwalsh@redhat.com> 1.23.4-1
- Update from NSA
	* Merged fix for set_matchpathcon* functions from Andreas Steinmetz.
	* Merged fix for getconlist utility from Andreas Steinmetz.

* Tue Mar 29 2005 Dan Walsh <dwalsh@redhat.com> 1.23.2-3
- Update from NSA

* Wed Mar 23 2005 Dan Walsh <dwalsh@redhat.com> 1.23.2-2
- Better handling of booleans

* Thu Mar 17 2005 Dan Walsh <dwalsh@redhat.com> 1.23.2-1
- Update from NSA
	* Merged destructors patch from Tomas Mraz.

* Thu Mar 17 2005 Dan Walsh <dwalsh@redhat.com> 1.23.1-1
- Update from NSA
	* Added set_matchpathcon_flags() function for setting flags
	  controlling operation of matchpathcon.  MATCHPATHCON_BASEONLY
	  means only process the base file_contexts file, not 
	  file_contexts.homedirs or file_contexts.local, and is for use by
	  setfiles -c.
	* Updated matchpathcon.3 man page.

* Thu Mar 10 2005 Dan Walsh <dwalsh@redhat.com> 1.22-1
- Update from NSA

* Tue Mar 8 2005 Dan Walsh <dwalsh@redhat.com> 1.21.13-1
- Update from NSA
	* Fixed bug in matchpathcon_filespec_add() - failure to clear fl_head.

* Tue Mar 1 2005 Dan Walsh <dwalsh@redhat.com> 1.21.12-1
- Update from NSA
  * Changed matchpathcon_common to ignore any non-format bits in the mode.

* Mon Feb 28 2005 Dan Walsh <dwalsh@redhat.com> 1.21.11-2
- Default matchpathcon to regular files if the user specifies a mode

* Tue Feb 22 2005 Dan Walsh <dwalsh@redhat.com> 1.21.11-1
- Update from NSA
	* Merged several fixes from Ulrich Drepper.

* Mon Feb 21 2005 Dan Walsh <dwalsh@redhat.com> 1.21.10-3
- Fix matchpathcon on eof.

* Thu Feb 17 2005 Dan Walsh <dwalsh@redhat.com> 1.21.10-1
- Update from NSA
	* Merged matchpathcon patch for file_contexts.homedir from Dan Walsh.
	* Added selinux_users_path() for path to directory containing
	  system.users and local.users.

* Thu Feb 10 2005 Dan Walsh <dwalsh@redhat.com> 1.21.9-2
- Process file_context.homedir

* Thu Feb 10 2005 Dan Walsh <dwalsh@redhat.com> 1.21.9-1
- Update from NSA
  *	 Changed relabel Makefile target to use restorecon.

* Tue Feb 8 2005 Dan Walsh <dwalsh@redhat.com> 1.21.8-1
- Update from NSA
	* Regenerated av_permissions.h.

* Wed Feb 2 2005 Dan Walsh <dwalsh@redhat.com> 1.21.7-1
- Update from NSA
	* Modified avc_dump_av to explicitly check for any permissions that
	  cannot be mapped to string names and display them as a hex value.
	* Regenerated av_permissions.h.

* Mon Jan 31 2005 Dan Walsh <dwalsh@redhat.com> 1.21.5-1
- Update from NSA
	* Generalized matchpathcon internals, exported more interfaces,
	  and moved additional code from setfiles into libselinux so that
	  setfiles can directly use matchpathcon.

* Fri Jan 28 2005 Dan Walsh <dwalsh@redhat.com> 1.21.4-1
- Update from NSA
	* Prevent overflow of spec array in matchpathcon.
	* Fixed several uses of internal functions to avoid relocations.
	* Changed rpm_execcon to check is_selinux_enabled() and fallback to
	  a regular execve if not enabled (or unable to determine due to a lack
	  of /proc, e.g. chroot'd environment).

* Wed Jan 26 2005 Dan Walsh <dwalsh@redhat.com> 1.21.2-1
- Update from NSA
	* Merged minor fix for avcstat from Dan Walsh.

* Mon Jan 24 2005 Dan Walsh <dwalsh@redhat.com> 1.21.1-3
- rpmexeccon should not fail in permissive mode.

* Fri Jan 20 2005 Dan Walsh <dwalsh@redhat.com> 1.21.1-2
- fix printf in avcstat

* Thu Jan 20 2005 Dan Walsh <dwalsh@redhat.com> 1.21.1-1
- Update from NSA

* Wed Jan 12 2005 Dan Walsh <dwalsh@redhat.com> 1.20.1-3
- Modify matchpathcon to also process file_contexts.local if it exists

* Wed Jan 12 2005 Dan Walsh <dwalsh@redhat.com> 1.20.1-2
- Add is_customizable_types function call

* Fri Jan 7 2005 Dan Walsh <dwalsh@redhat.com> 1.20.1-1
- Update to latest from upstream
	* Just changing version number to match upstream

* Wed Dec 29 2004 Dan Walsh <dwalsh@redhat.com> 1.19.4-1
- Update to latest from upstream
	* Changed matchpathcon to return -1 with errno ENOENT for 
	  <<none>> entries, and also for an empty file_contexts configuration.

* Tue Dec 28 2004 Dan Walsh <dwalsh@redhat.com> 1.19.3-3
- Fix link devel libraries

* Mon Dec 27 2004 Dan Walsh <dwalsh@redhat.com> 1.19.3-2
- Fix unitialized variable in avcstat.c

* Tue Nov 30 2004 Dan Walsh <dwalsh@redhat.com> 1.19.3-1
- Upgrade to upstream
	* Removed some trivial utils that were not useful or redundant.
	* Changed BINDIR default to /usr/sbin to match change in Fedora.
	* Added security_compute_member.
	* Added man page for setcon.

* Tue Nov 30 2004 Dan Walsh <dwalsh@redhat.com> 1.19.2-1
- Upgrade to upstream

* Thu Nov 18 2004 Dan Walsh <dwalsh@redhat.com> 1.19.1-6
- Add avcstat program

* Mon Nov 15 2004 Dan Walsh <dwalsh@redhat.com> 1.19.1-4
- Add lots of missing man pages

* Fri Nov 12 2004 Dan Walsh <dwalsh@redhat.com> 1.19.1-2
- Fix output of getsebool.

* Tue Nov 9 2004 Dan Walsh <dwalsh@redhat.com> 1.19.1-1
- Update from upstream, fix setsebool -P segfault

* Fri Nov 5 2004 Steve Grubb <sgrubb@redhat.com> 1.18.1-5
- Add a patch from upstream. Fixes signed/unsigned issues, and 
  incomplete structure copy.

* Thu Nov 4 2004 Dan Walsh <dwalsh@redhat.com> 1.18.1-4
- More fixes from sgrubb, better syslog

* Thu Nov 4 2004 Dan Walsh <dwalsh@redhat.com> 1.18.1-3
- Have setsebool and togglesebool log changes to syslog

* Wed Nov 3 2004 Steve Grubb <sgrubb@redhat.com> 1.18.1-2
- Add patch to make setsebool update bool on disk
- Make togglesebool have a rollback capability in case it blows up inflight

* Tue Nov 2 2004 Dan Walsh <dwalsh@redhat.com> 1.18.1-1
- Upgrade to latest from NSA

* Thu Oct 28 2004 Steve Grubb <sgrubb@redhat.com> 1.17.15-2
- Changed the location of the utilities to /usr/sbin since
  normal users can't use them anyways.

* Wed Oct 27 2004 Steve Grubb <sgrubb@redhat.com> 1.17.15-2
- Updated various utilities, removed utilities that are for testing,
  added man pages.

* Fri Oct 15 2004 Dan Walsh <dwalsh@redhat.com> 1.17.15-1
- Add -g flag to make
- Upgrade to latest  from NSA
	* Added rpm_execcon.

* Fri Oct 1 2004 Dan Walsh <dwalsh@redhat.com> 1.17.14-1
- Upgrade to latest  from NSA
	* Merged setenforce and removable context patch from Dan Walsh.
	* Merged build fix for alpha from Ulrich Drepper.
	* Removed copyright/license from selinux_netlink.h - definitions only.

* Fri Oct 1 2004 Dan Walsh <dwalsh@redhat.com> 1.17.13-3
- Change setenforce to accept Enforcing and Permissive

* Wed Sep 22 2004 Dan Walsh <dwalsh@redhat.com> 1.17.13-2
- Add alpha patch

* Mon Sep 20 2004 Dan Walsh <dwalsh@redhat.com> 1.17.13-1
- Upgrade to latest  from NSA

* Thu Sep 16 2004 Dan Walsh <dwalsh@redhat.com> 1.17.12-2
- Add selinux_removable_context_path

* Tue Sep 14 2004 Dan Walsh <dwalsh@redhat.com> 1.17.12-1
- Update from NSA
	* Add matchmediacon

* Tue Sep 14 2004 Dan Walsh <dwalsh@redhat.com> 1.17.11-1
- Update from NSA
	* Merged in matchmediacon changes.

* Fri Sep 10 2004 Dan Walsh <dwalsh@redhat.com> 1.17.10-1
- Update from NSA
	* Regenerated headers for new nscd permissions.

* Wed Sep 8 2004 Dan Walsh <dwalsh@redhat.com> 1.17.9-2
- Add matchmediacon

* Wed Sep 8 2004 Dan Walsh <dwalsh@redhat.com> 1.17.9-1
- Update from NSA
	* Added get_default_context_with_role.

* Thu Sep 2 2004 Dan Walsh <dwalsh@redhat.com> 1.17.8-2
- Clean up spec file
	* Patch from Matthias Saou

* Thu Sep 2 2004 Dan Walsh <dwalsh@redhat.com> 1.17.8-1
- Update from NSA
	* Added set_matchpathcon_printf.	

* Wed Sep 1 2004 Dan Walsh <dwalsh@redhat.com> 1.17.7-1
- Update from NSA
	* Reworked av_inherit.h to allow easier re-use by kernel. 

* Tue Aug 31 2004 Dan Walsh <dwalsh@redhat.com> 1.17.6-1
- Add strcasecmp in selinux_config
- Update from NSA
	* Changed avc_has_perm_noaudit to not fail on netlink errors.
	* Changed avc netlink code to check pid based on patch by Steve Grubb.
	* Merged second optimization patch from Ulrich Drepper.
	* Changed matchpathcon to skip invalid file_contexts entries.
	* Made string tables private to libselinux.
	* Merged strcat->stpcpy patch from Ulrich Drepper.
	* Merged matchpathcon man page from Dan Walsh.
	* Merged patch to eliminate PLTs for local syms from Ulrich Drepper.
	* Autobind netlink socket.
	* Dropped compatibility code from security_compute_user.
	* Merged fix for context_range_set from Chad Hanson.
	* Merged allocation failure checking patch from Chad Hanson.
	* Merged avc netlink error message patch from Colin Walters.


* Mon Aug 30 2004 Dan Walsh <dwalsh@redhat.com> 1.17.5-1
- Update from NSA
	* Merged second optimization patch from Ulrich Drepper.
	* Changed matchpathcon to skip invalid file_contexts entries.
	* Made string tables private to libselinux.
	* Merged strcat->stpcpy patch from Ulrich Drepper.
	* Merged matchpathcon man page from Dan Walsh.
	* Merged patch to eliminate PLTs for local syms from Ulrich Drepper.
	* Autobind netlink socket.
	* Dropped compatibility code from security_compute_user.
	* Merged fix for context_range_set from Chad Hanson.
	* Merged allocation failure checking patch from Chad Hanson.
	* Merged avc netlink error message patch from Colin Walters.

* Mon Aug 30 2004 Dan Walsh <dwalsh@redhat.com> 1.17.4-1
- Update from NSA
- Add optflags

* Fri Aug 26 2004 Dan Walsh <dwalsh@redhat.com> 1.17.3-1
- Update from NSA

* Thu Aug 26 2004 Dan Walsh <dwalsh@redhat.com> 1.17.2-1
- Add matchpathcon man page
- Latest from NSA
	* Merged patch to eliminate PLTs for local syms from Ulrich Drepper.
	* Autobind netlink socket.
	* Dropped compatibility code from security_compute_user.
	* Merged fix for context_range_set from Chad Hanson.
	* Merged allocation failure checking patch from Chad Hanson.
	* Merged avc netlink error message patch from Colin Walters.

* Tue Aug 24 2004 Dan Walsh <dwalsh@redhat.com> 1.17.1-1
- Latest from NSA
	* Autobind netlink socket.
	* Dropped compatibility code from security_compute_user.
	* Merged fix for context_range_set from Chad Hanson.
	* Merged allocation failure checking patch from Chad Hanson.
	* Merged avc netlink error message patch from Colin Walters.

* Sun Aug 22 2004 Dan Walsh <dwalsh@redhat.com> 1.16.1-1
- Latest from NSA

* Thu Aug 19 2004 Colin Walters <walters@redhat.com> 1.16-1
- New upstream version

* Tue Aug 17 2004 Dan Walsh <dwalsh@redhat.com> 1.15.7-1
- Latest from Upstream

* Mon Aug 16 2004 Dan Walsh <dwalsh@redhat.com> 1.15.6-1
- Fix man pages

* Mon Aug 16 2004 Dan Walsh <dwalsh@redhat.com> 1.15.5-1
- Latest from Upstream

* Fri Aug 13 2004 Dan Walsh <dwalsh@redhat.com> 1.15.4-1
- Latest from Upstream

* Thu Aug 12 2004 Dan Walsh <dwalsh@redhat.com> 1.15.3-2
- Add man page for boolean functions and SELinux

* Sat Aug 8 2004 Dan Walsh <dwalsh@redhat.com> 1.15.3-1
- Latest from NSA

* Mon Jul 19 2004 Dan Walsh <dwalsh@redhat.com> 1.15.2-1
- Latest from NSA

* Mon Jul 19 2004 Dan Walsh <dwalsh@redhat.com> 1.15.1-3
- uppercase getenforce returns, to make them match system-config-securitylevel

* Thu Jul 15 2004 Dan Walsh <dwalsh@redhat.com> 1.15.1-2
- Remove old path patch

* Thu Jul 8 2004 Dan Walsh <dwalsh@redhat.com> 1.15.1-1
- Update to latest from NSA
- Add fix to only get old path if file_context file exists in old location

* Wed Jun 30 2004 Dan Walsh <dwalsh@redhat.com> 1.14.1-1
- Update to latest from NSA

* Wed Jun 16 2004 Dan Walsh <dwalsh@redhat.com> 1.13.4-1
- add nlclass patch
- Update to latest from NSA

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Sat Jun 13 2004 Dan Walsh <dwalsh@redhat.com> 1.13.3-2
- Fix selinux_config to break once it finds SELINUXTYPE.

* Fri May 28 2004 Dan Walsh <dwalsh@redhat.com> 1.13.2-1
-Update with latest from NSA

* Thu May 27 2004 Dan Walsh <dwalsh@redhat.com> 1.13.1-1
- Change to use new policy mechanism

* Mon May 17 2004 Dan Walsh <dwalsh@redhat.com> 1.12-2
- add man patch

* Thu May 14 2004 Dan Walsh <dwalsh@redhat.com> 1.12-1
- Update with latest from NSA

* Wed May 5 2004 Dan Walsh <dwalsh@redhat.com> 1.11.4-1
- Update with latest from NSA

* Thu Apr 22 2004 Dan Walsh <dwalsh@redhat.com> 1.11.3-1
- Add changes for relaxed policy 
- Update to match NSA 

* Thu Apr 15 2004 Dan Walsh <dwalsh@redhat.com> 1.11.2-1
- Add relaxed policy changes 

* Thu Apr 15 2004 Dan Walsh <dwalsh@redhat.com> 1.11-4
- Sync with NSA

* Thu Apr 15 2004 Dan Walsh <dwalsh@redhat.com> 1.11-3
- Remove requires glibc>2.3.4

* Wed Apr 14 2004 Dan Walsh <dwalsh@redhat.com> 1.11-2
- Fix selinuxenabled man page.

* Wed Apr 7 2004 Dan Walsh <dwalsh@redhat.com> 1.11-1
- Upgrade to 1.11

* Wed Apr 7 2004 Dan Walsh <dwalsh@redhat.com> 1.10-2
- Add memleaks patch

* Wed Apr 7 2004 Dan Walsh <dwalsh@redhat.com> 1.10-1
- Upgrade to latest from NSA and add more man pages

* Thu Apr 1 2004 Dan Walsh <dwalsh@redhat.com> 1.9-1
- Update to match NSA
- Cleanup some man pages

* Tue Mar 30 2004 Dan Walsh <dwalsh@redhat.com> 1.8-1
- Upgrade to latest from NSA

* Thu Mar 25 2004 Dan Walsh <dwalsh@redhat.com> 1.6-6
- Add Russell's Man pages

* Thu Mar 25 2004 Dan Walsh <dwalsh@redhat.com> 1.6-5
- Change getenforce to also check is_selinux_enabled

* Thu Mar 25 2004 Dan Walsh <dwalsh@redhat.com> 1.6-4
- Add ownership to /usr/include/selinux

* Wed Mar 10 2004 Dan Walsh <dwalsh@redhat.com> 1.6-3
- fix location of file_contexts file.

* Wed Mar 10 2004 Dan Walsh <dwalsh@redhat.com> 1.6-2
- Fix matchpathcon to use BUFSIZ

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Feb 23 2004 Dan Walsh <dwalsh@redhat.com> 1.4-11
- add matchpathcon

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Jan 23 2004 Dan Walsh <dwalsh@redhat.com> 1.4-9
- Add rootok patch

* Wed Jan 14 2004 Dan Walsh <dwalsh@redhat.com> 1.4-8
- Updated getpeernam patch

* Tue Jan 13 2004 Dan Walsh <dwalsh@redhat.com> 1.4-7
- Add getpeernam patch

* Thu Dec 18 2003 Dan Walsh <dwalsh@redhat.com> 1.4-6
- Add getpeercon patch

* Thu Dec 18 2003 Dan Walsh <dwalsh@redhat.com> 1.4-5
- Put mntpoint patch, because found fix for SysVinit

* Wed Dec 17 2003 Dan Walsh <dwalsh@redhat.com> 1.4-4
- Add remove mntpoint patch, because it breaks SysVinit

* Wed Dec 17 2003 Dan Walsh <dwalsh@redhat.com> 1.4-3
- Add mntpoint patch for SysVinit

* Fri Dec 12 2003 Dan Walsh <dwalsh@redhat.com> 1.4-2
- Add -r -u -t to getcon 

* Sat Dec 6 2003 Dan Walsh <dwalsh@redhat.com> 1.4-1
- Upgrade to latest from NSA

* Mon Oct 27 2003 Dan Walsh <dwalsh@redhat.com> 1.3-2
- Fix x86_64 build

* Wed Oct 21 2003 Dan Walsh <dwalsh@redhat.com> 1.3-1
- Latest tarball from NSA.

* Tue Oct 21 2003 Dan Walsh <dwalsh@redhat.com> 1.2-9
- Update with latest changes from NSA

* Mon Oct 20 2003 Dan Walsh <dwalsh@redhat.com> 1.2-8
- Change location of .so file

* Wed Oct 8 2003 Dan Walsh <dwalsh@redhat.com> 1.2-7
- Break out into development library

* Wed Oct  8 2003 Dan Walsh <dwalsh@redhat.com> 1.2-6
- Move location of libselinux.so to /lib

* Fri Oct  3 2003 Dan Walsh <dwalsh@redhat.com> 1.2-5
- Add selinuxenabled patch

* Wed Oct  1 2003 Dan Walsh <dwalsh@redhat.com> 1.2-4
- Update with final NSA 1.2 sources.

* Fri Sep  12 2003 Dan Walsh <dwalsh@redhat.com> 1.2-3
- Update with latest from NSA.

* Fri Aug  28 2003 Dan Walsh <dwalsh@redhat.com> 1.2-2
- Fix to build on x86_64

* Thu Aug  21 2003 Dan Walsh <dwalsh@redhat.com> 1.2-1
- update for version 1.2

* Wed May 27 2003 Dan Walsh <dwalsh@redhat.com> 1.0-1
- Initial version

