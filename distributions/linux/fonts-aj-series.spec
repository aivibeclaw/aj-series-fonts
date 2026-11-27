Name:           fonts-aj-series
Version:        3.1.0
Release:        1%{?dist}
Summary:        AJ Series & Aaahhh Fonts Vibe Enterprise Typefaces (5 Families · 27 Styles · Default 3D Press)
License:        LicenseRef-Aivibe-Open-Ecosystem-NoMod-NoResale-3.1
URL:            https://fonts.aivibe.cloud
Source0:        fonts-aj-series-%{version}.tar.gz
BuildArch:      noarch
Requires:       fontconfig

%description
Five 100%% original enterprise typeface families (27 styles) with Default 3D Mild-Gradient Press, Sound of Font smart phonetics, Chromium/libass bindings, and 25+ unified native languages.

%prep
%setup -q -c -T

%install
mkdir -p %{buildroot}/usr/share/fonts/aj-series/ttf %{buildroot}/etc/fonts/conf.d
if [ -d ../../dist ]; then
  install -m 0444 ../../dist/*/ttf/*.ttf %{buildroot}/usr/share/fonts/aj-series/ttf/
  cp -a ./01-aj-shresti-default.conf %{buildroot}/etc/fonts/conf.d/01-aj-shresti-default.conf
elif [ -d dist ]; then
  install -m 0444 dist/*/ttf/*.ttf %{buildroot}/usr/share/fonts/aj-series/ttf/
  cp -a distributions/linux/01-aj-shresti-default.conf %{buildroot}/etc/fonts/conf.d/01-aj-shresti-default.conf
else
  install -m 0444 %{_sourcedir}/*.ttf %{buildroot}/usr/share/fonts/aj-series/ttf/
  cp -a %{_sourcedir}/01-aj-shresti-default.conf %{buildroot}/etc/fonts/conf.d/01-aj-shresti-default.conf
fi

%post
fc-cache -rf || :

%files
/usr/share/fonts/aj-series
/etc/fonts/conf.d/01-aj-shresti-default.conf
