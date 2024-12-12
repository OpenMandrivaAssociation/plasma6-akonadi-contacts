#define git 20240217
%define gitbranch release/24.02
%define gitbranchd %(echo %{gitbranch} |sed -e "s,/,-,g")
Name:		plasma6-akonadi-contacts
Version:	24.12.0
Release:	%{?git:0.%{git}.}1
Summary:	Akonadi Contacts Integration
License:	GPLv2+ and LGPLv2+
Group:		Graphical desktop/KDE
URL:		https://www.kde.org/
%define is_beta %(if test `echo %{version} |cut -d. -f3` -ge 70; then echo -n 1; else echo -n 0; fi)
%if %{is_beta}
%define ftpdir unstable
%else
%define ftpdir stable
%endif
%if 0%{?git:1}
Source0:	https://invent.kde.org/pim/akonadi-contacts/-/archive/%{gitbranch}/akonadi-contacts-%{gitbranchd}.tar.bz2#/akonadi-contacts-%{git}.tar.bz2
%else
Source0:	http://download.kde.org/%{ftpdir}/release-service/%{version}/src/akonadi-contacts-%{version}.tar.xz
%endif

BuildRequires:	cmake(Qt6)
BuildRequires:	cmake(Qt6Core)
BuildRequires:	cmake(Qt6Gui)
BuildRequires:	cmake(Qt6Test)
BuildRequires:	cmake(Qt6WebEngineCore)
BuildRequires:	cmake(Qt6WebEngineWidgets)
BuildRequires:	cmake(Qt6Widgets)
BuildRequires:	cmake(ECM)
BuildRequires:	cmake(KF6TextTemplate)
BuildRequires:	cmake(KPim6Akonadi)
BuildRequires:	cmake(KPim6AkonadiMime)
BuildRequires:	cmake(KPim6GrantleeTheme)
BuildRequires:	cmake(KPim6Mime)
BuildRequires:	cmake(KPim6Libkleo)
BuildRequires:	cmake(KF6CalendarCore)
BuildRequires:	cmake(KF6Completion)
BuildRequires:	cmake(KF6Codecs)
BuildRequires:	cmake(KF6Contacts)
BuildRequires:	cmake(KF6DBusAddons)
BuildRequires:	cmake(KF6IconThemes)
BuildRequires:	cmake(KF6KIO)
BuildRequires:	cmake(KF6Prison)
BuildRequires:	cmake(KF6TextWidgets)
BuildRequires:	cmake(KF6KCMUtils)
BuildRequires:	cmake(KF6TextUtils)
BuildRequires:	boost-devel
# For QCH format docs
BuildRequires: doxygen
BuildRequires: qt6-qttools-assistant

%description
Akonadi Contacts Integration.

%files -f %{name}.lang
%{_datadir}/qlogging-categories6/akonadi-contacts.categories
%{_datadir}/qlogging-categories6/akonadi-contacts.renamecategories
%{_libdir}/qt6/plugins/akonadi_serializer_addressee.so
%{_libdir}/qt6/plugins/akonadi_serializer_contactgroup.so
%{_datadir}/akonadi/plugins/serializer/akonadi_serializer_addressee.desktop
%{_datadir}/akonadi/plugins/serializer/akonadi_serializer_contactgroup.desktop
%{_datadir}/kf6/akonadi/contact/

#--------------------------------------------------------------------

%define major 6
%define libname %mklibname KPim6AkonadiContactCore

%package -n %{libname}
Summary:      Akonadi Contacts Integration main library
Group:        System/Libraries

%description -n %{libname}
Akonadi Contacts Integration main library.

%files -n %{libname}
%{_libdir}/libKPim6AkonadiContactCore.so*

#--------------------------------------------------------------------

%define major 6
%define wlibname %mklibname KPim6AkonadiContactWidgets

%package -n %{wlibname}
Summary:      Akonadi Contacts Integration widget library
Group:        System/Libraries

%description -n %{wlibname}
Akonadi Contacts Integration widget library.

%files -n %{wlibname}
%{_libdir}/libKPim6AkonadiContactWidgets.so*

#--------------------------------------------------------------------

%define develname %mklibname KPim6AkonadiContactCore -d

%package -n %{develname}
Summary:        Devel stuff for %{name}
Group:          Development/KDE and Qt
Requires:       %{name} = %{EVRD}
Requires:       %{libname} = %{EVRD}
Requires:       %{wlibname} = %{EVRD}

%description -n %{develname}
This package contains header files needed if you wish to build applications
based on %{name}.

%files -n %{develname}
%{_includedir}/KPim6/AkonadiContactCore
%{_libdir}/cmake/KPim6AkonadiContactCore

#--------------------------------------------------------------------

%define wdevelname %mklibname KPim6AkonadiContactWidgets -d

%package -n %{wdevelname}
Summary:        Devel stuff for %{name} Widgets
Group:          Development/KDE and Qt
Requires:       %{name} = %{EVRD}
Requires:       %{libname} = %{EVRD}
Requires:       %{wlibname} = %{EVRD}
Requires:       %{develname} = %{EVRD}

%description -n %{wdevelname}
This package contains header files needed if you wish to build applications
based on %{name} Widgets.

%files -n %{wdevelname}
%{_includedir}/KPim6/AkonadiContactWidgets
%{_libdir}/cmake/KPim6AkonadiContactWidgets/

#--------------------------------------------------------------------

%prep
%autosetup -p1 -n akonadi-contacts-%{?git:%{gitbranchd}}%{!?git:%{version}}
%cmake \
	-DKDE_INSTALL_USE_QT_SYS_PATHS:BOOL=ON \
	-G Ninja

%build
%ninja -C build

%install
%ninja_install -C build
%find_lang akonadicontact6
%find_lang akonadicontact6-serializer
cat *.lang >%{name}.lang
